import sys
import re
import bulkdoi.getdata as getdata


def checkheader(header):
    errors = []
    expected_header = ['URL', 'Creators', 'Title', 'Publisher', 'Publication Year', 'Resource Type', 'Description']
    if len(header) != len(expected_header):
        errors.append('Data file header has wrong number of columns')
    for i, j in zip(header, expected_header):
        if i.lower() != j.lower():
            errors.append('Data file header has unrecognized column: {}'.format(i))
    if errors:
        return [(1, errors)]
    else:
        return []


def checkdata(data):
    errors = []
    for idx, row in enumerate(data):
        rowerrors = checkrow(row)
        if rowerrors:
            errors.append((idx+2, rowerrors))
    return errors


def checkrow(row):
    errors = []
    errors.append(url_is_malformed(row['url']))
    errors.append(creators_is_malformed(row['creators']))
    errors.append(title_is_malformed(row['title']))
    errors.append(publisher_is_malformed(row['publisher']))
    errors.append(pubyear_is_malformed(row['publication_year']))
    errors.append(restype_is_malformed(row['resource_type']))
    return [i for i in errors if i]


def url_is_malformed(url):
    expected_form = url.startswith('https://') or url.startswith('http://') or url.startswith('ftp://')
    if expected_form:
        return None
    return 'URL field is malformed'


def creators_is_malformed(creators):
    if not len(creators.strip()):
        return 'Creators field is empty'
    for name in [item.strip() for item in creators.split(';')]:
        if name.startswith('['):
            if not re.fullmatch('^\[[^\[\]]+\]$', name):
                return 'Creators field has an organization with mismatched brackets'
        else:
            if '[' in name[1:]:
                return 'Creators field has a name with an embedded ['
            if ']' in name[:-1]:
                return 'Creators field has a name with an embedded ]'
            names = [n.strip() for n in name.split(',')]
            if len(names) == 0:
                return 'Creators field has an empty name'
            if len(names) > 2:
                return 'Creators field has a name with multiple commas'


def title_is_malformed(title):
    if len(title.strip()):
        return None
    return 'Title field is empty'


def publisher_is_malformed(publisher):
    if len(publisher.strip()):
        return None
    return 'Publisher field is empty'


def pubyear_is_malformed(pubyear):
    try:
        pubyear_int = int(pubyear)
    except:
        return 'Publication Year field must be an integer'
    if pubyear_int > 1900:
        return None
    return 'Publication Year field is malformed'


def restype_is_malformed(restype):
    accepted = set([
        'Audiovisual',
        'Collection',
        'DataPaper',
        'Dataset',
        'Event',
        'Image',
        'InteractiveResource',
        'Model',
        'PhysicalObject',
        'Service',
        'Software',
        'Sound',
        'Text',
        'Workflow'
    ])
    if restype.strip() in accepted:
        return None
    return 'Resource Type field must be one of the choices in list'


def main(argv=None):
    if argv is None:
        argv = sys.argv
    datafile = argv[1]
    header = getdata.extract_header(datafile)
    print(checkheader(header))
    data = getdata.extract_data(datafile)
    print(checkdata(data))


if __name__ == "__main__":
    sys.exit(main())