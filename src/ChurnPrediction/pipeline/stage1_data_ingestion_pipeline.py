from typing import Any
from ChurnPrediction.config.configuration import ConfigurationManager
from ChurnPrediction.components.data_ingestion import DataIngestion
from ChurnPrediction import logger


STAGE_NAME =  'Data Ingestion Stage'

class DataIngestionTrainingPipeline:
    def __call__(self):
        pass
    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config = data_ingestion_config)
        data_ingestion.download_file()


if __name__ == "__main__":
    try:
        logger.info(f"========= Stage {STAGE_NAME} started =========")
        object = DataIngestionTrainingPipeline()
        object.main()
        logger.info(f"========= Stage {STAGE_NAME} completed =========")

    except Exception as e:
        logger.exception(e)
        raise e
