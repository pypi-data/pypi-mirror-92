import mongoengine as me
import marshmallow as ma

from models.datafile import DataFileModel
from models.tasks import TaskModel, TaskSchema
from models.user import UserModel


class DataFileImportModel(TaskModel):
    meta = {
        'allow_inheritance': True
    }

    task_name = me.fields.StringField(default="datafile_import")
    datafile: DataFileModel = me.fields.ReferenceField(DataFileModel, required=True)


class DataFileImportSchema(TaskSchema):
    task_name = ma.fields.String(default="datafile_import")
    datafile = ma.fields.String(required=True)

    @ma.pre_load()
    def prepare_data(self, data, **kwargs):
        data["owner"] = str(data["owner"].id)
        data["datafile"] = str(data["datafile"].id)
        return data

    @ma.post_load()
    def create_task(self, data, **kwargs):
        return DataFileImportModel(**data)
