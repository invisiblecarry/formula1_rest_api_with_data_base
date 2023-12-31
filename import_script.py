from formula1.report import parse_log_files, load_abbreviations, build_report
import argparse
import os
from database.common.models import *
import datetime

parser = argparse.ArgumentParser(description="Import data from files to database.")
parser.add_argument('--db-path', type=str, help='Path to the database.', required=True)
parser.add_argument('--data-folder', type=str, help='Path to the folder with files.', required=True)


def get_report(path_to_data_folder) -> dict:
    start_data = parse_log_files(path_to_data_folder, 'start.log')
    end_data = parse_log_files(path_to_data_folder, "end.log")
    abbreviations = load_abbreviations(path_to_data_folder, "abbreviations.txt")
    report = build_report(start_data, end_data, abbreviations)
    return report


def import_data_from_files(db: SqliteDatabase, path: str) -> None:
    """
        Imports race data from files into the database.

        Parameters:
        - db: Database object with connect and create_tables methods.
        - path: String path to directory with race data files.

        This function initializes database connection, creates tables, and populates them with
        data parsed by `get_report` from the provided directory. It checks for existing entries
        of racers and race results to avoid duplicates before creating new records.
        If database is temporary than connection should be closed after using this func

        Note: `Racers` and `RaceResults` are pre-defined ORM models.
    """
    report = get_report(path)
    if not report:
        raise TypeError('Can`t get the report')
    database_proxy.initialize(db)
    database_proxy.connect()
    database_proxy.create_tables([Racers, RaceResults], safe=True)
    with database_proxy.atomic():
        for driver in report.values():
            existing_racer = Racers.select().where(Racers.abbreviation == driver['abbreviation']).first()
            if not existing_racer:
                racer = Racers.create(abbreviation=driver['abbreviation'],
                                      driver_name=driver['driver_name'],
                                      team=driver['team'])
            else:
                racer = existing_racer

            existing_race_result = RaceResults.select().where(RaceResults.racer_id == racer.id).first()
            if not existing_race_result:
                race_result = RaceResults.create(racer_id=racer.id,
                                                 start_time=driver['start_time'],
                                                 end_time=driver['end_time'],
                                                 best_lap_time=driver['best_lap_time'])
    if database_proxy.database != ':memory:':
        database_proxy.close()


if __name__ == "__main__":
    args = parser.parse_args()
    database = SqliteDatabase(args.db_path)
    import_data_from_files(db=database, path=args.data_folder)
