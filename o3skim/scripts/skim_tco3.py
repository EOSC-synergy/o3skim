#!/usr/bin/env python3
"""o3skim is a tool for data reduction for ozone applications.
"""
import argparse
import logging
import sys

import cf_xarray as cfxr
import o3skim
import xarray as xr

class StripArgument(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.strip())


# Script logger setup
logger = logging.getLogger("skim_tco3")

# Parser for script inputs
def create_parser():
    parser = argparse.ArgumentParser(
        prog=f"o3skim", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    # Parser arguments
    parser.add_argument(
        "-v", "--verbosity", type=str, default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help="Sets the logging level (default: %(default)s)")
    parser.add_argument(
        "-o", "--output", type=str, default='toz-skimmed.nc', action=StripArgument,
        help="Output file for skimmed data (default: %(default)s)")
    parser.add_argument(
        "--original_attributes", action='store_true',
        help="Skimming does not filter non cf attributes")
    parser.add_argument(
        "-n", "--variable_name", type=str, action=StripArgument,
        default='atmosphere_mole_content_of_ozone', 
        help="Variable or standard_name to skim (default: %(default)s)")
    parser.add_argument(
        "paths", nargs='+', type=str, action='store',
        help="Paths to netCDF files with the data to skim")

    # Available operations group
    operations = parser.add_argument_group('operations')
    operations.add_argument(
        "--lon_mean", action='append_const',
        dest='operations', const='lon_mean',
        help="Longitudinal mean across the dataset")
    operations.add_argument(
        "--lat_mean", action='append_const',
        dest='operations', const='lat_mean',
        help="Latitudinal mean across the dataset")

    return parser


def main():
    parser = create_parser()
    process(**vars(parser.parse_args()))
    sys.exit(0)  # Shell return 0 == success


def process(paths, operations, variable_name, **options):
    # Set logging level
    logging.basicConfig(
        level=getattr(logging, options["verbosity"]),
        format="%(asctime)s %(name)-24s %(levelname)-8s %(message)s",
    )

    # Common operations
    logger.info("Program start")

    # Loading of DataArray and attributes
    paths = paths[0] if len(paths) == 1 else paths 
    logger.info("Data loading from %s", paths)
    kwargs = dict(data_vars='minimal', concat_dim='time', combine='nested')
    dataset = xr.open_mfdataset(paths, **kwargs)

    # Clean of non cf attributes
    if not options["original_attributes"]:
        o3skim.utils.cf_clean(dataset)

    # Extraction of variable as dataset
    logger.info("Variable %s loading", variable_name)
    bounds = [dataset[v].attrs.get('bounds', None) for v in dataset.coords]
    bounds = [bound for bound in bounds if bound is not None]
    keep_v = set([dataset.cf[variable_name].name] + bounds)
    drop_v = [v for v in dataset.data_vars if v not in keep_v]
    ozone = dataset.cf.drop_vars(drop_v)

    # Variable name standardization
    logger.info("Renaming var %s to 'toz'/'toz_zm", variable_name)    
    operations = operations if operations else []
    if any([x in operations for x in ['lat_mean', 'lon_mean']]):
        ozone = ozone.cf.rename({variable_name: 'toz_zm'})
    else:
        ozone = ozone.cf.rename({variable_name: 'toz'})

    # Load cftime variables to support mean operations
    # See https://github.com/NCAR/esmlab/issues/161
    ozone.cf['time'].load()
    if 'bounds' in ozone.cf['time'].attrs:
        ozone[ozone.cf['time'].attrs['bounds']].load()

    # Processing of skimming operations
    logger.info("Data skimming using %s", operations)
    skimmed = o3skim.process(ozone, operations)

    # Saving
    logger.info("Staving result into %s", options["output"])
    skimmed.to_netcdf(options["output"])

    # End of program
    logger.info("End of program")
    dataset.close()
    ozone.close()
    skimmed.close()


if __name__ == '__main__':
    main()
