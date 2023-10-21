from typing import Any
from ChurnPrediction.config.configuration import ConfigurationManager
from ChurnPrediction.components.model_evaluation import Evaluation
from ChurnPrediction import logger


STAGE_NAME =  'Model Evaluation Stage'

class ModelEvaluationPipeline:
    def __call__(self):
        pass
    def main(self):
        config = ConfigurationManager()
        evaluation_config = config.get_evaluation_config()
        model_evaluator = Evaluation(evaluation_config)
        model_evaluator.evaluation()



if __name__ == "__main__":
    try:
        logger.info(f"========= Stage {STAGE_NAME} started =========")
        object = ModelEvaluationPipeline()
        object.main()
        logger.info(f"========= Stage {STAGE_NAME} completed =========")

    except Exception as e:
        logger.exception(e)
        raise e

