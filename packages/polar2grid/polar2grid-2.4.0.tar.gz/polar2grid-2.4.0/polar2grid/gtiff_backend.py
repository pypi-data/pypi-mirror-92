#!/usr/bin/env python3
# encoding: utf-8
# Copyright (C) 2012-2015 Space Science and Engineering Center (SSEC),
# University of Wisconsin-Madison.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This file is part of the polar2grid software package. Polar2grid takes
# satellite observation data, remaps it, and writes it to a file format for
#     input into another program.
# Documentation: http://www.ssec.wisc.edu/software/polar2grid/
#
# Written by David Hoese    November 2014
# University of Wisconsin-Madison
# Space Science and Engineering Center
# 1225 West Dayton Street
# Madison, WI  53706
# david.hoese@ssec.wisc.edu
"""The GeoTIFF backend puts gridded image data into a standard GeoTIFF file.  It
uses the GDAL python API to create the GeoTIFF files. It can handle any grid that
can be described by PROJ.4 and understood by GeoTIFF.

"""
__docformat__ = "restructuredtext en"

import sys
from osgeo import gdal

import logging
import numpy as np
import os
import osr

from polar2grid.core import roles
from polar2grid.core.dtype import clip_to_data_type, str_to_dtype, str2dtype
from polar2grid.core.rescale import Rescaler, DEFAULT_RCONFIG

LOG = logging.getLogger(__name__)

gtiff_driver = gdal.GetDriverByName("GTIFF")

DEFAULT_OUTPUT_PATTERN = "{satellite}_{instrument}_{product_name}_{begin_time}_{grid_name}.tif"


def _proj4_to_srs(proj4_str):
    """Helper function to convert a proj4 string
    into a GDAL compatible srs.  Mainly a function
    so if used multiple times it only has to be changed
    once for special cases.
    """
    try:
        srs = osr.SpatialReference()
        # GDAL doesn't like unicode
        result = srs.ImportFromProj4(str(proj4_str))
    except ValueError:
        LOG.error("Could not convert Proj4 string '%s' into a GDAL SRS" % (proj4_str,))
        LOG.debug("Exception: ", exc_info=True)
        raise ValueError("Could not convert Proj4 string '%s' into a GDAL SRS" % (proj4_str,))

    if result != 0:
        LOG.error("Could not convert Proj4 string '%s' into a GDAL SRS" % (proj4_str,))
        raise ValueError("Could not convert Proj4 string '%s' into a GDAL SRS" % (proj4_str,))

    return srs


