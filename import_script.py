from formula1.report import parse_log_files, load_abbreviations, build_report
import argparse
import os
from database.common.models import *
from rest_api_formula1_report import app


parser = argparse.ArgumentParser(description="Import data from files to database.")
parser.add_argument('--db-path', type=str, help='Path to the database.', required=True)
parser.add_argument('--data-folder', type=str, help='Path to the folder with files.', required=True)
args = parser.parse_args()


def get_report():
    start_data = parse_log_files(os.path.abspath(os.path.join('.', args.data_folder)), 'start.log')
    end_data = parse_log_files(os.path.abspath(os.path.join('.', args.data_folder)), "end.log")
    abbreviations = load_abbreviations(os.path.abspath(os.path.join('.', args.data_folder)), "abbreviations.txt")
    report = build_report(start_data, end_data, abbreviations)
    return report


def import_data_from_files():
    report = get_report()
    for v in report.values():
        existing_racer = Racers.select().where(Racers.abbreviation == v["Abbreviation"]).first()

        if not existing_racer:
            racer = Racers.create(abbreviation=v["Abbreviation"],
                                  driver_name=v["Driver Name"],
                                  team=v["Team"])
        else:
            racer = existing_racer

        if racer:
            existing_race_result = RaceResults.select().where(RaceResults.racer_id == racer.id).first()

            if not existing_race_result:
                race_result = RaceResults.create(
                    racer_id=racer.id,
                    start_time=v["Start time"],
                    end_time=v["End time"],
                    best_lap_time=v["Best Lap Time"]
                )


if app.config['DEBUG']:
    database = SqliteDatabase(os.path.join(args.db_path, 'local_formula1.db'))
elif app.config['TESTING']:
    database = SqliteDatabase(':memory:')
else:
    database = SqliteDatabase(os.path.join(args.db_path, 'production_formula1.db'))
database_proxy.initialize(database)


if __name__ == "__main__":
    database_proxy.connect()
    database_proxy.create_tables([Racers, RaceResults], safe=True)
    import_data_from_files()
