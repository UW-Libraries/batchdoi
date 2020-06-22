import urllib.parse
import json
import requests

def create_payload(form_data, doiname):
    payload = {
        "data": {
            "id": doiname,
            "type": "dois",
            "attributes": _make_attributes(form_data, doiname),
        }
    }
    return payload

def _make_attributes(form_data, doiname):
    attributes = {
        'doi': doiname,
        'url': form_data['url'],
        'creators': [_make_creator(item) for item in form_data['creators'].split(';')],
        'titles': [{'title': form_data['title']}],
        'publisher': form_data['publisher'],
        'publicationYear': form_data['publication_year'],
        'types': {'resourceTypeGeneral': form_data['resource_type']},
    }
    if 'description' in form_data:
        attributes['descriptions'] = [{'description': form_data['description']}]
    return attributes

def _make_creator(name):
    name = name.strip()
    assert(name)
    nametype, splitname = _parse_name(name)
    if nametype == 'Personal':
        if len(splitname) >= 2:
            return {
                "givenName": splitname[1],
                "familyName": splitname[0],
                "nameType": nametype,
            }        
        else:
            return {
                "givenName": '',
                "familyName": splitname[0],
                "nameType": nametype,
            }
    elif nametype == 'Organizational':
        return {
            "name": splitname[0],
            "nameType": nametype,
        }        
    else:
        raise ValueError

def _parse_name(name):
    name = name.strip()
    nametype = 'Personal'
    if name[0] == '[':
        name = name[1:]
        nametype = 'Organizational'
    if name[-1] == ']':
        name = name[:-1]
    if nametype == 'Personal':
        splitname = [n.strip() for n in name.split(',')]
        assert len(splitname) <= 2
    else:
        splitname = [name]
    return nametype, splitname

class DataciteService():
    HEADERS = {'Content-Type': 'application/vnd.api+json'}
    
    def __init__(self, params, use_live=False):
        if use_live:
            assert False
            params = params['datacite_live']
        else:
            params = params['datacite_test']
        self.auth = (params['username'], params['password'])
        self.url = params['url']
        self.prefix = params['doi_prefix']

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

    def update_doi(self, payload):
        assert False
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