def create_geotiff(data, output_filename, proj4_str, geotransform, etype=gdal.GDT_UInt16, compress=None,
                   quicklook=False, tiled=False, blockxsize=None, blockysize=None, colormap=None,
                   fill_value=None, **kwargs):
    """Function that creates a geotiff from the information provided.
    """
    log_level = logging.getLogger('').handlers[0].level or 0
    LOG.info("Creating geotiff '%s'" % (output_filename,))

    # Find the number of bands provided
    if isinstance(data, (list, tuple)):
        num_bands = len(data)
    elif data.ndim == 2:
        num_bands = 1
    else:
        num_bands = data.shape[0]

    # We only know how to handle L, LA, P, PA, RGB, and RGBA
    if num_bands not in [1, 2, 3, 4]:
        msg = "Geotiff backend doesn't know how to handle data of shape '%r'" % (data.shape,)
        LOG.error(msg)
        raise ValueError(msg)

    options = []
    if compress is not None and compress != "NONE":
        options.append("COMPRESS=%s" % (compress,))
    if tiled:
        options.append("TILED=YES")
    if blockxsize is not None:
        options.append("BLOCKXSIZE=%d" % (blockxsize,))
    if blockysize is not None:
        options.append("BLOCKYSIZE=%d" % (blockysize,))

    # Creating the file will truncate any pre-existing file
    LOG.debug("Creation Geotiff with options %r", options)
    if num_bands == 1 and data.ndim == 2:
        gtiff = gtiff_driver.Create(output_filename, data.shape[1], data.shape[0],
                                    bands=num_bands, eType=etype, options=options)
    else:
        gtiff = gtiff_driver.Create(output_filename, data[0].shape[1], data[0].shape[0],
                                    bands=num_bands, eType=etype, options=options)

    gtiff.SetGeoTransform(geotransform)
    srs = _proj4_to_srs(proj4_str)
    gtiff.SetProjection(srs.ExportToWkt())

    for idx in range(num_bands):
        gtiff_band = gtiff.GetRasterBand(idx + 1)

        if num_bands == 1 and data.ndim == 2:
            band_data = data
            if fill_value is not None:
                LOG.debug("Setting geotiff nodata value: {}".format(fill_value))
                gtiff_band.SetNoDataValue(fill_value)
        else:
            band_data = data[idx]

        # Clip data to datatype, otherwise let it go and see what happens
        # XXX: This might need to operate on colors as a whole or
        # do a linear scaling. No one should be scaling data to outside these
        # ranges anyway
        if etype == gdal.GDT_UInt16:
            band_data = clip_to_data_type(band_data, np.uint16)
        elif etype == gdal.GDT_Byte:
            band_data = clip_to_data_type(band_data, np.uint8)
        if log_level <= logging.DEBUG:
            LOG.debug("Data min: %f, max: %f" % (band_data.min(), band_data.max()))

        # Write the data
        if gtiff_band.WriteArray(band_data) != 0:
            LOG.error("Could not write band 1 data to geotiff '%s'" % (output_filename,))
            raise ValueError("Could not write band 1 data to geotiff '%s'" % (output_filename,))

    if colormap is not None:
        LOG.debug("Adding colormap as Geotiff ColorTable")
        from polar2grid.add_colormap import create_colortable, add_colortable
        ct = create_colortable(colormap)
        add_colortable(gtiff, ct)

    if quicklook:
        png_filename = output_filename.replace(os.path.splitext(output_filename)[1], ".png")
        png_driver = gdal.GetDriverByName("PNG")
        png_driver.CreateCopy(png_filename, gtiff)

    # Garbage collection/destructor should close the file properly
    return gtiff


np2etype = {
    np.uint16: gdal.GDT_UInt16,
    np.uint8: gdal.GDT_Byte,
    np.float32: gdal.GDT_Float32,
}


class Backend(roles.BackendRole):
    def __init__(self, rescale_configs=None, **kwargs):
        self.rescale_configs = rescale_configs or [DEFAULT_RCONFIG]
        self.rescaler = Rescaler(*self.rescale_configs)
        super(Backend, self).__init__(**kwargs)

    @property
    def known_grids(self):
        # should work regardless of grid
        return None

    def create_output_from_product(self, gridded_product, output_pattern=None,
                                   data_type=None, inc_by_one=None, fill_value=0,
                                   tiled=False, blockxsize=None, blockysize=None, **kwargs):
        data_type = data_type or np.uint8
        etype = np2etype[data_type]
        inc_by_one = inc_by_one or False
        grid_def = gridded_product["grid_definition"]
        if not output_pattern:
            output_pattern = DEFAULT_OUTPUT_PATTERN
        if "{" in output_pattern:
            # format the filename
            of_kwargs = gridded_product.copy(as_dict=True)
            of_kwargs["data_type"] = data_type
            output_filename = self.create_output_filename(output_pattern,
                                                          grid_name=grid_def["grid_name"],
                                                          rows=grid_def["height"],
                                                          columns=grid_def["width"],
                                                          **of_kwargs)
        else:
            output_filename = output_pattern

        if os.path.isfile(output_filename):
            if not self.overwrite_existing:
                LOG.error("Geotiff file already exists: %s", output_filename)
                raise RuntimeError("Geotiff file already exists: %s" % (output_filename,))
            else:
                LOG.warning("Geotiff file already exists, will overwrite: %s", output_filename)

        try:
            if np.issubdtype(data_type, np.floating):
                # assume they don't want to scale floating point
                data = gridded_product.get_data_array()
                rescale_options = {}
            else:
                LOG.debug("Scaling %s data to fit in geotiff...", gridded_product["product_name"])
                rescale_options = self.rescaler.get_rescale_options(gridded_product,
                                                                    data_type,
                                                                    inc_by_one=inc_by_one,
                                                                    fill_value=fill_value)
                data = self.rescaler.rescale_product(gridded_product, data_type, rescale_options=rescale_options.copy())

            # Create the geotiff
            # X and Y rotation are 0 in most cases so we just hard-code it
            geotransform = gridded_product["grid_definition"].gdal_geotransform
            colormap = rescale_options.get('colormap') if rescale_options.get('method') != 'colorize' else None
            gtiff = create_geotiff(data, output_filename, grid_def["proj4_definition"], geotransform,
                                   etype=etype, tiled=tiled, blockxsize=blockxsize, blockysize=blockysize,
                                   colormap=colormap, fill_value=fill_value, **kwargs)

            if rescale_options.get("method") in ["linear", "palettize", "colorize"] and "min_in" in rescale_options and "max_in" in rescale_options:
                LOG.debug("Setting geotiff metadata for linear min/max values")
                gtiff.SetMetadataItem("min_in", str(rescale_options["min_in"]))
                gtiff.SetMetadataItem("max_in", str(rescale_options["max_in"]))
        except (ValueError, KeyError):
            if not self.keep_intermediate and os.path.isfile(output_filename):
                os.remove(output_filename)
            raise

        return output_filename


