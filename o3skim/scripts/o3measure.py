#!/usr/bin/env python3
"""
o3norm is a tool for data standardization of ozone applications:
"""
import argparse
import logging
import sys

from o3skim.measures_sbuv import sbuv_function

# Script logger setup
logger = logging.getLogger("o3measure")

# Parser for script inputs
parser = argparse.ArgumentParser(
    prog=f"o3measure", description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="See '<command> --help' to read about a specific sub-command.")
parser.add_argument(
    "-n", "--variable-name", type=str, default='tco3_zm',
    help="Variable name inside netCDF output (default: %(default)s)")
parser.add_argument(
    "-v", "--verbosity", type=str, default='INFO',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    help="Sets the logging level (default: %(default)s)")
parser.add_argument(
    "-t", "--target", type=str, default='measures.nc',
    help="Target netCDF file (default: %(default)s)")
subparsers = parser.add_subparsers(dest='command', help='Sub-commands')


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


def run_command(command, **options):
    # Set logging level
    logging.basicConfig(
        level=getattr(logging, options['verbosity']),
        format='%(asctime)s %(name)-24s %(levelname)-8s %(message)s')

    # Common operations
    logger.info("Program start")

    # Loading of DataArray and attributes
    logger.info("Data loading and standardization of measurements")
    dataset = command(options['variable-name'], **options)

    # Saving
    logger.info("Staving result into %s.nc", options['target'])
    dataset.to_netcdf(options['target'])

    # End of program
    logger.info("End of program")


if __name__ == '__main__':
    main()
