from ChurnPrediction import logger
from ChurnPrediction.pipeline.stage1_data_ingestion_pipeline import DataIngestionTrainingPipeline

STAGE_NAME =  'Data Ingestion Stage'

try:
    logger.info(f"========= Stage {STAGE_NAME} started =========")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f"========= Stage {STAGE_NAME} completed =========")
except Exception as e:
    logger.exception(e)
    raise e