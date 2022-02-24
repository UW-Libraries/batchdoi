#!/usr/bin/env python3
# coding: utf8

import sys
import argparse

def get_args():
    '''Get command line arguments as well as configuration settings'''
    parser_desc = 'Create DOIs from input file.'
    parser = argparse.ArgumentParser(description=parser_desc)
    subparsers = parser.add_subparsers()
    create_parser = subparsers.add_parser('create')
    publish_parser = subparsers.add_parser('publish')
    delete_parser = subparsers.add_parser('delete')
    config_parser = subparsers.add_parser('config')
    
    create_parser.add_argument('-f', '--foo', action='store_true', help="FOO")
    publish_parser.add_argument('-b', '--bar', action='store_true', help="BAR")
    
    #parser.add_argument("requests", help="CSV formatted file of DOI requests")
    #parser.add_argument("-c", "--config", help="Config file path (defaults to './config.json')", default='config.json')
    parser.add_argument('-v', '--verbose', action='store_true', help="Show detailed output")
    #parser.add_argument('-s', '--submit', action='store_true', help="Submit DOI data to Datacite")
    #parser.add_argument('-l', '--live', action='store_true', help="Create DOIs on the live system instead of the test system")
    #parser.add_argument('-p', '--publish', action='store_true', help="Publish DOIs in addition to creating them. Note that published DOIs cannot be deleted.")

    config_parser.set_defaults(func=set_config)

    args = vars(parser.parse_args())
    return args

def main():
    args = get_args()
    args['func']()
    #datacite_params = get_config(args['config'])
    print(args)

if __name__ == "__main__":
    sys.exit(main())