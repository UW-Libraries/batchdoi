# cURL test request for creating and deleting a DOI on Datacite

# Create minimal DOI on Datacite test site
curl --request POST \
     --url https://api.test.datacite.org/dois \
     --header 'Content-Type: application/vnd.api+json' \
     --user "$DCUSER:$DCPW" \
     --data '
{
  "data": {
    "type": "dois",
    "attributes": {
      "doi": "10.70027/foo"
    }
  }
}
'

# Delete DOI from Datacite test site
curl --request DELETE \
     --user "$DCUSER:$DCPW" \
     --url https://api.test.datacite.org/dois/10.70027/foo
