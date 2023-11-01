from peewee import SqliteDatabase, Model, IntegerField, TextField, DateTimeField, ForeignKeyField, CharField
from datetime import datetime

db = SqliteDatabase('formula1_report.db')


class BaseModel(Model):
    class Meta:
        database = db


class Racers(BaseModel):
    id = IntegerField(primary_key=True)
    abbreviation = CharField(unique=True)
    driver_name = CharField()
    team = CharField()


class RaceResults(BaseModel):
    racer_id = ForeignKeyField(Racers,  backref='race_times')
    start_time = DateTimeField()
    end_time = DateTimeField()
    best_lap_time = DateTimeField()
