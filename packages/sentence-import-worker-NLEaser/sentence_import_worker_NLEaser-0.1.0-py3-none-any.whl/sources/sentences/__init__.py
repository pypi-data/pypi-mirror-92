import json
from flask_jwt_extended import get_current_user
from pandas import DataFrame

from models.datafile import DataFileModel
from models.tasks.datafile_import import DataFileImportModel
from models.tasks.sentence_import import SentenceImportModel, SentenceImportSchema

from sources.logger import create_logger
from sources.rabbit.producer import RabbitProducer

logger = create_logger(__name__)


def import_sentences_from_df(df: DataFrame, datafile: DataFileModel,
                             datafile_import_task: DataFileImportModel,
                             text_column: str = "sentences") -> None:
    logger.info("Importando sentenças", extra={"received_args": {
        "datafile": datafile.id
    }})
    datafile_import_task.status = "in_progress"
    datafile_import_task.save()
    try:

        schema = SentenceImportSchema()
        producer = RabbitProducer("NLEaser.sentence_import")
        for index, row in df.iterrows():
            sentence_import_task: SentenceImportModel = schema.load({
                "owner": datafile.owner,
                "datafile": datafile,
                "parent": datafile_import_task,
                "total": 1,
                "content": row[text_column],
                "index": index
            })
            sentence_import_task.save()
            producer.send_message(json.dumps({
                "task": str(sentence_import_task.id)
            }))
    except Exception as e:
        datafile_import_task.status = "error"
        datafile_import_task.error = "Erro desconhecido ao importar as sentenças"
        datafile_import_task.save()
        logger.error(
            "Erro ao importar sentenças do dataframe",
            exc_info=True,
            extra={"received_args": {
                "datafile": datafile.id,
                "datafile_import_task": datafile_import_task.id,
                "text_column": text_column
            }}
        )
