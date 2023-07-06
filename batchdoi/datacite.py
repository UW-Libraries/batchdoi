import urllib.parse
import json
import requests

class DataciteService():
    HEADERS = {'Content-Type': 'application/vnd.api+json'}
    
    def __init__(self, settings):
        self.auth = (settings['username'], settings['password'])
        self.url = settings['url']
        self.prefix = settings['doi_prefix']

    def add_doi(self, payload):
        return requests.post(
            self.url,
            headers=self.HEADERS,
            auth=self.auth,
            data=json.dumps(payload)
        )

    def get_doi(self, suffix):
        doi_name = '%s/%s' % (self.prefix, suffix)
        url = '{}/{}'.format(self.url, urllib.parse.quote_plus(doi_name))
        return requests.get(
            url,
            headers=self.HEADERS,
        )

    def update_doi(self, doi_name, payload):
        url = '{}/{}'.format(self.url, urllib.parse.quote_plus(doi_name))
        return requests.put(
            url,
            headers=self.HEADERS,
            auth=self.auth,
            data=json.dumps(payload)
        )

    def delete_doi(self, doi):
        url = '{}/{}'.format(self.url, urllib.parse.quote_plus(doi))
        return requests.delete(
            url,
            headers=self.HEADERS,
            auth=self.auth,
        )


