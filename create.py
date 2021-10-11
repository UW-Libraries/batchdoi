#!/usr/bin/env python3
# coding: utf8

'''Foo  
'''

import sys
import argparse
import logging
import json
import csv
import random
import string
import datacite

LOGGER = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)

def get_args():
    '''Get command line arguments as well as configuration settings'''
    parser_desc = 'Process a batch of DOI requests.'
    parser = argparse.ArgumentParser(description=parser_desc)
    parser.add_argument("requests", help="CSV formatted file of DOI requests")
    parser.add_argument("-c", "--config", help="Config file path (defaults to './config.json')", default='config.json')
    #parser.add_argument('-v', '--verbose', action='store_true', help="Show detailed output")
    parser.add_argument('-s', '--submit', action='store_true', help="Submit DOI data to Datacite")
    parser.add_argument('-l', '--live', action='store_true', help="Create DOIs on the live system instead of the test system")
    parser.add_argument('-p', '--publish', action='store_true', help="Publish DOIs in addition to creating them. Note that published DOIs cannot be deleted.")
    args = vars(parser.parse_args())
    return args

def make_form_data(csvdata):
    form_data = {}
    form_data['url'] = csvdata['URL']
    form_data['creators'] = csvdata['Creators']
    form_data['title'] = csvdata['Title']
    form_data['publisher'] = csvdata['Publisher']
    form_data['publication_year'] = csvdata['Publication Year']
    form_data['resource_type'] = csvdata['Resource Type']
    form_data['description'] = csvdata['Description']
    return form_data

class DOIService():
    def __init__(self, external_service, gen_suffix):
        self.external_service = external_service
        self.gen_suffix = gen_suffix

    def submit_doi(self, payload):
        response = self.external_service.add_doi(payload)
        status_code = response.status_code
        if status_code == 201:
            LOGGER.debug('DOI submitted:' + payload['data']['id'])
        else:
            LOGGER.error('Bad response from Datacite: %s' % response.text)
            return 'ERROR'
        return payload['data']['id']

    def doi_exists(self, doi):
        response = self.external_service.get_doi(doi)
        status_code = response.status_code
        return status_code != 404

    def generate_doi_name(self):
        for suffix in self.gen_suffix():
            doi = '%s/%s' % (self.external_service.prefix, suffix)
            if not self.doi_exists(doi):
                return doi

def gen_data(infile):
    with open(infile) as csvfile:
        reader = csv.DictReader(csvfile)
        for r in reader:
            yield r

def gen_doi_names(doi_service):
    while True:
        yield doi_service.generate_doi_name()

def gen_form_data(data):
    for d in data:
        yield make_form_data(d)

def gen_payloads(form_data, doi_names):
    for (fd, dn) in zip(form_data, doi_names):
        yield datacite.create_payload(fd, dn)

def process_payloads(doi_service, submit, payloads):
    for p in payloads:
        if submit:
            doi = doi_service.submit_doi(p)
            #assert doi_service.doi_exists(doi)
            yield doi
        else:
            yield json.dumps(p)

def get_config(path):
    with open(path) as json_data_file:
        settings = json.load(json_data_file)
    return settings

def gen_suffix():
    chars = string.ascii_lowercase + string.digits
    while True:
        yield ''.join([random.choice(chars) for _ in range(8)])

def main():
    args = get_args()
    datacite_params = get_config(args['config'])
    datacite_adapter = datacite.DataciteService(datacite_params, use_live=args['live'])
    doi_service = DOIService(datacite_adapter, gen_suffix)
    doi_names = gen_doi_names(doi_service)
    data = gen_data(args['requests'])
    form_data = gen_form_data(data)
    payloads = gen_payloads(form_data, doi_names)
    for item in process_payloads(doi_service, args['submit'], payloads):
        print(item)

if __name__ == "__main__":
    sys.exit(main())

