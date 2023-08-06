from flask_jwt_extended import get_current_user
from threading import Thread
from werkzeug.datastructures import FileStorage

from models.datafile import DataFileSchema, DataFileModel
from models.user import UserModel
from models.tasks.datafile_import import DataFileImportModel, DataFileImportSchema

from sources.datafile.util import open_file
from sources.datafile.exceptions import TextColumnNotFound, NotAuthorized
from sources.sentences import import_sentences_from_df


def import_data_file(file: FileStorage, format: str, text_column: str, language: str, separador=";") -> DataFileModel:
    datafile_schema = DataFileSchema()
    datafile_import_schema = DataFileImportSchema()
    df = open_file(file, format, separador)

    if format != 'txt':
        if not text_column in df.columns:
            raise TextColumnNotFound("Não foi possivel encontrar a coluna " + text_column + " no conjunto de dados")

    data_file: DataFileModel = datafile_schema.load(
        {
            'name': file.filename,
            'format': format,
            'language': language,
            'text_column': text_column
        }
    )
    data_file.owner = get_current_user()
    data_file.save()

    datafile_import_task: DataFileImportModel = datafile_import_schema.load({
        "owner": get_current_user(),
        "total": df.shape[0],
        "datafile": data_file
    })
    datafile_import_task.save()

    import_sentences_thread = Thread(
        target=import_sentences_from_df,
        args=[df, data_file, datafile_import_task, text_column]
    )
    import_sentences_thread.start()

    return data_file


def list_all_user_data_files(orderby: str = "name", order_ascending: bool = True):
    user: UserModel = get_current_user()
    documents = DataFileModel.objects(
        owner=user, excluded=False
    ).order_by(
        ("+" if order_ascending else "-") + orderby
    ).all()
    return documents


def delete_data_file(id: str):
    user: UserModel = get_current_user()
    datafile: DataFileModel = DataFileModel.objects(owner=user, id=id, excluded=False).first()
    if datafile is None:
        raise FileNotFoundError("Não foi encontrado nenhum arquivo com o id informado para esse usuário")

    datafile.excluded = True
    datafile.save()

    return datafile.excluded
