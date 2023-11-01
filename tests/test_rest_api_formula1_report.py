import unittest
import os
from rest_api_formula1_report import app
import json
import xml.etree.ElementTree as ET

app.config['DATA_FOLDER'] = os.path.join('..', 'data')


class TestYourFlaskApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def test_get_report_json(self):
        response = self.app.get('/api/v1/report/?format=json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertIn("Driver Name", data)
        self.assertIn("Team", data)
        self.assertIn("Start time", data)
        self.assertIn("End time", data)
        self.assertIn("Best Lap Time", data)
        self.assertIn("Abbreviation", data)

    def test_get_report_xml(self):
        response = self.app.get('/api/v1/report/?format=xml')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode('utf-8')
        self.assertIn("DriverName", data)
        self.assertIn("Team", data)
        self.assertIn("StartTime", data)
        self.assertIn("EndTime", data)
        self.assertIn("BestLapTime", data)
        self.assertIn("Abbreviation", data)

    def test_invalid_format(self):
        response = self.app.get('/api/v1/report/?format=invalid_format')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
