#!/usr/bin/env python3
# coding: utf8

'''Delete DOIs in input file
'''
import sys
import argparse
import logging
import json
import services

import datacite

logger = logging.getLogger(__name__)

def get_args():
    """Parse command-line arguments for deleting DOIs from DOI service.

    Returns:
        dict: A dictionary containing the parsed command-line arguments.
    """
    parser_desc = 'Delete DOIs from DOI service.'
    parser = argparse.ArgumentParser(description=parser_desc)
    parser.add_argument("doifile", help="Line by line file of DOIs to delete")
    parser.add_argument("-c", "--config", help="Config file path (defaults to './config.json')", default='config.json')
    parser.add_argument('-l', '--live', action='store_true', help="Create DOIs on the live system instead of the test system")
    #parser.add_argument('-v', '--verbose', action='store_true', help="Show detailed output")
    args = vars(parser.parse_args())
    return args

def get_config(path):
    with open(path) as json_data_file:
        settings = json.load(json_data_file)
    return settings

def main(argv=None):
    args = get_args()
    infile = args['doifile']
    datacite_params = get_config(args['config'])
    if args['live']:
        datacite_settings = datacite_params['datacite_live']
    else:
        datacite_settings = datacite_params['datacite_test']
    datacite_service = datacite.DataciteService(datacite_settings)
    doi_service = services.DOIService(datacite_service, None, None)
    with open(infile) as fh:
        for line in fh:
            doi_name = line.strip()
            doi_service.delete_doi(doi_name)

if __name__ == "__main__":
    sys.exit(main())