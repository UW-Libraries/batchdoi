import sys
import argparse
import logging
import json

import datacite

logger = logging.getLogger(__name__)

def delete_doi(params, doi):
    service = datacite.DataciteService(params, False)
    return service.delete_doi(doi)

def get_args():
    '''Get command line arguments as well as configuration settings'''
    parser_desc = 'Process a batch of DOI requests.'
    parser = argparse.ArgumentParser(description=parser_desc)
    parser.add_argument("doifile", help="Line by line file of DOIs to delete")
    parser.add_argument("-c", "--config", help="Config file path (defaults to './config.json')", default='config.json')
    #parser.add_argument('-v', '--verbose', action='store_true', help="Show detailed output")
    args = vars(parser.parse_args())
    return args

def main(argv=None):
    args = get_args()
    with open(args['config']) as json_data_file:
        params = json.load(json_data_file)
    #params = {v['doi_prefix']:v for (k, v) in settings.items()}
    infile = args['doifile']
    with open(infile) as fh:
        for line in fh:
            doi = line.strip()
            delete_doi(params, doi)

if __name__ == "__main__":
    sys.exit(main())
