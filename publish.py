import sys
import logging
import urllib.parse

import settings
import datacite

logger = logging.getLogger(__name__)

#TEST_PARAMS = settings.DATACITE_TEST
PARAMS = settings.DATACITE_LIVE

def _auth():
    return {
        'username': PARAMS['username'],
        'password': PARAMS['password'],
    }

def publish_doi(doi):
    url = '{}/{}'.format(PARAMS['url'], urllib.parse.quote_plus(doi))
    payload = {"data": {"attributes": {"event": "publish"}}}
    response = datacite.update_doi(url, _auth(), payload)
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
