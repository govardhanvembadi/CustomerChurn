from typing import Any
from ChurnPrediction.config.configuration import ConfigurationManager
from ChurnPrediction.components.model_trainer import ModelTrainer
from ChurnPrediction import logger


STAGE_NAME =  'Model Training Stage'

class ModelTrainerPipeline:
    def __call__(self):
        pass
    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config = model_trainer_config)
        model_trainer.train()



if __name__ == "__main__":
    try:
        logger.info(f"========= Stage {STAGE_NAME} started =========")
        object = ModelTrainerPipeline()
        object.main()
        logger.info(f"========= Stage {STAGE_NAME} completed =========")

    except Exception as e:
        logger.exception(e)
        raise e
