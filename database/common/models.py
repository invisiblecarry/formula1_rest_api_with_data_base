from peewee import (Model,
                    IntegerField,
                    DateTimeField,
                    ForeignKeyField,
                    CharField,
                    DatabaseProxy,
                    SqliteDatabase)

database_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy


class Racers(BaseModel):
    id = IntegerField(primary_key=True)
    abbreviation = CharField(unique=True)
    driver_name = CharField()
    team = CharField()


class RaceResults(BaseModel):
    racer_id = ForeignKeyField(Racers, backref='race_times')
    start_time = DateTimeField()
    end_time = DateTimeField()
    best_lap_time = DateTimeField()
