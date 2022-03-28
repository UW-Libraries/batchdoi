#!/usr/bin/env python3
# coding: utf8

"""Foo
"""

import logging


LOGGER = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)


class DOIService():
    def __init__(self, external_service, service_data_creator, doi_names):
        self.external_service = external_service
        self.service_data_creator = service_data_creator
        self.doi_names = doi_names
    
    def submit_doi(self, request, submit=False):
        payload = self.service_data_creator(request, next(iter(self.doi_names)))
        if not submit:
            return payload
        #assert False
        response = self.external_service.add_doi(payload)
        if response.status_code == 201:
            LOGGER.debug('DOI submitted:' + payload['data']['id'])
        else:
            LOGGER.error('Bad response from Datacite: %s' % response.text)
            return 'ERROR'
        return payload['data']['id']
    
    def publish_doi(self, doi_name):
        payload = self.service_data_creator()
        response = self.external_service.update_doi(doi_name, payload)
        if response.status_code == 201:
            LOGGER.debug('DOI published:' + doi_name)
        elif response.status_code == 404:
            LOGGER.error('Bad response from Datacite: %s' % response.status_code)
            return False
        else:
            LOGGER.error('Bad response from Datacite: %s' % response.text)
            return 'ERROR'
        return True
    
    def delete_doi(self, doi_name):
        response = self.external_service.delete_doi(doi_name)
        if response.status_code == 201:
            LOGGER.debug('DOI deleted:' + doi_name)
        elif response.status_code == 404:
            LOGGER.error('Bad response from Datacite: %s' % response.status_code)
            return False
        return True

class DOINameGenerator():
    def __init__(self, external_service, gen_suffix):
        self.external_service = external_service
        self.gen_suffix = gen_suffix

    def doi_names(self):
        for suffix in self.gen_suffix:
            doi = '%s/%s' % (self.external_service.prefix, suffix)
            if not self.doi_exists(doi):
                yield doi

    def doi_exists(self, doi):
        response = self.external_service.get_doi(doi)
        status_code = response.status_code
        return status_code != 404

