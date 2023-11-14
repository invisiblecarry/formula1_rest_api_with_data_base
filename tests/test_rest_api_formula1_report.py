import unittest
import os
import json
import xml.etree.ElementTree as ET
from rest_api_formula1_report import create_app
from database.common.models import *

test_config = {
    "SECRET_KEY": 'dev',
    "TESTING": True,
    "DEBUG": False,
    "PATH_TO_DATA": os.path.abspath(os.path.join('..', 'data')),
    "DATABASE": SqliteDatabase(':memory:')
}


class TestYourFlaskApp(unittest.TestCase):
    """
    TestYourFlaskApp contains a set of unit tests for the Flask application's
    API endpoints delivering Formula 1 reports in both JSON and XML formats.
    """

    def setUp(self):
        """
        Set up the Flask application for testing. It configures the app for
        testing and initializes the test client.
        """
        self.app = create_app(cfg=test_config)
        self.client = self.app.test_client()

    def test_get_report_json(self):
        """
        Test the '/api/v1/report/?format=json' endpoint to ensure it returns a
        status code of 200 and the response contains the correct keys for driver
        information in JSON format.
        """
        response = self.client.get('/api/v1/report/?format=json')
        self.assertEqual(response.status_code, 200)
        try:
            data = json.loads(response.text)
            self.assertIn("driver_name", data)
            self.assertIn("team", data)
            self.assertIn("start_time", data)
            self.assertIn("end_time", data)
            self.assertIn("best_lap_time", data)
            self.assertIn("abbreviation", data)
        except json.JSONDecodeError:
            print('JSON Decode Error')
            raise

    def test_get_report_xml(self):
        """
        Test the '/api/v1/report/?format=xml' endpoint to ensure it returns a
        status code of 200 and the response data can be successfully parsed as XML.
        Also verifies that the XML contains all the required elements.
        """
        response = self.client.get('/api/v1/report/?format=xml')
        self.assertEqual(response.status_code, 200)
        cleaned_data = response.data.decode('utf-8').strip()[1:-1]
        try:
            data = ET.fromstring(cleaned_data)
            self.assertTrue(data.find('.//driver') is not None)
            self.assertTrue(data.find('.//team') is not None)
            self.assertTrue(data.find('.//start_time') is not None)
            self.assertTrue(data.find('.//end_time') is not None)
            self.assertTrue(data.find('.//best_lap_time') is not None)
            self.assertTrue(data.find('.//abbreviation') is not None)

        except ET.ParseError:
            print('XML Parse Error')
            raise

    def test_invalid_format(self):
        """
        Test the API response to an invalid format request.
        """
        response = self.client.get('/api/v1/report/?format=invalid_format')
        self.assertEqual(response.status_code, 400)

    def TearDown(self):
        """
        Finalizes test by closing the database connection.
        """
        with self.app.app_context():
            database_proxy.close()


if __name__ == '__main__':
    unittest.main()
