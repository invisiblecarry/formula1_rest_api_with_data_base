import unittest
import os
import json
import xml.etree.ElementTree as ET
from rest_api_formula1_report import create_app
from database.common.models import *


test_config = {
    "SECRET_KEY": 'dev',
    "TESTING": True,
    "DEBUG": False
}


class TestYourFlaskApp(unittest.TestCase):

    def setUp(self):
        app = create_app(test_config=test_config)
        self.app = app.test_client()

    def test_get_report_json(self):
        pass
        # response = self.app.get('/api/v1/report/?format=json')
        # self.assertEqual(response.status_code, 200)
        # data = json.loads(response.text)
        # self.assertIn("driver_name", data)
        # self.assertIn("team", data)
        # self.assertIn("start_time", data)
        # self.assertIn("end_time", data)
        # self.assertIn("best_lap_time", data)
        # self.assertIn("abbreviation", data)

    def test_get_report_xml(self):
        pass
        # response = self.app.get('/api/v1/report/?format=xml')
        # self.assertEqual(response.status_code, 200)
        # data = response.data.decode('utf-8')
        # self.assertIn("driver_name", data)
        # self.assertIn("team", data)
        # self.assertIn("start_time", data)
        # self.assertIn("end_time", data)
        # self.assertIn("best_lap_time", data)
        # self.assertIn("abbreviation", data)

    def test_invalid_format(self):
        response = self.app.get('/api/v1/report/?format=invalid_format')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
