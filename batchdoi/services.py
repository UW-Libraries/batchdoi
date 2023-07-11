#!/usr/bin/env python3
# coding: utf8


import logging
import random
import dcdata


LOGGER = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)

def gen_suffix():
    chars = '0123456789bcdfghjkmnpqrstvwxyz' # alphanum without vowels and l
    while True:
        yield ''.join([random.choice(chars) for _ in range(8)])

class DOIService():
    def __init__(self, external_service):
        self.external_service = external_service
    
    def submit_doi(self, request, submit=False, names=None):
        names = names or DOINameGenerator(self.external_service, gen_suffix()).doi_names()
        if not submit:
            return request 
        payload = dcdata.make_create_payload(request, next(iter(self.doi_names)))
        response = self.external_service.add_doi(payload)
        if response.status_code == 201:
            LOGGER.debug('DOI submitted:' + payload['data']['id'])
        else:
            LOGGER.error('Bad response from Datacite: %s' % response.text)
            return 'ERROR'
        return payload['data']['id']
    
    def publish_doi(self, doi_name):
        payload = dcdata.make_publish_payload()
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


