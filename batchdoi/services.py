#!/usr/bin/env python3
# coding: utf8

import urllib.parse
import logging
import random
from . import dcdata
from . import datacite


LOGGER = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)


class DOIService():
    def __init__(self, settings, api=None, data=None):
        self.api = api or datacite
        self.data = data or dcdata
        self.auth = (settings['username'], settings['password'])
        self.url = settings['url']
        self.prefix = settings['doi_prefix']
    
    def submit_doi(self, request, submit=False, names=None):
        names = names or ('%s/%s' % (self.prefix, suffix) for suffix in gen_suffix())
        if not submit:
            return request
        for name in names:
            if not self.doi_exists(name):
                break
        payload = self.data.make_create_payload(request, name)
        response = self.api.add_doi(self.auth, self.url, payload)
        if response.status_code == 201:
            LOGGER.debug('DOI submitted:' + payload['data']['id'])
        else:
            LOGGER.error('Bad response from Datacite: %s' % response.text)
            return 'ERROR'
        return payload['data']['id']
    
    def publish_doi(self, doi_name):
        url = '{}/{}'.format(self.url, urllib.parse.quote_plus(doi_name))
        payload = dcdata.make_publish_payload()
        response = self.api.update_doi(self.auth, url, payload)
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
        url = '{}/{}'.format(self.url, urllib.parse.quote_plus(doi_name))
        response = self.api.delete_doi(self.auth, url)
        if response.status_code == 201:
            LOGGER.debug('DOI deleted:' + doi_name)
        elif response.status_code == 404:
            LOGGER.error('Bad response from Datacite: %s' % response.status_code)
            return False
        return True
    
    def doi_exists(self, doi_name):
        url = '{}/{}'.format(self.url, urllib.parse.quote_plus(doi_name))
        response = self.api.get_doi(url)
        status_code = response.status_code
        return status_code != 404
    

# def gen_names(prefix):
#     while True:
#         yield '%s/%s' % (prefix, next(gen_suffix()))


def gen_suffix():
    chars = '0123456789bcdfghjkmnpqrstvwxyz' # alphanum without vowels and l
    while True:
        yield ''.join([random.choice(chars) for _ in range(8)])

# class DOINameGenerator():
#     def __init__(self, external_service, gen_suffix):
#         self.external_service = external_service
#         self.gen_suffix = gen_suffix

#     def doi_names(self):
#         for suffix in self.gen_suffix:
#             doi = '%s/%s' % (self.external_service.prefix, suffix)
#             if not self.doi_exists(doi):
#                 yield doi

#     def doi_exists(self, doi):
#         response = self.external_service.get_doi(doi)
#         status_code = response.status_code
#         return status_code != 404


