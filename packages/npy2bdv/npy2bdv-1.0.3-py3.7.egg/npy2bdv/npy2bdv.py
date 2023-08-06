# Fast writing of numpy arrays to HDF5 format compatible with Fiji/BigDataViewer and BigStitcher
# Author: Nikita Vladimirov
# License: GPL-3.0
import os
import h5py
import numpy as np
from xml.etree import ElementTree as ET
import skimage.transform
import shutil
import z5py

class BdvWriter:
    __version__ = "1.0.2"

    def __init__(self, filename,
                 subsamp_zyx=((1, 1, 1),),
                 blockdim=((4, 256, 256),),
                 compression=None,
                 nilluminations=1, nchannels=1, ntiles=1, nangles=1,
                 overwrite=False,
                 format='h5'):
        """Class for writing multiple numpy 3d-arrays into BigDataViewer/BigStitcher compatible dataset.
        Currently implemented formats: H5, N5.

        Parameters:
        -----------
            filename: string
                Name of the N5 or H5 file to create (full path).
            subsamp_zyx: tuple of tuples
                Subsampling levels in (z,y,x) order. Integers >= 1, default value ((1, 1, 1),) for no subsampling.
            blockdim: tuple of tuples
                Block size for h5 storage, in pixels, in (z,y,x) order. Default ((4,256,256),), see notes.
            compression: None or str
                H5 compression options: (None, 'gzip', 'lzf'), Default is None for high-speed writing.
                N5 compression: (None, 'gzip', 'xz'), default is None (raw).
            nilluminations: int
            nchannels: int
            ntiles: int
            nangles: int
                Number of view attributes, >=1.
            overwrite: boolean
                If True, overwrite existing file. Default False.
            format: str
                Data format to use: 'h5' (default), 'n5'.

        .. note::
        ------
        Input stacks and output files are assumed uint16 type.

        The h5 recommended block (chunk) size should be between 10 KB and 1 MB, larger for large arrays.
        For example, block dimensions (4,256,256)px gives ~0.5MB block size for type int16 (2 bytes) and writes very fast.
        Block size can be larger than stack dimension.
        """
        assert nilluminations >= 1, "Total number of illuminations must be at least 1."
        assert nchannels >= 1, "Total number of channels must be at least 1."
        assert ntiles >= 1, "Total number of tiles must be at least 1."
        assert nangles >= 1, "Total number of angles must be at least 1."
        assert all([isinstance(element, int) for tupl in subsamp_zyx for element in
                    tupl]), 'subsamp values should be integers >= 1.'
        if len(blockdim) < len(subsamp_zyx):
            print(f"INFO: blockdim levels ({len(blockdim)}) < subsamp levels ({len(subsamp_zyx)}):"
                  f" First-level block size {blockdim[0]} will be used for all levels")
        self._fmt = 't{:05d}/s{:02d}/{}'
        self.nsetups = nilluminations * nchannels * ntiles * nangles
        self.nilluminations = nilluminations
        self.nchannels = nchannels
        self.ntiles = ntiles
        self.nangles = nangles
        self.subsamp_zyx = np.asarray(subsamp_zyx)
        self.nlevels = len(subsamp_zyx)
        self.chunks = self._compute_chunk_size(blockdim)
        self.stack_shapes = {}
        self.affine_matrices = {}
        self.affine_names = {}
        self.calibrations = {}
        self.voxel_size_xyz = {}
        self.voxel_units = {}
        self.exposure_time = {}
        self.exposure_units = {}
        self.filename = filename
        self.file_format = format
        self.compression = None
        if os.path.exists(self.filename):
            if overwrite:
                if self.file_format == 'h5':
                    os.remove(self.filename)
                    print("Warning: H5 file already exists, overwriting.")
                elif self.file_format == 'n5':
                    shutil.rmtree(self.filename)
                    print("Warning: N5 dataset already exists, overwriting.")
            else:
                raise FileExistsError(f"File {self.filename} already exists.")
        if self.file_format == 'h5':
            self.file_object = h5py.File(filename, 'a')
            assert compression in (None, 'gzip', 'lzf'), f'H5 compression unknown: {compression}'
            self.compression = compression
            self._write_H5_headers()
        elif self.file_format == 'n5':
            self.file_object = z5py.File(filename[:-2] + 'n5', 'a')
            assert compression in (None, 'gzip', 'xz'), \
                f'N5 compression unknown: {compression}'
            self.compression = 'raw' if compression is None else compression
        else:
            raise ValueError("File format unknown")
        self.virtual_stacks = False
        self.setup_id_present = [[False] * self.nsetups]

    def _write_H5_headers(self):
        """Write resolutions and subdivisions for all setups into h5 file."""
        for isetup in range(self.nsetups):
            group_name = 's{:02d}'.format(isetup)
            if group_name in self.file_object:
                del self.file_object[group_name]
            grp = self.file_object.create_group(group_name)
            data_subsamp = np.flip(self.subsamp_zyx, 1).astype('float64')
            data_chunks = np.flip(self.chunks, 1).astype('int32')
            grp.create_dataset('resolutions', data=data_subsamp, dtype='<f8')
            grp.create_dataset('subdivisions', data=data_chunks, dtype='<i4')

    def append_plane(self, plane, plane_index, time=0, illumination=0, channel=0, tile=0, angle=0):
        """Append a plane to a virtual stack. Requires stack initialization by calling e.g.
        `append_view(stack=None, virtual_stack_dim=(1000,2048,2048))` beforehand.

        Parameters:
        -----------
            plane: array_like
                A 2d numpy array of (y,x) pixel values.
            plane_index: int
                Plane z-position in the virtual stack.
            time: int
                Time index of the view, >=0.
            illumination: int
            channel: int
            tile: int
            angle: int
                Indices of the view attributes, >=0.
        """

        assert self.virtual_stacks, "Appending planes requires initialization with virtual stack, " \
                                    "see append_view(stack=None,...)"
        isetup = self._determine_setup_id(illumination, channel, tile, angle)
        self._update_setup_id_present(isetup, time)
        assert plane.shape == self.stack_shapes[isetup][1:], "Plane dimensions must match (y,x) size of virtual stack."
        assert plane_index < self.stack_shapes[isetup][0], "Plane index must be less than virtual stack z-dimension."
        for ilevel in range(self.nlevels):
            group_name = self._fmt.format(time, isetup, ilevel)
            dataset = self.file_object[group_name]["cells"]
            dataset[plane_index, :, :] = self._subsample_plane(plane, self.subsamp_zyx[ilevel]).astype('int16')

    def append_view(self, stack, virtual_stack_dim=None,
                    time=0, illumination=0, channel=0, tile=0, angle=0,
                    m_affine=None, name_affine='manually defined',
                    voxel_size_xyz=(1, 1, 1), voxel_units='px', calibration=(1, 1, 1),
                    exposure_time=0, exposure_units='s'):
        """
        Write 3-dimensional numpy array (stack) to the h5 file with the specified timepoint `itime` and attributes.

        Parameters:
        -----------
            stack: numpy array (uint16) or None
                A 3-dimensional stack of uint16 data in (z,y,x) axis order.
                If None, creates an empty dataset of size huge_stack_dim.
            virtual_stack_dim: None, or tuple of (z,y,x) dimensions, optional.
                Dimensions to allocate a huge stack and fill it later by individual planes.
            time: int
                Time index, >=0.
            illumination: int
            channel: int
            tile: int
            angle: int
                Indices of the view attributes, >= 0.
            m_affine: a numpy array of shape (3,4), optional.
                Coefficients of affine transformation matrix (m00, m01, ...)
            name_affine: str, optional
                Name of the affine transformation.
            voxel_size_xyz: tuple of size 3, optional
                The physical size of voxel, in voxel_units. Default (1, 1, 1).
            voxel_units: str, optional
                Spatial units, default is 'px'.
            calibration: tuple of size 3, optional
                The anisotropy factors for (x,y,z) voxel calibration. Default (1, 1, 1).
                Leave it default unless you know how it affects transformations.
            exposure_time: float, optional
                Camera exposure time for this view, default 0.
            exposure_units: str, optional
                Time units for this view, default "s".
        """
        isetup = self._determine_setup_id(illumination, channel, tile, angle)
        self._update_setup_id_present(isetup, time)
        assert len(calibration) == 3, "Calibration must be a tuple of 3 elements (x, y, z)."
        assert len(voxel_size_xyz) == 3, "Voxel size must be a tuple of 3 elements (x, y, z)."
        if stack is not None:
            assert len(stack.shape) == 3, "Stack should be a 3-dimensional numpy array (z,y,x)"
            self.stack_shapes[isetup] = stack.shape
        else:
            assert self.file_format == 'h5', "Only H5 is currently implemented for virtual stack writing."
            assert len(virtual_stack_dim) == 3, "Stack is virtual, so parameter virtual_stack_dim must be defined."
            self.stack_shapes[isetup] = virtual_stack_dim
            self.virtual_stacks = True

        if m_affine is not None:
            self.affine_matrices[isetup] = m_affine.copy()
            self.affine_names[isetup] = name_affine
        self.calibrations[isetup] = calibration
        self.voxel_size_xyz[isetup] = voxel_size_xyz
        self.voxel_units[isetup] = voxel_units
        self.exposure_time[isetup] = exposure_time
        self.exposure_units[isetup] = exposure_units

        if self.file_format == 'h5':
            self._write_h5_dataset(stack, isetup, time)
        else:
            self._write_n5_dataset(stack, isetup, time)

    def _write_h5_dataset(self, stack, isetup, time, dtype='int16'):
        """Write the view (stack) as N5 dataset in BigDataViewer format.
        Note that type must be int16, rather than uint16, for correct reading by Fiji (a bug?)"""
        for ilevel in range(self.nlevels):
            group_name = self._fmt.format(time, isetup, ilevel)
            if group_name in self.file_object:
                del self.file_object[group_name]
            grp = self.file_object.create_group(group_name)
            if stack is not None: # real stack, written in one go
                subdata = self._subsample_stack(stack, self.subsamp_zyx[ilevel]).astype(dtype)
                grp.create_dataset('cells', data=subdata, chunks=self.chunks[ilevel],
                                   maxshape=(None, None, None), compression=self.compression, dtype=dtype)
            else:  # virtual stack initialization
                assert self.subsamp_zyx[ilevel][0] == 1, "Virtual stacks must have z-subsampling == 1," \
                                                         " eg subsamp=((1, 1, 1), (1, 4, 4), (1, 16, 16))."
                grp.create_dataset('cells', chunks=self.chunks[ilevel],
                                   shape=virtual_stack_dim // self.subsamp_zyx[ilevel],
                                   compression=self.compression, dtype=dtype)

    def _write_n5_dataset(self, stack, isetup, time, dtype='uint16'):
        """Write the view (stack) as N5 dataset in BigDataViewer format"""
        grp = self.file_object.create_group(f"setup{isetup}/timepoint{time}")
        self.file_object[f"setup{isetup}"].attrs['downsamplingFactors'] = np.flip(self.subsamp_zyx, 1).tolist()
        self.file_object[f"setup{isetup}"].attrs['dataType'] = dtype
        self.file_object[f"setup{isetup}/timepoint{time}"].attrs["resolution"] = list(self.voxel_size_xyz[isetup])
        self.file_object[f"setup{isetup}/timepoint{time}"].attrs["saved_completely"] = True
        self.file_object[f"setup{isetup}/timepoint{time}"].attrs["multiScale"] = True
        if stack is not None:
            for ilevel in range(self.nlevels):
                subdata = self._subsample_stack(stack, self.subsamp_zyx[ilevel]).astype(dtype)
                grp.create_dataset(f"s{ilevel}", data=subdata, chunks=self.chunks[ilevel],
                                   compression=self.compression, dtype=dtype)
                self.file_object[f"setup{isetup}/timepoint{time}/s{ilevel}"].attrs['downsamplingFactors'] = \
                    np.flip(self.subsamp_zyx[ilevel]).tolist()

    def _compute_chunk_size(self, blockdim):
        """Populate the size of h5 chunks.
        Use first-level chunk size if there are more subsampling levels than chunk size levels.
        """
        chunks = []
        base_level = blockdim[0]
        if len(blockdim) < len(self.subsamp_zyx):
            for ilevel in range(len(self.subsamp_zyx)):
                chunks.append(base_level)
            chunks_tuple = tuple(chunks)
        else:
            chunks_tuple = blockdim
        return chunks_tuple

    def _subsample_stack(self, stack, subsamp_level):
        """Subsampling of a 3d stack.
        
        Parameters:
        -----------
            stack, numpy 3d array (z,y,x) of int16
            subsamp_level, array-like with 3 elements, eg (2,4,4) for downsampling z(x2), x and y (x4).
            
        Returns:
        --------
            down-scaled stack, unit16 type.
        """
        if all(subsamp_level[:] == 1):
            stack_sub = stack
        else:
            stack_sub = skimage.transform.downscale_local_mean(stack, tuple(subsamp_level)).astype(np.uint16)
        return stack_sub

    def _subsample_plane(self, plane, subsamp_level):
        """Subsampling of a 2d plane.
        
        Parameters:
        -----------
            plane: numpy 2d array (y,x) of int16
            subsamp_level: array-like with 3 elements, eg (1,4,4) for downsampling x and y (x4).
            
        Returns:
        --------
            down-scaled plane, unit16 type.
        """
        assert subsamp_level[0] == 1, "z-subsampling must be == 1 for virtual stacks."
        if all(subsamp_level[:] == 1):
            plane_sub = plane
        else:
            plane_sub = skimage.transform.downscale_local_mean(plane, tuple(subsamp_level[1:])).astype(np.uint16)
        return plane_sub

    def write_xml(self, ntimes=1,
                  camera_name="camera", microscope_name="SPIM1",
                  microscope_version="0.0", user_name="user1"):
        """
        Write XML header file for the HDF5 file.
        The camera-related view attributes will be written only if `camera_name` is not None.

        Parameters:
        -----------
            ntimes: int
                Number of time points
            camera_name: None or str, optional
                Name of the camera (same for all setups at the moment)
            microscope_name: None or str, optional
            microscope_version: None or str, optional
            user_name: None or str, optional
        """
        assert ntimes >= 1, "Total number of time points must be at least 1."
        root = ET.Element('SpimData')
        root.set('version', '0.2')
        bp = ET.SubElement(root, 'BasePath')
        bp.set('type', 'relative')
        bp.text = '.'
        # new XML data, added by @nvladimus
        generator = ET.SubElement(root, 'generatedBy')
        library = ET.SubElement(generator, 'library')
        library.set('version', self.__version__)
        library.text = "npy2bdv"
        if microscope_name:
            microscope = ET.SubElement(generator, 'microscope')
            ET.SubElement(microscope, 'name').text = microscope_name
            if microscope_version:
                ET.SubElement(microscope, 'version').text = microscope_version
            if user_name:
                ET.SubElement(microscope, 'user').text = user_name
        # end of new XML data

        seqdesc = ET.SubElement(root, 'SequenceDescription')
        imgload = ET.SubElement(seqdesc, 'ImageLoader')
        if self.file_format == 'h5':
            imgload.set('format', 'bdv.hdf5')
            el = ET.SubElement(imgload, 'hdf5')
        else:
            imgload.set('format', 'bdv.n5')
            imgload.set('version', '1.0')
            el = ET.SubElement(imgload, 'n5')
        el.set('type', 'relative')
        el.text = os.path.basename(self.filename)
        # write ViewSetups
        viewsets = ET.SubElement(seqdesc, 'ViewSetups')
        for iillumination in range(self.nilluminations):
            for ichannel in range(self.nchannels):
                for itile in range(self.ntiles):
                    for iangle in range(self.nangles):
                        isetup = self._determine_setup_id(iillumination, ichannel, itile, iangle)
                        if any([self.setup_id_present[t][isetup] for t in range(len(self.setup_id_present))]):
                            vs = ET.SubElement(viewsets, 'ViewSetup')
                            ET.SubElement(vs, 'id').text = str(isetup)
                            ET.SubElement(vs, 'name').text = 'setup ' + str(isetup)
                            nz, ny, nx = tuple(self.stack_shapes[isetup])
                            ET.SubElement(vs, 'size').text = '{} {} {}'.format(nx, ny, nz)
                            vox = ET.SubElement(vs, 'voxelSize')
                            ET.SubElement(vox, 'unit').text = self.voxel_units[isetup]
                            dx, dy, dz = self.voxel_size_xyz[isetup]
                            ET.SubElement(vox, 'size').text = '{} {} {}'.format(dx, dy, dz)
                            # new XML data, added by @nvladimus
                            if camera_name:
                                cam = ET.SubElement(vs, 'camera')
                                ET.SubElement(cam, 'name').text = camera_name
                                ET.SubElement(cam, 'exposureTime').text = '{}'.format(self.exposure_time[isetup])
                                ET.SubElement(cam, 'exposureUnits').text = self.exposure_units[isetup]
                            # end of new XML data
                            a = ET.SubElement(vs, 'attributes')
                            ET.SubElement(a, 'illumination').text = str(iillumination)
                            ET.SubElement(a, 'channel').text = str(ichannel)
                            ET.SubElement(a, 'tile').text = str(itile)
                            ET.SubElement(a, 'angle').text = str(iangle)

        # write Attributes (range of values)
        attrs_illum = ET.SubElement(viewsets, 'Attributes')
        attrs_illum.set('name', 'illumination')
        for iilumination in range(self.nilluminations):
            illum = ET.SubElement(attrs_illum, 'Illumination')
            ET.SubElement(illum, 'id').text = str(iilumination)
            ET.SubElement(illum, 'name').text = 'illumination ' + str(iilumination)

        attrs_chan = ET.SubElement(viewsets, 'Attributes')
        attrs_chan.set('name', 'channel')
        for ichannel in range(self.nchannels):
            chan = ET.SubElement(attrs_chan, 'Channel')
            ET.SubElement(chan, 'id').text = str(ichannel)
            ET.SubElement(chan, 'name').text = 'channel ' + str(ichannel)

        attrs_tile = ET.SubElement(viewsets, 'Attributes')
        attrs_tile.set('name', 'tile')
        for itile in range(self.ntiles):
            tile = ET.SubElement(attrs_tile, 'Tile')
            ET.SubElement(tile, 'id').text = str(itile)
            ET.SubElement(tile, 'name').text = 'tile ' + str(itile)

        attrs_ang = ET.SubElement(viewsets, 'Attributes')
        attrs_ang.set('name', 'angle')
        for iangle in range(self.nangles):
            ang = ET.SubElement(attrs_ang, 'Angle')
            ET.SubElement(ang, 'id').text = str(iangle)
            ET.SubElement(ang, 'name').text = 'angle ' + str(iangle)

        # Time points
        tpoints = ET.SubElement(seqdesc, 'Timepoints')
        tpoints.set('type', 'range')
        ET.SubElement(tpoints, 'first').text = str(0)
        ET.SubElement(tpoints, 'last').text = str(ntimes - 1)

        # missing views
        if any(True in l for l in self.setup_id_present):
            miss_views = ET.SubElement(seqdesc, 'MissingViews')
            for t in range(len(self.setup_id_present)):
                for i in range(len(self.setup_id_present[t])):
                    if not self.setup_id_present[t][i]:
                        miss_view = ET.SubElement(miss_views, 'MissingView')
                        miss_view.set('timepoint', str(t))
                        miss_view.set('setup', str(i))

        # Transformations of coordinate system
        vregs = ET.SubElement(root, 'ViewRegistrations')
        for itime in range(ntimes):
            for isetup in range(self.nsetups):
                if self.setup_id_present[itime][isetup]:
                    vreg = ET.SubElement(vregs, 'ViewRegistration')
                    vreg.set('timepoint', str(itime))
                    vreg.set('setup', str(isetup))
                    # write arbitrary affine transformation, specific for each view
                    if isetup in self.affine_matrices.keys():
                        vt = ET.SubElement(vreg, 'ViewTransform')
                        vt.set('type', 'affine')
                        ET.SubElement(vt, 'Name').text = self.affine_names[isetup]
                        n_prec = 6
                        mx_string = np.array2string(self.affine_matrices[isetup].flatten(), separator=' ',
                                                    precision=n_prec, floatmode='fixed',
                                                    max_line_width=(n_prec+6)*4)
                        ET.SubElement(vt, 'affine').text = mx_string[1:-1].strip()

                    # write registration transformation (calibration)
                    vt = ET.SubElement(vreg, 'ViewTransform')
                    vt.set('type', 'affine')
                    ET.SubElement(vt, 'Name').text = 'calibration'
                    calx, caly, calz = self.calibrations[isetup]
                    ET.SubElement(vt, 'affine').text = \
                        '{} 0.0 0.0 0.0 0.0 {} 0.0 0.0 0.0 0.0 {} 0.0'.format(calx, caly, calz)

        _xml_indent(root)
        tree = ET.ElementTree(root)
        tree.write(os.path.splitext(self.filename)[0] + ".xml", xml_declaration=True, encoding='utf-8', method="xml")

    def _determine_setup_id(self, illumination=0, channel=0, tile=0, angle=0):
        """Takes the view attributes (illumination, channel, tile, angle) and converts them into unique setup_id.
        
        Parameters:
        -----------
            illumination: int
            channel: int)
            tile: int
            angle: int
            
        Returns:
        --------
            setup_id: int, >=0 (first setup)
            """
        setup_id_matrix = np.arange(self.nsetups)
        setup_id_matrix = setup_id_matrix.reshape((self.nilluminations, self.nchannels, self.ntiles, self.nangles))
        setup_id = setup_id_matrix[illumination, channel, tile, angle]
        return setup_id

    def _update_setup_id_present(self, isetup, itime):
        """Update the lookup table (list of lists) for missing setups"""
        if len(self.setup_id_present) <= itime:
            self.setup_id_present.append([False] * self.nsetups)
        self.setup_id_present[itime][isetup] = True

    def close(self):
        """Save changes and close the data file if needed."""
        if self.file_format == "h5":
            self.file_object.close()


