"""DataCite API functions
"""

import json
import requests


HEADERS = {'Content-Type': 'application/vnd.api+json'}
    

def add_doi(auth, url, payload):
    return requests.post(
        url,
        headers=HEADERS,
        auth=auth,
        data=json.dumps(payload)
    )


def get_doi(url):
    return requests.get(
        url,
        headers=HEADERS,
    )


def update_doi(auth, url, payload):
    return requests.put(
        url,
        headers=HEADERS,
        auth=auth,
        data=json.dumps(payload)
    )


def delete_doi(auth, url):
    return requests.delete(
        url,
        headers=HEADERS,
        auth=auth,
    )