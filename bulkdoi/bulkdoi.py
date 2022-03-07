#!/usr/bin/env python3
# coding: utf8

import sys
import os
import argparse
import configure

def set_config():
    configure.set_config()

def checkdata(args):
    datafile = args['datafile']
    print('CHECK DATA in file: {}'.format(datafile))
    if not os.path.exists(datafile):
        print('File {} does not exist.'.format(datafile))


def create_dois():
    print('CREATE')
    conf = configure.get_config()
    print(conf)

def publish_dois():
    print('PUBLISH')

def delete_dois():
    test_username = input('Delete the DOIs in file: {}.'.format(doifile))
    print('DELETE')

def get_args():
    '''Get command line arguments as well as configuration settings'''
    parser_desc = 'Create, publish, and delete Datacite DOIs.'
    parser = argparse.ArgumentParser(description=parser_desc)
    subparsers = parser.add_subparsers()
    create_parser = subparsers.add_parser('create', description='Create Datacite DOIs')
    publish_parser = subparsers.add_parser('publish')
    checkdata_parser = subparsers.add_parser('checkdata')
    delete_parser = subparsers.add_parser('delete')
    config_parser = subparsers.add_parser('config', description='Configure Datacite credentials')

    checkdata_parser.add_argument("datafile", type=str, help="Excel spreadsheet with DOI request data")

    create_parser.add_argument("datafile", type=str, help="Excel spreadsheet with DOI request data")
    create_parser.add_argument('-s', '--submit', action='store_true', help="Submit DOI data to Datacite")
    create_parser.add_argument('-l', '--live', action='store_true',
                        help="Create DOIs on the live system instead of the test system")
    create_parser.add_argument('-p', '--publish', action='store_true', help="Publish DOIs in addition to creating them. Note that published DOIs cannot be deleted.")

    publish_parser.add_argument("doifile", help="File of DOIs to publish")

    delete_parser.add_argument("doifile", help="File of DOIs to delete")

    config_parser.set_defaults(func=set_config)
    checkdata_parser.set_defaults(func=checkdata)
    create_parser.set_defaults(func=create_dois)
    publish_parser.set_defaults(func=publish_dois)
    delete_parser.set_defaults(func=delete_dois)

    args = vars(parser.parse_args())
    return args

def main():
    args = get_args()
    if 'func' in args:
        args['func'](args)
    #datacite_params = get_config(args['config'])
    #print(args)

if __name__ == "__main__":
    sys.exit(main())