import sys
import logging
import urllib.parse

import settings
import requests
import json

logger = logging.getLogger(__name__)

#TEST_PARAMS = settings.DATACITE_TEST
PARAMS = settings.DATACITE_LIVE
HEADERS = {'Content-Type': 'application/vnd.api+json'}

def _auth():
    return (PARAMS['username'], PARAMS['password'])


def update_doi(url, auth, payload):
    return requests.put(
        url,
        headers=HEADERS,
        auth=auth,
        data=json.dumps(payload)
    )


def publish_doi(doi):
    url = '{}/{}'.format(PARAMS['url'], urllib.parse.quote_plus(doi))
    payload = {"data": {"attributes": {"event": "publish"}}}
    response = update_doi(url, _auth(), payload)
    if response.status_code == 200:
        logger.debug('DOI:' + doi)
    else:
        logger.error('Bad response from Datacite: %s' % response.text)
        return False
    return True

def main(argv=None):
    if argv is None:
        argv = sys.argv
    if len(argv) == 1:
        inf = sys.stdin
    elif len(argv) == 2:
        inf = open(argv[1], 'r')
    for line in inf:
        publish_doi(line.strip())

if __name__ == "__main__":
    sys.exit(main())
