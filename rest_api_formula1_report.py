import os
import json
import xml.etree.ElementTree as ET
from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import Swagger
from database.common.models import *
import datetime

app = Flask(__name__)
app.config['DATA_FOLDER'] = os.path.abspath(os.path.join('', 'data'))
app.config['DATABASE'] = os.path.abspath(os.path.join('database', 'formula1_report.db'))
api = Api(app)
swagger = Swagger(app)


def convert_data_to_str(data: list) -> list:
    for item in data:
        item['start_time'] = str(item['start_time'])
        item['end_time'] = str(item['end_time'])
        item['best_lap_time'] = str(item['best_lap_time'])

    return data


def init_database():
    database = SqliteDatabase(app.config['DATABASE'])
    database_proxy.initialize(database)


def get_data_from_database():
    init_database()
    try:
        database_proxy.connect()
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
        print(result)
        return result

    except Exception as ex:
        print(ex)
        return None


class ReportResource(Resource):

    def get(self, version):
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


api.add_resource(ReportResource, '/api/<string:version>/report/')

if __name__ == '__main__':
    app.run(debug=True)