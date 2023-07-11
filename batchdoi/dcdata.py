def make_create_payload(form_data, doiname):
    payload = {
        "data": {
            "id": doiname,
            "type": "dois",
            "attributes": make_attributes(form_data, doiname),
        }
    }
    return payload

def make_publish_payload():
    return {
        "data": {
            "attributes": {"event": "publish"},
        }
    }

def make_attributes(form_data, doiname):
    attributes = {
        'doi': doiname,
        'url': form_data['url'],
        'creators': [make_creator(item) for item in form_data['creators'].split(';')],
        'titles': [{'title': form_data['title']}],
        'publisher': form_data['publisher'],
        'publicationYear': form_data['publication_year'],
        'types': {'resourceTypeGeneral': form_data['resource_type']},
    }
    if 'description' in form_data:
        attributes['descriptions'] = [{'description': form_data['description']}]
    return attributes

def make_creator(name):
    assert(name)
    nametype, splitname = parse_name(name)
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

def parse_name(name):
    name = name.strip()
    nametype = 'Personal'
    if name[0] == '[':
        name = name[1:]
        nametype = 'Organizational'
    if name[-1] == ']':
        name = name[:-1]
        name = name.strip()
    if nametype == 'Personal':	
        splitname = [n.strip() for n in name.split(',')]
        assert len(splitname) <= 2
    else:
        splitname = [name]
    return nametype, splitname
