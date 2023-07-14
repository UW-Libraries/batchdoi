#!/usr/bin/env python3
# coding: utf8

'''Publish DOIs given input file with DOI names
'''
import sys
import logging
from . import services


logger = logging.getLogger(__name__)


def main(args, datacite_settings):
    doi_service = services.DOIService(datacite_settings)
    infile = args.doifile
    with open(infile) as fh:
        for line in fh:
            doi_name = line.strip()
            doi_service.publish_doi(doi_name)


if __name__ == "__main__":
    sys.exit(main())