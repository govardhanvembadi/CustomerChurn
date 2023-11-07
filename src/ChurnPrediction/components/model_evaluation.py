import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from ChurnPrediction.utils.common import *
import pandas as pd
import mlflow
from urllib.parse import urlparse

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

            # Set the remote tracking uri for the experiments
            mlflow.set_tracking_uri(self.config.tracking_uri)
            tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
            
            experiment_name = self.config.experiment_name
            
            try:
                # create new experiment
                mlflow.create_experiment(experiment_name)
                logger.info(f"{experiment_name} has been created")

            except mlflow.exceptions.MlflowException as e:
                # set experiment if the experiment already exists
                mlflow.set_experiment(experiment_name = experiment_name)
                logger.info(f"{experiment_name} has been reassembled")

            experiment = mlflow.get_experiment_by_name(experiment_name)
            experiment_id = experiment.experiment_id

            with mlflow.start_run(experiment_id = experiment_id):

                logger.info("Started mlflow run")

                # Separate features and labels
                X_test = test_data.drop(columns=[self.config.target_column], axis = 1)
                y_test = test_data[self.config.target_column]
                
                #evaluate the scores 
                scores = self.evaluate_model(model, X_test, y_test)
                logger.info(f"scores will be saving")

                # log all the params into mlflow 
                mlflow.log_params(self.config.all_params)
                logger.info("Logged all the params into mlflow")

                # log all the metircs into mlflow
                mlflow.log_metric("accuracy", scores['accuracy'])
                mlflow.log_metric("precision", scores['precision'])
                mlflow.log_metric("recall", scores['recall'])
                mlflow.log_metric("f1_score", scores['f1_score']) 
                logger.info("logged all the metrics into mlflow")

                # log and register the model
                # Model registry does not work with file store
                if tracking_url_type_store != "file":
                    # Register the model
                    mlflow.sklearn.log_model(model, "model", registered_model_name="model_3")
                    logger.info("registered the model to the model registry")
                else:
                    # log the model to the artifact store
                    mlflow.sklearn.log_model(model, "model")
                    logger.info("logged the model to the artifact store")

                # Save the scores to a JSON file
                save_json(path = Path(self.config.scores_path), data = scores)
                logger.info(f"scores saved to scores.json file")

        except Exception as e:
            raise e        