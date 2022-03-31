import unittest
import bulkdoi.services as services
from unittest.mock import Mock


class TestDOIService(unittest.TestCase):
    def test_submit_doi_normal_response(self):
        response = Mock()
        response.status_code = 201
        external_service = Mock(spec=['add_doi'])
        external_service.add_doi.return_value = response

        service_data_creator = Mock(spec=['create_payload'])
        service_data_creator.return_value = {'data': {'id': 'DOINAME'}}

        expected = 'DOINAME'
        doi_service = services.DOIService(external_service, service_data_creator, ['FOO'])
        response = doi_service.submit_doi({}, True)
        self.assertEqual(response, expected)

    def test_submit_doi_bad_response(self):
        response = Mock()
        response.status_code = 404
        external_service = Mock(spec=['add_doi'])
        external_service.add_doi.return_value = response
        service_data_creator = Mock(spec=['create_payload'])
        expected = 'ERROR'
        doi_service = services.DOIService(external_service, service_data_creator, ['FOO'])
        response = doi_service.submit_doi({}, True)
        self.assertEqual(response, expected)

    def test_publish_doi_normal_response(self):
        response = Mock()
        response.status_code = 201
        external_service = Mock(spec=['update_doi'])
        external_service.update_doi.return_value = response
        doi_service = services.DOIService(external_service, Mock(), Mock())
        response = doi_service.publish_doi('')
        expected = True
        self.assertEqual(response, expected)

    def test_publish_doi_bad_response(self):
        response = Mock()
        response.status_code = 404
        external_service = Mock(spec=['update_doi'])
        external_service.update_doi.return_value = response
        doi_service = services.DOIService(external_service, Mock(), Mock())
        response = doi_service.publish_doi('')
        expected = False
        self.assertEqual(response, expected)

    def test_delete_doi_normal_response(self):
        response = Mock()
        response.status_code = 201
        external_service = Mock(spec=['delete_doi'])
        external_service.delete_doi.return_value = response
        doi_service = services.DOIService(external_service, Mock(), Mock())
        response = doi_service.delete_doi('')
        expected = True
        self.assertEqual(response, expected)

    def test_delete_doi_bad_response(self):
        response = Mock()
        response.status_code = 404
        external_service = Mock(spec=['delete_doi'])
        external_service.delete_doi.return_value = response
        doi_service = services.DOIService(external_service, Mock(), Mock())
        response = doi_service.delete_doi('')
        expected = False
        self.assertEqual(response, expected)


class TestNameGenerator(unittest.TestCase):
    def test_generate_doi_name(self):
        response = Mock()
        response.status_code = 404
        external_service = Mock(spec=['get_doi'])
        external_service.get_doi.return_value = response
        external_service.prefix = 'FOO'
        suffix_generator = (suffix for suffix in [123])

        doi_name_generator = services.DOINameGenerator(external_service, suffix_generator)
        response = next(doi_name_generator.doi_names())
        expected = 'FOO/123' 
        self.assertEqual(response, expected)

    def test_generate_doi_name_first_taken(self):
        response1 = Mock()
        response2 = Mock()
        response1.status_code = 201
        response2.status_code = 404
        responses = [response1, response2]
        external_service = Mock(spec=['get_doi'])
        external_service.get_doi.side_effect = responses
        external_service.prefix = 'FOO'
        suffix_generator = (suffix for suffix in ['123', '456'])

        doi_name_generator = services.DOINameGenerator(external_service, suffix_generator)
        response = next(doi_name_generator.doi_names())
        expected = 'FOO/456' 
        self.assertEqual(response, expected)


if __name__ == '__main__':
    unittest.main()
