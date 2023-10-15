from typing import Any
from ChurnPrediction.config.configuration import ConfigurationManager
from ChurnPrediction.components.data_transformation import DataTransformation
from ChurnPrediction import logger


STAGE_NAME =  'Data Transformation Stage'

class DataTransformationPipeline:
    def __call__(self):
        pass
    def main(self):
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformation(config = data_transformation_config)
        data_transformation.transform_data()



if __name__ == "__main__":
    try:
        logger.info(f"========= Stage {STAGE_NAME} started =========")
        object = DataTransformationPipeline()
        object.main()
        logger.info(f"========= Stage {STAGE_NAME} completed =========")

    except Exception as e:
        logger.exception(e)
        raise e
