import mongoengine as me
import marshmallow as ma

from models.datafile import DataFileModel
from models.user import UserModel
from models.tasks.datafile_import import DataFileImportModel, DataFileImportSchema


class SentenceImportModel(DataFileImportModel):
    task_name = me.fields.StringField(default="sentence_import")
    parent: DataFileImportModel = me.fields.ReferenceField(DataFileImportModel, required=True)
    content = me.fields.StringField(required=True)
    index = me.fields.IntField(required=True)


class SentenceImportSchema(DataFileImportSchema):
    parent = ma.fields.String(required=True)
    content = ma.fields.String(required=True)
    index = ma.fields.Integer(required=True)

    @ma.pre_load
    def prepare_data(self, data, **kwargs):
        data["owner"] = str(data["owner"].id)
        data["datafile"] = str(data["datafile"].id)
        data["parent"] = str(data["parent"].id)
        return data

    @ma.post_load()
    def create_task(self, data, **kwargs):
        return SentenceImportModel(**data)
