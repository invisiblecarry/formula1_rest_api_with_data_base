from typing import Dict, List, TypeVar
from ..common.models import db, BaseModel
from peewee import ModelSelect, DoesNotExist

T = TypeVar('T')


def _store_data(dtbs: db, model: T, **data: [Dict]) -> None:
    with dtbs.atomic():
        return model.create(**data)


def _retrieve_data(dtbs: db, model: T, *columns: BaseModel) -> ModelSelect:
    with dtbs.atomic():
        response = model.select(*columns)

    return response


def _update_data(dtbs: db, model: T, data: [Dict], **conditions: [Dict]):
    with dtbs.atomic():
        try:
            entry = model.get(**conditions)
            for key, value in data.items():
                setattr(entry, key, value)
            entry.save()
            return entry
        except DoesNotExist:
            return None


def _delete_data(dtbs: db, model: T, **conditions: [Dict]):
    with dtbs.atomic():
        try:
            entry = model.get(**conditions)
            entry.delete_instance()
            return True
        except DoesNotExist:
            return False


class CRUDInterface():
    @staticmethod
    def create(model, **data):
        return _store_data(db, model, **data)

    @staticmethod
    def retrieve(model, *columns):
        return _retrieve_data(db, model, *columns)

    @staticmethod
    def update(model, data, **conditions):
        return _update_data(db, model, data, **conditions)

    @staticmethod
    def delete(model, **conditions):
        return _delete_data(db, model, **conditions)

