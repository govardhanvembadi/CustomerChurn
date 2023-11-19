import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from ChurnPrediction import logger


from ChurnPrediction.config.configuration import ConfigurationManager
from ChurnPrediction.components.data_transformation import DataTransformation

class PredictionPipeline:
    def __init__(self):
        self.model = joblib.load(Path('artifacts/model/model.joblib'))

    def predict(self, data):
        preprocessor_object = joblib.load(Path('artifacts/model/preprocessor.joblib'))
        logger.info("got the Preprocessor object for prediction data preprocessing.")

        data_preprocessed = preprocessor_object.transform(data)
        logger.info("preprocessed the features.")
        logger.info(f'{data_preprocessed}')

        # Create a DataFrame with the preprocessed features
        transformed_feature_names = preprocessor_object.get_feature_names_out(input_features = data.columns)
        final_preprocessed_data = pd.DataFrame(data_preprocessed, columns=transformed_feature_names)

        logger.info(f"{final_preprocessed_data}")
        prediction = self.model.predict(final_preprocessed_data)

        return prediction
    
    
class CustomData:
    def __init__(self, data: dict):
        self.data = data

    def get_data_as_dataframe(self):
        try:
            logger.info("transforming data into dataframe")
            data_df = pd.DataFrame(data = [self.data.values()], columns = self.data.keys())
            logger.info(f"data turned into dataframe:  {data_df}")
            return data_df
        except Exception as e:
            raise e