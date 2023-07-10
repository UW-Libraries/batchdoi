import argparse
import json

import create
import publish
import delete

def create_dois(args):
    datacite_settings = get_datacite_settings(args)
    create.main(args, datacite_settings)

def publish_dois(args):
    datacite_settings = get_datacite_settings(args)
    publish.main(args, datacite_settings)

def delete_dois(args):
    datacite_settings = get_datacite_settings(args)
    delete.main(args, datacite_settings)

def get_config(path):
    with open(path) as json_data_file:
        settings = json.load(json_data_file)
    return settings

def get_datacite_settings(args):
    datacite_params = get_config(args['config'])
    if args['live']:
        datacite_settings = datacite_params['datacite_live']
    else:
        datacite_settings = datacite_params['datacite_test']
    return datacite_settings


def main():
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
