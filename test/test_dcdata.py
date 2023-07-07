import unittest
import batchdoi.dcdata as dcdata
from unittest.mock import patch


class TestCreatePayload(unittest.TestCase):
    def test_foo(self):
        expected = {
            "data": {
                "id": 'DOINAME',
                "type": "dois",
                "attributes": 'ATTRIBUTES',
            }
        }
        with patch('batchdoi.dcdata.make_attributes') as mock_make_attributes:
            mock_make_attributes.return_value = 'ATTRIBUTES'
            self.assertEqual(dcdata.create_payload(None, 'DOINAME'), expected)


class TestMakeAttributes(unittest.TestCase):
    def setUp(self):
        self.request_data = {
            'url': 'URL',
            'creators': 'CREATOR',
            'title': 'TITLE',
            'publisher': 'PUBLISHER',
            'publication_year': 'PUBLICATION_YEAR',
            'resource_type': 'RESOURCE_TYPE',            
        }

    def test_no_description(self):
        expected = {
            'doi': 'DOINAME',
            'url': 'URL',
            'creators': ['CREATOR'],
            'titles': [{'title': 'TITLE'}],
            'publisher': 'PUBLISHER',
            'publicationYear': 'PUBLICATION_YEAR',
            'types': {'resourceTypeGeneral': 'RESOURCE_TYPE'},
        }
        with patch('batchdoi.dcdata.make_creator') as mock_make_creator:
            mock_make_creator.return_value = 'CREATOR'
            response = dcdata.make_attributes(self.request_data, 'DOINAME')
            self.assertEqual(response, expected)

    def test_with_description(self):
        self.request_data['description'] = 'DESCRIPTION'
        expected = [{'description': 'DESCRIPTION'}]
        with patch('batchdoi.dcdata.make_creator') as mock_make_creator:
            mock_make_creator.return_value = 'CREATOR'
            response = dcdata.make_attributes(self.request_data, 'DOINAME')
            self.assertEqual(response['descriptions'], expected)

    def test_multiple_creators(self):
        self.request_data['creators'] = 'CREATOR1; CREATOR2'
        expected = ['CREATOR1', 'CREATOR2']
        with patch('batchdoi.dcdata.make_creator') as mock_make_creator:
            mock_make_creator.side_effect = ['CREATOR1', 'CREATOR2']
            response = dcdata.make_attributes(self.request_data, 'DOINAME')
            self.assertEqual(response['creators'], expected)


class TestMakeCreator(unittest.TestCase):
    def test_empty_name(self):
        with self.assertRaises(Exception):
            dcdata.make_creator('  ')

    def test_weird_nametype(self):
        expected = {'givenName': '', 'familyName': 'Smith', 'nameType': 'Personal'}
        with patch('batchdoi.dcdata.parse_name') as mock_parse_name:
            mock_parse_name.return_value = ('Weird', ['Smith'])
            with self.assertRaises(ValueError):
                self.assertEqual(dcdata.make_creator('x'), expected)

    def test_personal_single_name(self):
        expected = {'givenName': '', 'familyName': 'Smith', 'nameType': 'Personal'}
        with patch('batchdoi.dcdata.parse_name') as mock_parse_name:
            mock_parse_name.return_value = ('Personal', ['Smith'])
            self.assertEqual(dcdata.make_creator('x'), expected)

    def test_personal_full_name(self):
        expected = {'givenName': 'Robert M', 'familyName': 'Smith', 'nameType': 'Personal'}
        with patch('batchdoi.dcdata.parse_name') as mock_parse_name:
            mock_parse_name.return_value = ('Personal', ['Smith', 'Robert M'])
            self.assertEqual(dcdata.make_creator('x'), expected)

    def test_organizational_name(self):
        expected = {'name': 'University of Washington', 'nameType': 'Organizational'}
        with patch('batchdoi.dcdata.parse_name') as mock_parse_name:
            mock_parse_name.return_value = ('Organizational', ['University of Washington'])
            self.assertEqual(dcdata.make_creator('x'), expected)


class TestParseName(unittest.TestCase):
    def test_personal_name_split(self):
        #logger.info('Running test_add()')
        data = ' Smith , Robert M '
        expected = ['Smith', 'Robert M']
        _, splitname = dcdata.parse_name(data)
        self.assertEqual(splitname, expected)

    def test_org_name(self):
        data = ' [ University of Washington ] '
        expected = ['University of Washington']
        _, splitname = dcdata.parse_name(data)
        self.assertEqual(splitname, expected)

    def test_name_type_is_org(self):
        data = '[University of Washington]'
        expected = 'Organizational'
        nametype, _ = dcdata.parse_name(data)
        self.assertEqual(nametype, expected)

    def test_name_type_is_personal(self):
        data = 'Smith , Robert M '
        expected = 'Personal'
        nametype, _ = dcdata.parse_name(data)
        self.assertEqual(nametype, expected)

    def test_personal_name_multiple_commas(self):
        data = 'Smith , Robert, M '
        with self.assertRaises(Exception):
            dcdata.parse_name(data)


if __name__ == '__main__':
    unittest.main()
