# Bulk DOI Utilities
Scripts for use in creating and managing bulk DOI requests.

## Background

These scripts were created in response to a request from Jen Muilenberg. She wanted to give individuals a means to submit DOI requests in a batch rather than one-by-one through the libraries' DOI request web page.

The requester enters the data into a spreadsheet that we provide them with all of the necessary fields. We then export the data to CSV file and use it as input to the create.py script as described below.

## Getting Started

### Prerequisites

You will need Python 3.x and the requests library to run these scripts.  

### Installing

1. Clone the respository

    git clone https://github.com/UW-Libraries/bulkdoi.git  
    cd bulkdoi  

2. Create a config.json file.

    Copy the config.json.template file to config.json. Edit config.json adding a values for username and password items for both datacite_test and datacite_live sections.  

### Example usage

```python3 create.py --config <config.json file> <requests-file> > <doi-file>```   

*requests-file* is CSV file with DOI request data. See the **requests-example.csv** file for format. Refer to guide below for more detailed information about the fields for the requests data.

This script will create DOIs on the test Datacite system. DOIs can be viewed on our [test Fabrica account](https://doi.test.datacite.org/repositories/orbis.uwl).

```python3 delete.py --config <config.json file> <doi-file>```

This command will delete DOIs on Datacite. The DOIs to delete are listed in *doi-file*. This file should contain one DOI per line.

```python3 publish.py --config <config.json file> <doi-file>```

This command will make specified DOIs available for search. Note that DOIs that are published can no longer be deleted.

## Request CSV fields

All fields are required to have values unless otherwise noted.

### URL

The location of the landing page with more information about the resource. 

Should start with https://
http:// and ftp:// are also supported.

### Creators

The main researchers involved in producing the data, or the authors of the publication, in priority order, separated by semicolons.

Please enter each personal name in 'Last name, First name' format.

Example:

    Brown, J.M.; Smith, Alice

If the name is an organization, enclose it in square brackets

Example:

    [University of Washington]

### Publisher

The name of the entity that holds, archives, publishes prints, distributes, releases, issues, or produces the resource.

### Publication Year

The year when the resource was or will be made publicly available. No earlier than 1450 and no later than 1 year in the future.

### Description

All additional information that does not fit in any of the other categories.

*Optional but recommended*