class BdvEditor:
    __version__ = "1.0.2"

    def __init__(self, filename):
        """
        Class for reading and editing existing H5/XML file pairs.
        Warning: Editing of H5/XML files occurs in-place, and there is currently no undo option. Use at your own risk.
        Todo: add an option to save results as new XML file.

        Parameters:
        -----------
            filename: string,
                Path to either .h5 or .xml file. The other file of the pair must be present
                in the same folder.
        """
        self._fmt = 't{:05d}/s{:02d}/{}'
        if filename[-2:] == 'h5':
            self.filename_h5 = filename
            self.filename_xml = filename[:-2] + 'xml'
        elif filename[-3:] == 'xml':
            self.filename_h5 = filename[:-3] + 'h5'
            self.filename_xml = filename
        assert os.path.exists(self.filename_h5), f"Error: {self.filename_h5} file not found"
        assert os.path.exists(self.filename_xml), f"Error: {self.filename_xml} file not found"
        self._file_object_h5 = h5py.File(self.filename_h5, 'r+')
        self._root = None
        self.ntimes, self.nilluminations, self.nchannels, self.ntiles, self.nangles = self.get_attribute_count()
        self.nsetups = self.nilluminations * self.nchannels * self.ntiles * self.nangles

    def get_attribute_count(self):
        """ Get the number of view attributes: time points, illuminations, channels, tiles, angles, using the XML file.
        Returns:
        --------
        (ntimes, nilluminations, nchannels, ntiles, nangle)
         """
        with open(self.filename_xml, 'r') as file:
            root = ET.parse(file).getroot()
            element = root.find("./SequenceDescription/Timepoints[@type='range']")
            nt = int(element.find('last').text) - int(element.find('first').text) + 1 if element else 0
            ni = len(root.findall("./SequenceDescription/ViewSetups/Attributes[@name='illumination']/Illumination"))
            nch = len(root.findall("./SequenceDescription/ViewSetups/Attributes[@name='channel']/Channel"))
            ntiles = len(root.findall("./SequenceDescription/ViewSetups/Attributes[@name='tile']/Tile"))
            nang = len(root.findall("./SequenceDescription/ViewSetups/Attributes[@name='angle']/Angle"))
        return nt, ni, nch, ntiles, nang

    def read_view(self, time=0, illumination=0, channel=0, tile=0, angle=0, ilevel=0):
        """Read a view (stack) specified by its time, attributes, and downsampling level into numpy array (uint16).
        Todo: implement detection of missing views using XML file, return None.

        Parameters:
        -----------
            time: int
                Index of time point (default 0).
            illumination: int
            channel: int
            tile: int
            angle: int
                Indices of the view attributes, >= 0.
            ilevel: int
                Level of subsampling, if available (default 0, no subsampling)

        Returns:
        --------
            dataset: numpy array (dim=3, dtype=uint16)"""
        isetup = self._determine_setup_id(illumination, channel, tile, angle)
        group_name = self._fmt.format(time, isetup, ilevel)
        if self._file_object_h5:
            dataset = self._file_object_h5[group_name]["cells"][()].astype('uint16')
            return dataset
        else:
            raise ValueError('File object is None')

    def crop_view(self, bbox_xyz=((1, -1), (1, -1), None), illumination=0, channel=0, tile=0, angle=0, ilevel=0):
        """Crop a view in-place, both in H5 and XML files, for all time points.

        Parameters:
        -----------
            bbox_xyz: tuple of int
                Bounding box of the crop. Default `((1, -1), (2, -2), None)` crops to view[1:-1, 2:-2, :].
            illumination: int
            channel: int
            tile: int
            angle: int
                Indices of the view attributes, >= 0.
            ilevel: int
                Level of subsampling, if available (default 0, no subsampling)
        """
        isetup = self._determine_setup_id(illumination, channel, tile, angle)
        if self._file_object_h5:
            for time in range(self.ntimes):
                group_name = self._fmt.format(time, isetup, ilevel)
                view_dataset = self._file_object_h5[group_name]["cells"]
                view_arr = view_dataset[()]
                if bbox_xyz[0]:
                    view_arr = view_arr[:, :, slice(*bbox_xyz[0])]
                if bbox_xyz[1]:
                    view_arr = view_arr[:, slice(*bbox_xyz[1]), :]
                if bbox_xyz[2]:
                    view_arr = view_arr[slice(*bbox_xyz[2]), :, :]
                view_dataset.resize(view_arr.shape)
                view_dataset[:] = view_arr # Always use braces here! A common mistake to omit them.
                self._file_object_h5.flush()
        else:
            raise FileNotFoundError(self.filename_h5)
        # Edit the XML file as well.
        with open(self.filename_xml, 'r+') as file:
            self._get_xml_root()
            for elem in self._root.findall("./SequenceDescription/ViewSetups/ViewSetup"):
                elem_id = elem.find("id")
                if int(elem_id.text) == isetup:
                    nz, ny, nx = tuple(view_arr.shape)
                    elem_size = elem.find("size")
                    elem_size.text = '{} {} {}'.format(nx, ny, nz)

    def _determine_setup_id(self, illumination=0, channel=0, tile=0, angle=0):
        """Takes the view attributes (illumination, channel, tile, angle) and converts them into unique setup_id.

        Parameters:
        -----------
            illumination: int
            channel: int
            tile: int
            angle: int

        Returns:
        --------
            setup_id: int, >=0 (first setup)
            """
        setup_id_matrix = np.arange(self.nsetups)
        setup_id_matrix = setup_id_matrix.reshape((self.nilluminations, self.nchannels, self.ntiles, self.nangles))
        setup_id = setup_id_matrix[illumination, channel, tile, angle]
        return setup_id

    def get_view_property(self, key, illumination=0, channel=0, tile=0, angle=0) -> tuple:
        """"Get property of a vew setup from XML file. No time information required, since the setups are fixed.
        Tuples are returned in (x, y, z) order, as in the XML file.
        Parameters:
        -----------
            key: str
                Name of the property: 'voxel_size' | 'view_shape'
            illumination: int
            channel: int
            tile: int
            angle: int
                Indices of the view attributes, >= 0.
        Returns:
        --------
            Value of the property, a tuple.
        """
        accepted_keys = ['voxel_size', 'view_shape']
        assert key in accepted_keys, f"Key {key} not recognized, must be one of: {accepted_keys}."
        isetup = self._determine_setup_id(illumination, channel, tile, angle)
        self._get_xml_root()
        if key == 'voxel_size':
            path = "./SequenceDescription/ViewSetups/ViewSetup/voxelSize/size"
            type_caster = float
        elif key == 'view_shape':
            path = "./SequenceDescription/ViewSetups/ViewSetup/size"
            type_caster = int
        props_list = self._root.findall(path)
        # Todo: possible bug here, if the views are not in setupID order.
        assert 0 <= isetup < len(props_list), f"Setup index {isetup} out of range 0..{len(props_list)-1}"
        value = tuple([type_caster(val) for val in props_list[isetup].text.split()])
        return value

    def append_affine(self, m_affine, name_affine="Appended affine transformation using npy2bdv.",
                      time=0, illumination=0, channel=0, tile=0, angle=0):
        """" Append affine transformation to a view. This transformation will be placed on top,
        e.g. executed by the BigStitcher last.
        The transformation is defined as matrix of shape (3,4).
        Each column represents coordinate unit vectors after the transformation.
        The last column represents translation in (x,y,z).

        Parameters:
        -----------
            time: int
                Time index, >=0.
            illumination: int
            channel: int
            tile: int
            angle: int
                Indices of the view attributes, >= 0.
            m_affine: numpy array of shape (3,4)
                Coefficients of affine transformation matrix (m00, m01, ...)
            name_affine: str, optional
                Name of the affine transformation.
            """
        self._get_xml_root()
        isetup = self._determine_setup_id(illumination, channel, tile, angle)
        assert m_affine.shape == (3,4), "m_affine must be a numpy array of shape (3,4)"
        found = False
        for node in self._root.findall('./ViewRegistrations/ViewRegistration'):
            if int(node.attrib['setup']) == isetup and int(node.attrib['timepoint']) == time:
                found = True
                break
        assert found, f'Node not found: <ViewRegistration setup="{isetup}" timepoint="{time}">'
        vt = ET.Element('ViewTransform')
        node.insert(0, vt)
        vt.set('type', 'affine')
        ET.SubElement(vt, 'Name').text = name_affine
        n_prec = 6
        mx_string = np.array2string(m_affine.flatten(), separator=' ',
                                    precision=n_prec, floatmode='fixed',
                                    max_line_width=(n_prec + 6) * 4)
        ET.SubElement(vt, 'affine').text = mx_string[1:-1].strip()

    def _get_xml_root(self):
        """Load the meta-information information from XML header file"""
        assert os.path.exists(self.filename_xml), f"Error: {self.filename_xml} file not found"
        if self._root is None:
            with open(self.filename_xml, 'r') as file:
                self._root = ET.parse(file).getroot()
        else:
            pass

    def finalize(self):
        """Finalize the H5 and XML files: save changes and close them."""
        if self._file_object_h5 is not None:
            self._file_object_h5.close()
        if self._root is not None:
            _xml_indent(self._root)
            tree = ET.ElementTree(self._root)
            shutil.copy(self.filename_xml, self.filename_xml + '~1') # backup the previous XML file.
            tree.write(self.filename_xml, xml_declaration=True, encoding='utf-8', method="xml")


def _xml_indent(elem, level=0):
    """Pretty printing function"""
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            _xml_indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i