#!/usr/bin/env python3

import logging
import argparse
import json
import csv

from . import services

LOGGER = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', filemode='w', level=logging.WARNING)


def make_arg_parser():
    """Creates an argument parser for the command line interface.
    """
    parser = argparse.ArgumentParser(description='Manage batches of DOIs.')
    subparsers = parser.add_subparsers(title='commands', dest='command')

    create_parser = subparsers.add_parser('create', help='Create DOIs from input file.')
    create_parser.add_argument("requests", help="CSV formatted file of DOI requests")
    create_parser.add_argument("-c", "--config", help="Config file path (defaults to './config.json')", default='config.json')
    create_parser.add_argument('-s', '--submit', action='store_true', help="Submit DOI data to Datacite")
    create_parser.add_argument('-l', '--live', action='store_true', help="Create DOIs on the live system instead of the test system")
    create_parser.add_argument('-p', '--publish', action='store_true', help="Publish DOIs in addition to creating them. Note that published DOIs cannot be deleted.")

    publish_parser = subparsers.add_parser('publish', help='Publish previously created DOIs.')
    publish_parser.add_argument("doifile", help="Line by line file of DOIs to delete")
    publish_parser.add_argument("-c", "--config", help="Config file path (defaults to './config.json')", default='config.json')
    publish_parser.add_argument('-l', '--live', action='store_true', help="Create DOIs on the live system instead of the test system")

    delete_parser = subparsers.add_parser('delete', help='Delete previously created DOIs.')
    delete_parser.add_argument("doifile", help="Line by line file of DOIs to delete")
    delete_parser.add_argument("-c", "--config", help="Config file path (defaults to './config.json')", default='config.json')
    delete_parser.add_argument('-l', '--live', action='store_true', help="Create DOIs on the live system instead of the test system")

    return parser


def create_dois(args):
    """Creates DOIs from a CSV file.
    """
    datacite_settings = get_datacite_settings(args)
    doi_service = services.DOIService(datacite_settings)

    with open(args.requests) as csvfile:
        reader = csv.DictReader(csvfile)
        for r in reader:
            request_data = {}
            request_data['url'] = r['URL']
            request_data['creators'] = r['Creators']
            request_data['title'] = r['Title']
            request_data['publisher'] = r['Publisher']
            request_data['publication_year'] = r['Publication Year']
            request_data['resource_type'] = r['Resource Type']
            request_data['description'] = r['Description']
            doi = doi_service.submit_doi(request_data, submit=args.submit)
            print(doi)


def publish_dois(args):
    """Publishes DOIs listed in a file.
    """
    datacite_settings = get_datacite_settings(args)
    doi_service = services.DOIService(datacite_settings)
    infile = args.doifile
    with open(infile) as fh:
        for line in fh:
            doi_name = line.strip()
            doi_service.publish_doi(doi_name)


def delete_dois(args):
    """Deletes DOIs listed in a file.
    """
    datacite_settings = get_datacite_settings(args)
    infile = args.doifile
    doi_service = services.DOIService(datacite_settings)
    with open(infile) as fh:
        for line in fh:
            doi_name = line.strip()
            doi_service.delete_doi(doi_name)


def get_datacite_settings(args):
    """Gets the Datacite settings from the config file.
    """
    datacite_params = get_config(args.config)
    if args.live:
        datacite_settings = datacite_params['datacite_live']
    else:
        datacite_settings = datacite_params['datacite_test']
    return datacite_settings


def get_config(path):
    """Read the config info from a file.
    """
    with open(path) as json_data_file:
        settings = json.load(json_data_file)
    return settings


def main():
    parser = make_arg_parser()
    args = parser.parse_args()
    if args.command == 'create':
        create_dois(args)
    elif args.command == 'publish':
        publish_dois(args)
    elif args.command == 'delete':
        delete_dois(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
