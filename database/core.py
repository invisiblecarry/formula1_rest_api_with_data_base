from database.utils.CRUD import CRUDInterface
from database.common.models import *
from formula1.report import parse_log_files, load_abbreviations, build_report
import os

path_to_data = os.path.abspath(os.path.join('.', 'data'))


def get_report():
    start_data = parse_log_files(path_to_data, "start.log")
    end_data = parse_log_files(path_to_data, "end.log")
    abbreviations = load_abbreviations(path_to_data, "abbreviations.txt")
    report = build_report(start_data, end_data, abbreviations)
    return report


def import_data_from_files():
    report = get_report()
    for v in report.values():
        existing_racer = Racers.select().where(Racers.abbreviation == v["Abbreviation"]).first()

        if not existing_racer:
            racer = CRUDInterface.create(Racers, abbreviation=v["Abbreviation"], driver_name=v['Driver Name'],
                                         team=v["Team"])
        else:
            racer = existing_racer

        if racer:
            existing_race_result = RaceResults.select().where(RaceResults.racer_id == racer.id).first()

            if not existing_race_result:
                race_result = CRUDInterface.create(
                    RaceResults,
                    racer_id=racer.id,
                    start_time=v['Start time'],
                    end_time=v['End time'],
                    best_lap_time=v['Best Lap Time']
                )


db.connect()
db.create_tables([Racers, RaceResults], safe=True)
import_data_from_files()
crud = CRUDInterface()
