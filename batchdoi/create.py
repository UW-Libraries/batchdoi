#!/usr/bin/env python3
# coding: utf8

'''Given DOI data as input, create DOIs via web service
'''

import sys
import logging
import csv
from . import services


LOGGER = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)


def main(args, datacite_settings):
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


if __name__ == "__main__":
    sys.exit(main())

