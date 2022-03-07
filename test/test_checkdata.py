import unittest
import bulkdoi.checkdata as checkdata


class TestCheckHeader(unittest.TestCase):
    def test_good_header(self):
        header = ['URL', 'Creators', 'Title', 'Publisher', 'Publication Year', 'Resource Type', 'Description']
        is_ok, msg = checkdata.checkheader(header)
        self.assertTrue(is_ok)

    def test_empty_header(self):
        header = ['URLx', 'Creators', 'Title', 'Publisher', 'Publication Year', 'Resource Type', 'Description']
        header = []
        is_ok, msg = checkdata.checkheader(header)
        self.assertFalse(is_ok)

    def test_bad_field_name(self):
        header = ['URL', 'Creators', 'XXX', 'Publisher', 'Publication Year', 'Resource Type', 'Description']
        is_ok, msg = checkdata.checkheader(header)
        self.assertFalse(is_ok)

    def test_case_insensitive(self):
        header = ['url', 'creators', 'title', 'publisher', 'publication year', 'resource Type', 'description']
        is_ok, msg = checkdata.checkheader(header)
        self.assertTrue(is_ok)

class TestUrlIsMalformed(unittest.TestCase):
    def test_http_accepted(self):
        response = checkdata.url_is_malformed('http://example.com')
        self.assertIsNone(response)

    def test_https_accepted(self):
        response = checkdata.url_is_malformed('https://example.com')
        self.assertIsNone(response)

    def test_ftp_accepted(self):
        response = checkdata.url_is_malformed('ftp://example.com')
        self.assertIsNone(response)

    def test_empty_rejected(self):
        response = checkdata.url_is_malformed('')
        self.assertIsNotNone(response)

    def test_bad_protocol_rejected(self):
        response = checkdata.url_is_malformed('feed://example.com/rss.xml')
        self.assertIsNotNone(response)

class TestCreatorsIsMalformed(unittest.TestCase):
    def test_normal_organization(self):
        response = checkdata.creators_is_malformed('[Some Organization]')
        self.assertIsNone(response)

    def test_normal_single_name(self):
        response = checkdata.creators_is_malformed('Madonna')
        self.assertIsNone(response)

    def test_normal_double_name(self):
        response = checkdata.creators_is_malformed('Smith, Joe')
        self.assertIsNone(response)

    def test_multiple_items(self):
        response = checkdata.creators_is_malformed('[Some Organization];Smith, Joe')
        self.assertIsNone(response)

    def test_empty_rejected(self):
        response = checkdata.creators_is_malformed('')
        self.assertIsNotNone(response)

    def test_extra_left_bracket(self):
        response = checkdata.creators_is_malformed('[[Some Organization]')
        self.assertIsNotNone(response)

    def test_double_brackets(self):
        response = checkdata.creators_is_malformed('[First][Second]')
        self.assertIsNotNone(response)

    def test_multiple_commas(self):
        response = checkdata.creators_is_malformed('Brown, Alice, Mary')
        self.assertIsNotNone(response)

    def test_name_with_embedded_left_bracket(self):
        response = checkdata.creators_is_malformed('Brown, Al[ice')
        self.assertIsNotNone(response)

    def test_name_with_embedded_right_bracket(self):
        response = checkdata.creators_is_malformed('Brown], Alice')
        self.assertIsNotNone(response)

class TestTitleIsMalformed(unittest.TestCase):
    def test_normal(self):
        response = checkdata.title_is_malformed('This is a title')
        self.assertIsNone(response)

    def test_empty_rejected(self):
        response = checkdata.title_is_malformed('')
        self.assertIsNotNone(response)

class TestPublisherIsMalformed(unittest.TestCase):
    def test_normal(self):
        response = checkdata.publisher_is_malformed('This is a publisher')
        self.assertIsNone(response)

    def test_empty_rejected(self):
        response = checkdata.publisher_is_malformed('')
        self.assertIsNotNone(response)

class TestPubyearIsMalformed(unittest.TestCase):
    def test_normal(self):
        response = checkdata.pubyear_is_malformed(1999)
        self.assertIsNone(response)

    def test_float(self):
        response = checkdata.pubyear_is_malformed(1999.0)
        self.assertIsNone(response)

    def test_low_number_rejected(self):
        response = checkdata.pubyear_is_malformed(0)
        self.assertIsNotNone(response)

    def test_string_rejected(self):
        response = checkdata.pubyear_is_malformed('')
        self.assertIsNotNone(response)

class TestRestypeIsMalformed(unittest.TestCase):
    def test_normal(self):
        accepted_values = [
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
        ]
        for item in accepted_values:
            response = checkdata.restype_is_malformed(item)
            self.assertIsNone(response)

    def test_not_in_list_rejected(self):
        response = checkdata.restype_is_malformed('SomeWeirdValue')
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
