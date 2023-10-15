from ChurnPrediction import logger
from ChurnPrediction.pipeline.stage1_data_ingestion_pipeline import DataIngestionPipeline
from ChurnPrediction.pipeline.stage2_data_validation_pipeline import DataValidationPipeline
from ChurnPrediction.pipeline.stage3_data_transformation_pipeline import DataTransformationPipeline
from ChurnPrediction.pipeline.stage4_model_trainer_pipeline import ModelTrainerPipeline


STAGE_NAME =  'Data Ingestion Stage'

try:
    logger.info(f"========= Stage {STAGE_NAME} started =========")
    data_ingestion = DataIngestionPipeline()
    data_ingestion.main()
    logger.info(f"========= Stage {STAGE_NAME} completed =========")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME =  'Data Validation Stage'

try:
    logger.info(f"========= Stage {STAGE_NAME} started =========")
    object = DataValidationPipeline()
    object.main()
    logger.info(f"========= Stage {STAGE_NAME} completed =========")

except Exception as e:
    logger.exception(e)
    raise e


STAGE_NAME =  'Data Transformation Stage'

try:
    logger.info(f"========= Stage {STAGE_NAME} started =========")
    object = DataTransformationPipeline()
    object.main()
    logger.info(f"========= Stage {STAGE_NAME} completed =========")

except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME =  'Model Trainer Stage'

try:
    logger.info(f"========= Stage {STAGE_NAME} started =========")
    object = ModelTrainerPipeline()
    object.main()
    logger.info(f"========= Stage {STAGE_NAME} completed =========")

except Exception as e:
    logger.exception(e)
    raise e