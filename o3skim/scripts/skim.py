#!/usr/bin/env python3
"""
o3skim is a tool for data reduction for ozone applications.
"""
import argparse
import logging
import sys
import warnings

import o3skim
import xarray as xr

warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    parser = run_parser()
    args = parser.parse_args()
    if args.command is not None:
        run_command(**vars(args))
    else:
        parser.print_help()
    sys.exit(0)  # Shell return 0 == success


def run_parser():
    parser = argparse.ArgumentParser(
        prog='PROG', description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="See '<command> --help' to read about a specific sub-command.")
    parser.add_argument(
        "-v", "--verbosity", type=str, default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help="Sets the logging level (default: %(default)s)")
    parser.add_argument(
        "-o", "--output", type=str, default='o3skim',
        help="Target netCDF file (default: %(default)s)")
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
    operations.add_argument(
        "--year_mean", action='append_const',
        dest='operations', const='year_mean',
        help="Time average accross the year")

    # Parser return
    return parser


def run_command(verbosity, operations, output, paths):
    # Set logging level
    logging.basicConfig(
        level=getattr(logging, verbosity),
        format='%(asctime)s %(name)-24s %(levelname)-8s %(message)s')

    # Common operations
    logging.info("Program start")

    # Loading of DataArray and attributes
    logging.info("Data loading from %s", paths)
    dataset = xr.open_mfdataset(paths)

    # Processing of skimming operations
    logging.info("Data skimming using %s", operations)
    skimmed = o3skim.process(dataset, operations)

    # Saving
    logging.info("Staving result into %s.nc", output)
    o3skim.save(skimmed, output)

    # End of program
    logging.info("End of program")



if __name__ == '__main__':
    main()
