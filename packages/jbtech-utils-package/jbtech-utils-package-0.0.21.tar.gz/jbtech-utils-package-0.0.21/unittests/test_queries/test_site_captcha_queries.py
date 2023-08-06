""" Unit tests for site captcha results queries """
from utils_package.data_controller.scripts.captcha_cookie.site_captcha_results_queries \
    import SiteCaptchaResultsWriter, SiteCaptchaResultsReader
from unittest import TestCase
from datetime import datetime, timedelta


class TestSiteCaptchaQueries(TestCase):
    """ Unit tests for site captcha queries """

    def setUp(self):
        """ Set up class variables """
        self.captcha_queries_writer = SiteCaptchaResultsWriter()
        self.captcha_queries_reader = SiteCaptchaResultsReader()

    def test_site_captcha_new_record(self):
        """ Validates that a record can be inserted into the site captcha cookie table
        1. Generate test data
        2. Generate new record in the database
        3. Validate response
        """
        # 1. Generate test data
        cookie_content = {
                'expiration_date': datetime.now() + timedelta(days=1),
                'score': '0.9',
                'human_prob': '0.95'
            }
        record_dict = {
            'ipaddress': '192.168.1.251',
            'score': '0.9',
            'cookie_content': str(cookie_content)
        }

        # 2. Generate new record in the database
        response = self.captcha_queries_writer.insert_new_record(record_dict)
        self.assertIsNotNone(response)

        # 3. Validate response
        self.assertEqual(1, response[0])

    def test_get_captcha_record(self):
        """ Validates that a record can be read from the database after being created
        1. Generate test data
        2. Generate new record in the database
        3. Validate response
        4. Create request to get the newly created data
        5. Validate response
        """
        # 1. Generate test data
        cookie_content = {
                'expiration_date': datetime.now() + timedelta(days=1),
                'score': '0.9',
                'human_prob': '0.95'
            }
        record_dict = {
            'ipaddress': '192.168.1.251',
            'score': '0.9',
            'cookie_content': str(cookie_content)
        }

        # 2. Generate new record in the database
        response = self.captcha_queries_writer.insert_new_record(record_dict)
        self.assertIsNotNone(response)

        # 3. Validate response
        self.assertEqual(1, response[0])

        # 4. Create request to get the newly created data
        response = self.captcha_queries_reader.get_record_for_ip_address(record_dict['ipaddress'])

        # 5. Validate response
        self.assertGreaterEqual(response[0], 1)
        self.assertEqual(record_dict['ipaddress'], response[1][0]['ipaddress'])
