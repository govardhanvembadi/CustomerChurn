import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from ChurnPrediction.utils.common import *
import pandas as pd

from ChurnPrediction import logger
from ChurnPrediction.entity.config_entity import EvaluationConfig


class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config

    def evaluate_model(self, model, X_test, y_test):

        # Make predictions on the test data
        y_pred = model.predict(X_test)

        # Calculate evaluation scores
        scores = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred),
            "recall": recall_score(y_test, y_pred),
            "f1_score": f1_score(y_test, y_pred)
        }
        logger.info(f"evaluation scores: {scores}")

        return scores
    
    def evaluation(self):
        try:
            model = joblib.load(self.config.model_path)
            test_data = pd.read_csv(self.config.test_data_path)
            logger.info(f'model has loaded')
        
            # Separate features and labels
            X_test = test_data.drop(columns=[self.config.target_column], axis = 1)
            y_test = test_data[self.config.target_column]

            scores = self.evaluate_model(model, X_test, y_test)

            logger.info(f"scores will be saving")
            # Save the scores to a JSON file
            save_json(path = Path(self.config.scores_path), data = scores)
            logger.info(f"scores saved to scores.json file")

        except Exception as e:
            raise e        