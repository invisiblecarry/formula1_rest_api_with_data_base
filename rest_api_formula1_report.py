import errno
import os
import json
import xml.etree.ElementTree as ET
from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import Swagger
from database.common.models import *
import datetime


def create_app(test_config=None):
    """
    Creates and configures an instance of a Flask application.

    :param test_config: A dictionary of configuration parameters for testing.
    :return: A Flask application object.
    """
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='dev',
        TESTING=False,
        DEBUG=True

    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    if app.config['TESTING']:
        database = SqliteDatabase(':memory:')
    else:
        database = SqliteDatabase(os.path.abspath(os.path.join('database', 'formula1_report.db')))
    database_proxy.initialize(database)

    with app.app_context():
        database_proxy.connect()
        database_proxy.create_tables([Racers, RaceResults], safe=True)
        database_proxy.close()

    api = Api(app)
    swagger = Swagger(app)
    api.add_resource(ReportResource, '/api/<string:version>/report/')
    return app


def convert_data_to_str(data: list) -> list:
    """
    Converts datetime and time objects to string representation in data lists.
    :param data: A list of dictionaries containing data.
    :return: The same list of dictionaries with time objects converted to strings.
    """
    for item in data:
        item['start_time'] = str(item['start_time'])
        item['end_time'] = str(item['end_time'])
        item['best_lap_time'] = str(item['best_lap_time'])

    return data


def get_data_from_database():
    """
    Retrieves data from the database and converts it into a list of dictionaries.

    :return: A list of dictionaries with data from the database or None in case of an error.
    """
    try:
        with database_proxy.connection_context():
            query = (Racers
                     .select(Racers.abbreviation,
                             Racers.driver_name,
                             Racers.team,
                             RaceResults.start_time,
                             RaceResults.end_time,
                             RaceResults.best_lap_time)
                     .join(RaceResults, on=(Racers.id == RaceResults.racer_id))
                     .dicts())
            result = convert_data_to_str(list(query))
            return result

    except Exception as ex:
        print(ex)
        return None


class ReportResource(Resource):
    """
    An API resource for retrieving reports in JSON or XML formats.
    """

    def get(self, version) -> tuple:
        """
        Handles GET requests to retrieve reports. Supports JSON and XML formats.

        :param version: The version of the API.
        :return: A tuple where the first element is the response data (a JSON string or XML string),
                 and the second element is the HTTP status code (an integer).
        """
        data = get_data_from_database()
        if not data:
            raise TypeError('Can`t get data from database')
        data_format = request.args.get('format', 'json')
        if data_format == 'json':
            response_data = json.dumps(data)
            return response_data, 200
        elif data_format == 'xml':
            root = ET.Element("report")
            for driver_info in data:
                driver = ET.SubElement(root, "driver")
                ET.SubElement(driver, "DriverName").text = driver_info['driver_name']
                ET.SubElement(driver, "Team").text = driver_info['team']
                ET.SubElement(driver, "StartTime").text = driver_info['start_time']
                ET.SubElement(driver, "EndTime").text = driver_info['end_time']
                ET.SubElement(driver, "BestLapTime").text = driver_info['best_lap_time']
                ET.SubElement(driver, "Abbreviation").text = driver_info['abbreviation']
            xml_response = ET.tostring(root, encoding="utf-8").decode('utf-8')
            return xml_response, 200
        else:
            return "Invalid format. Use 'json' or 'xml'.", 400


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(debug=True)
