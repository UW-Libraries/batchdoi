#!/usr/bin/env python3
# coding: utf8

import sys
import os
import argparse
import configure
import random
import getdata
import check
import datacite
import dcdata
import services


def get_args():
    '''Get command line arguments as well as configuration settings'''
    parser_desc = 'Create, publish, and delete Datacite DOIs.'
    parser = argparse.ArgumentParser(description=parser_desc)
    subparsers = parser.add_subparsers()

    config_parser = subparsers.add_parser('config', description='Configure Datacite credentials')
    config_parser.set_defaults(func=set_config)

    checkdata_parser = subparsers.add_parser('checkdata')
    checkdata_parser.add_argument("datafile", type=str, help="Excel spreadsheet with DOI request data")
    checkdata_parser.set_defaults(func=checkdata)

    create_parser = subparsers.add_parser('create', description='Create Datacite DOIs')
    create_parser.add_argument("datafile", type=str, help="Excel spreadsheet with DOI request data")
    create_parser.add_argument('-s', '--submit', action='store_true', help="Submit DOI data to Datacite")
    create_parser.add_argument('-l', '--live', action='store_true',
                               help="Create DOIs on the live system instead of the test system")
    create_parser.add_argument('-p', '--publish', action='store_true',
                               help="Publish DOIs after creating them. Note that published DOIs cannot be deleted.")
    create_parser.set_defaults(func=create_dois)

    publish_parser = subparsers.add_parser('publish')
    publish_parser.add_argument("doifile", help="File of DOIs to publish")
    publish_parser.set_defaults(func=publish_dois)

    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument("doifile", help="File of DOIs to delete")
    delete_parser.set_defaults(func=delete_dois)

    args = vars(parser.parse_args())
    return args


def set_config():
    configure.set_config()


def checkdata(args):
    datafile = args['datafile']
    if not os.path.exists(datafile):
        print('File {} does not exist.'.format(datafile))
        return False
    header = getdata.extract_header(datafile)
    errors = check.checkheader(header)
    for line, msgs in errors:
        for m in msgs:
            print('Error in row {}: {}'.format(line, m))
    if errors:
        return False
    data = getdata.extract_data(datafile)
    errors = check.checkdata(data)
    for line, msgs in errors:
        for m in msgs:
            print('Error in row {}: {}'.format(line, m))
    return not errors


def create_dois(args):
    if not checkdata(args):
        return
    datafile = args['datafile']
    conf = configure.get_config()
    if args['live']:
        datacite_settings = conf['datacite_live']
    else:
        datacite_settings = conf['datacite_test']
    datacite_service = datacite.DataciteService(datacite_settings)
    names = services.DOINameGenerator(datacite_service, gen_suffix()).doi_names()
    doi_service = services.DOIService(datacite_service, dcdata.create_payload, names)
    for request in getdata.extract_data(datafile):
        doi = doi_service.submit_doi(request, submit=args['submit'])
        print(doi)


def gen_suffix():
    chars = '0123456789bcdfghjkmnpqrstvwxyz' # alphanum without vowels and l
    while True:
        yield ''.join([random.choice(chars) for _ in range(8)])


def publish_dois():
    print('PUBLISH')


def delete_dois():
    test_username = input('Delete the DOIs in file: {}.'.format(doifile))
    print('DELETE')


def main():
    args = get_args()
    if 'func' in args:
        args['func'](args)


if __name__ == "__main__":
    sys.exit(main())