def add_backend_argument_groups(parser):
    from polar2grid.writers.geotiff import NumpyDtypeList, NUMPY_DTYPE_STRS
    parser.set_defaults(forced_grids=["wgs84_fit"])
    group = parser.add_argument_group(title="Backend Initialization")
    group.add_argument('--rescale-configs', nargs="*", dest="rescale_configs",
                       help="alternative rescale configuration files")
    group = parser.add_argument_group(title="Backend Output Creation")
    group.add_argument("--output-pattern", default=DEFAULT_OUTPUT_PATTERN,
                       help="output filenaming pattern")
    group.add_argument('--dont-inc', dest="inc_by_one", default=True, action="store_false",
                       help="do not increment data by one (ex. 0-254 -> 1-255 with 0 being fill)")
    group.add_argument("--compress", default="LZW", choices=["JPEG", "LZW", "PACKBITS", "DEFLATE", "NONE"],
                       help="Specify compression method for geotiff")
    group.add_argument("--png-quicklook", dest="quicklook", action="store_true",
                       help="Create a PNG version of the created geotiff")
    group.add_argument("--dtype", dest="data_type", type=str_to_dtype, default=None,
                       choices=NumpyDtypeList(NUMPY_DTYPE_STRS),
                       help="specify the data type for the backend to output "
                            "(default: 'uint8' 8-bit integer)")
    group.add_argument('--tiled', action='store_true',
                       help="Create tiled geotiffs")
    group.add_argument('--blockxsize', default=None, type=int,
                       help="Set tile block X size")
    group.add_argument('--blockysize', default=None, type=int,
                       help="Set tile block Y size")
    return ["Backend Initialization", "Backend Output Creation"]


def main():
    from polar2grid.core.script_utils import create_basic_parser, create_exc_handler, setup_logging
    from polar2grid.core.containers import GriddedScene, GriddedProduct
    parser = create_basic_parser(description="Create geotiff files from provided gridded scene or product data")
    subgroup_titles = add_backend_argument_groups(parser)
    parser.add_argument("--scene", required=True, help="JSON SwathScene filename to be remapped")
    global_keywords = ("keep_intermediate", "overwrite_existing", "exit_on_error")
    args = parser.parse_args(subgroup_titles=subgroup_titles, global_keywords=global_keywords)

    # Logs are renamed once data the provided start date is known
    levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    setup_logging(console_level=levels[min(3, args.verbosity)], log_filename=args.log_fn)
    sys.excepthook = create_exc_handler(LOG.name)

    LOG.info("Loading scene or product...")
    gridded_scene = GriddedScene.load(args.scene)

    LOG.info("Initializing backend...")
    backend = Backend(**args.subgroup_args["Backend Initialization"])
    if isinstance(gridded_scene, GriddedScene):
        backend.create_output_from_scene(gridded_scene, **args.subgroup_args["Backend Output Creation"])
    elif isinstance(gridded_scene, GriddedProduct):
        backend.create_output_from_product(gridded_scene, **args.subgroup_args["Backend Output Creation"])
    else:
        raise ValueError("Unknown Polar2Grid object provided")

if __name__ == "__main__":
    sys.exit(main())
