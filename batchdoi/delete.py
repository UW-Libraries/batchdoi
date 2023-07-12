#!/usr/bin/env python3
# coding: utf8

'''Delete DOIs in input file
'''
import sys
import logging
import services


logger = logging.getLogger(__name__)


def main(args, datacite_settings):
    infile = args['doifile']
    doi_service = services.DOIService(datacite_settings)
    with open(infile) as fh:
        for line in fh:
            doi_name = line.strip()
            doi_service.delete_doi(doi_name)

if __name__ == "__main__":
    sys.exit(main())