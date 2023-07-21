import unittest
from collections import defaultdict
from unittest.mock import Mock
from batchdoi import gateway


class TestDOIService(unittest.TestCase):
    def test_submit_doi_normal_response(self):
        api = Mock()

        response = Mock()
        response.status_code = 201
        api.add_doi.return_value = response

        response = Mock()
        response.status_code = 404
        api.get_doi.return_value = response

        service_data_creator = Mock()
        service_data_creator.make_create_payload.return_value = {'data': {'id': 'DOINAME'}}

        settings = defaultdict(str)
        expected = 'DOINAME'
        doi_service = gateway.DOIService(settings, api, service_data_creator)
        response = doi_service.submit_doi(defaultdict(str), True)
        self.assertEqual(response, expected)

    def test_submit_doi_bad_response(self):
        api = Mock()

        response = Mock()
        response.status_code = 404
        api.add_doi.return_value = response

        response = Mock()
        response.status_code = 404
        api.get_doi.return_value = response

        service_data_creator = Mock()
        service_data_creator.make_create_payload.return_value = {'data': {'id': 'DOINAME'}}
        
        settings = defaultdict(str)
        expected = 'ERROR'
        doi_service = gateway.DOIService(settings, api, service_data_creator)
        response = doi_service.submit_doi({}, True)
        self.assertEqual(response, expected)

    def test_publish_doi_normal_response(self):
        api = Mock()

        response = Mock()
        response.status_code = 201
        api.update_doi.return_value = response

        settings = defaultdict(str)
        doi_service = gateway.DOIService(settings, api, Mock())
        response = doi_service.publish_doi('')
        expected = True
        self.assertEqual(response, expected)

    def test_publish_doi_bad_response(self):
        api = Mock()

        response = Mock()
        response.status_code = 404
        api.update_doi.return_value = response

        settings = defaultdict(str)
        doi_service = gateway.DOIService(settings, api, Mock())
        response = doi_service.publish_doi('')
        expected = False
        self.assertEqual(response, expected)

    def test_delete_doi_normal_response(self):
        api = Mock()
        response = Mock()
        response.status_code = 201
        api.delete_doi.return_value = response
        settings = defaultdict(str)
        doi_service = gateway.DOIService(settings, api, Mock())
        response = doi_service.delete_doi('')
        expected = True
        self.assertEqual(response, expected)

    def test_delete_doi_bad_response(self):
        api = Mock()
        response = Mock()
        response.status_code = 404
        api.delete_doi.return_value = response
        settings = defaultdict(str)
        doi_service = gateway.DOIService(settings, api, Mock())
        response = doi_service.delete_doi('')
        expected = False
        self.assertEqual(response, expected)


if __name__ == '__main__':
    unittest.main()
