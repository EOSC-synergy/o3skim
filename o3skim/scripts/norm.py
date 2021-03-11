#!/usr/bin/env python3
"""
o3norm is a tool for data standardization of ozone applications:
"""
import argparse
import logging
import sys

from o3skim.standardization import ccmi_function, ecmwf_function
from o3skim.standardization import esacci_function, sbuv_function
import o3skim


# Script logger setup
logger = logging.getLogger("o3norm")

# Parser for script inputs
parser = argparse.ArgumentParser(
    prog=f"o3norm", description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="See '<command> --help' to read about a specific sub-command.")
parser.add_argument(
    "-v", "--verbosity", type=str, default='INFO',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    help="Sets the logging level (default: %(default)s)")
parser.add_argument(
    "-t", "--target", type=str, default='o3data',
    help="Target netCDF file (default: %(default)s)")
subparsers = parser.add_subparsers(dest='command', help='Sub-commands')

# Variables to standardize
vars_group = parser.add_mutually_exclusive_group(required=True)
vars_group.add_argument(
    "--tco3_zm", action='append_const',
    dest='parameter', const='tco3_zm',
    help="Standardization for total column ozone")
vars_group.add_argument(
    "--vmro3_zm", action='append_const',
    dest='parameter', const='vmro3_zm',
    help="Standardization for volume mixing ratio ozone")

# Arguments for subcommand CCMI-1
ccmi_parser = subparsers.add_parser('CCMI-1', help='CCMI-1 Source input')
ccmi_coordinates = ccmi_parser.add_argument_group('coordinates')
ccmi_coordinates.add_argument(
    "--time", type=str, default='time',
    help="Time coordinate on dataset (default: %(default)s)")
ccmi_coordinates.add_argument(
    "--plev", type=str, default='plev',
    help="Pressure level coordinate on dataset (default: %(default)s)")
ccmi_coordinates.add_argument(
    "--lat", type=str, default='lat',
    help="Latitude coordinate on dataset (default: %(default)s)")
ccmi_coordinates.add_argument(
    "--lon", type=str, default='lon',
    help="Longitude coordinate on dataset (default: %(default)s)")
ccmi_parser.set_defaults(command=ccmi_function)
ccmi_parser.add_argument(
    "variable", nargs=1, type=str, action='store',
    help="Variable name to load from the netCFD dataset")
ccmi_parser.add_argument(
    "paths", nargs='+', type=str, action='store',
    help="Paths to netCDF files with the variable to load")

# Arguments for subcommand ECMWF
ecmwf_parser = subparsers.add_parser('ECMWF', help='ECMWF Source input')
ecmwf_coordinates = ecmwf_parser.add_argument_group('coordinates')
ecmwf_coordinates.add_argument(
    "--time", type=str, default='time',
    help="Time coordinate on dataset (default: %(default)s)")
ecmwf_coordinates.add_argument(
    "--plev", type=str, default='pressure',
    help="Pressure level coordinate on dataset (default: %(default)s)")
ecmwf_coordinates.add_argument(
    "--lat", type=str, default='latitude',
    help="Latitude coordinate on dataset (default: %(default)s)")
ecmwf_coordinates.add_argument(
    "--lon", type=str, default='longitude',
    help="Longitude coordinate on dataset (default: %(default)s)")
ecmwf_parser.set_defaults(command=ecmwf_function)
ecmwf_parser.add_argument(
    "variable", nargs=1, type=str, action='store',
    help="Variable name to load from the netCFD dataset")
ecmwf_parser.add_argument(
    "paths", nargs='+', type=str, action='store',
    help="Paths to netCDF files with the variable to load")

# Arguments for subcommand ESACCI
esacci_parser = subparsers.add_parser('ESACCI', help='ESACCI Source input')
esacci_coordinates = esacci_parser.add_argument_group('coordinates')
esacci_coordinates.add_argument(
    "--time_position", type=int, default=-2,
    help="Time position from file name (default: %(default)s)")
esacci_coordinates.add_argument(
    "--plev", type=str, default='pressure',
    help="Pressure level coordinate on dataset (default: %(default)s)")
esacci_coordinates.add_argument(
    "--lat", type=str, default='latitude',
    help="Latitude coordinate on dataset (default: %(default)s)")
esacci_coordinates.add_argument(
    "--lon", type=str, default='longitude',
    help="Longitude coordinate on dataset (default: %(default)s)")
esacci_parser.set_defaults(command=esacci_function)
esacci_parser.add_argument(
    "variable", nargs=1, type=str, action='store',
    help="Variable name to load from the netCFD dataset")
esacci_parser.add_argument(
    "paths", nargs='+', type=str, action='store',
    help="Paths to netCDF files with the variable to load")

# Arguments for subcommand SBUV
sbuv_parser = subparsers.add_parser('SBUV', help='SBUV Source input')
sbuv_parser.set_defaults(command=sbuv_function)
sbuv_parser.add_argument(
    "-s", "--delimiter", type=str, default=r'\s+',
    help="Delimiter to use (default: %(default)s)")
sbuv_parser.add_argument(
    "textfile", nargs=1, type=str, action='store',
    help="File .txt with the data to load")


def main():
    args = parser.parse_args()
    if args.command is not None:
        run_command(**vars(args))
    else:
        parser.print_help()
    sys.exit(0)  # Shell return 0 == success


def run_command(command, parameter, verbosity, target, **kwargs):
    # Set logging level
    logging.basicConfig(
        level=getattr(logging, verbosity),
        format='%(asctime)s %(name)-24s %(levelname)-8s %(message)s')

    # Common operations
    logger.info("Program start")

    # Loading of DataArray and attributes
    logger.info("Data loading and standardization of %s", parameter[0])
    dataset = command(parameter, **kwargs)

    # Saving
    logger.info("Staving result into %s.nc", target)
    o3skim.save(dataset, target)

    # End of program
    logger.info("End of program")


if __name__ == '__main__':
    main()
