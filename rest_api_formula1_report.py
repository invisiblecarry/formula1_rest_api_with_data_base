import os
import json
import xml.etree.ElementTree as ET
from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import Swagger
from formula1.report import parse_log_files, load_abbreviations, build_report
from database.core import crud
from database import core

app = Flask(__name__)
app.config['DATA_FOLDER'] = os.path.join('', 'data')
api = Api(app)
swagger = Swagger(app)


def get_report():
    start_data = parse_log_files(app.config['DATA_FOLDER'], "start.log")
    end_data = parse_log_files(app.config['DATA_FOLDER'], "end.log")
    abbreviations = load_abbreviations(app.config['DATA_FOLDER'], "abbreviations.txt")
    report = build_report(start_data, end_data, abbreviations)
    return report


class ReportResource(Resource):

    def get(self, version):
        """
        This is the GET endpoint for the report.
        ---
        parameters:
          - name: format
            in: query
            type: string
            description: The format of the report (json or xml)
            required: true
        responses:
          200:
            description: Successful response
        """
        report = get_report()
        data_format = request.args.get('format', 'json')
        if data_format == 'json':
            response_data = json.dumps(report)
            return response_data, 200
        elif data_format == 'xml':
            root = ET.Element("report")
            for driver_id, info in report.items():
                driver = ET.SubElement(root, "driver")
                ET.SubElement(driver, "DriverName").text = info['Driver Name']
                ET.SubElement(driver, "Team").text = info['Team']
                ET.SubElement(driver, "StartTime").text = info['Start time']
                ET.SubElement(driver, "EndTime").text = info['End time']
                ET.SubElement(driver, "BestLapTime").text = info['Best Lap Time']
                ET.SubElement(driver, "Abbreviation").text = info['Abbreviation']
            xml_response = ET.tostring(root, encoding="utf-8").decode('utf-8')
            return xml_response, 200
        else:
            return "Invalid format. Use 'json' or 'xml'.", 400


api.add_resource(ReportResource, '/api/<string:version>/report/')

if __name__ == '__main__':
    app.run(debug=True)
