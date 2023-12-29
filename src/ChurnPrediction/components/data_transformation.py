import os
import pandas as pd
import numpy as np
import joblib

from pathlib import Path
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder,MinMaxScaler, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

from ChurnPrediction import logger
from ChurnPrediction.entity.config_entity import DataTransformationConfig
from ChurnPrediction.utils.common import create_directory


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        create_directory(["artifacts/model"])
        self.preprocessor_file_path = "artifacts/model/preprocessor.joblib"

    def get_transformer_object(self) -> ColumnTransformer:
        try:
            # Feature lists
            cat_columns = [
                'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService',
                'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
                'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
                'Contract', 'PaperlessBilling', 'PaymentMethod'
            ]
            num_columns = ['tenure', 'MonthlyCharges', 'TotalCharges']

            # Pipelines for features
            numeric_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='mean')),
                ('scaler', StandardScaler())
            ])

            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('label', OrdinalEncoder())
            ])

            preprocessor = ColumnTransformer([
                ('numerical_pipeline', numeric_transformer, num_columns),
                ('categorical_pipeline', categorical_transformer, cat_columns)
            ])

            return preprocessor

        except Exception as e:
            raise e

    def transform_data(self):
        data = pd.read_csv(self.config.data_path)

        # Remove 'customerID' as it is unique for each customer
        data.drop(['customerID'], axis=1, inplace=True)
        logger.info("customerID feature dropped.")

        # Change the datatypes of 'SeniorCitizen' and 'TotalCharges' features
        data['SeniorCitizen'] = data['SeniorCitizen'].astype('object')
        data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors='coerce')
        logger.info("SeniorCitizen and TotalCharges features data types has been updated.")

        # Encode 'Churn' (the target feature) into numeric values
        data['Churn'] = data['Churn'].replace({'Yes': 1, 'No': 0})
        data['Churn'] = data['Churn'].astype('object')

        # Split features and target
        data_X = data.drop(['Churn'], axis=1)
        data_y = data['Churn']

        # Get the preprocessor object
        preprocessor_object = self.get_transformer_object()
        logger.info("got the Preprocessor object.")
        
        # Preprocess the features
        data_X_preprocessed = preprocessor_object.fit_transform(pd.DataFrame(data_X))
        logger.info("preprocessed the features.")

        # Create a DataFrame with the preprocessed features
        transformed_feature_names = preprocessor_object.get_feature_names_out(input_features = data_X.columns)
        data_X_scaled = pd.DataFrame(data_X_preprocessed, columns=transformed_feature_names)

        # Split the data into train and test sets
        train_data, test_data = train_test_split(pd.concat([data_X_scaled, data_y], axis = 1), test_size=0.2, random_state=42, stratify = data_y)
        logger.info("Data spltting completed.")

        # Save the proprocessor object into joblib file format
        joblib.dump(preprocessor_object, Path(self.preprocessor_file_path))
        logger.info("preprocessor object saved into joblib file format")

        # Save the train and test data to CSV files
        train_data.to_csv(self.config.train_data_path, index=False)
        test_data.to_csv(self.config.test_data_path, index=False)
        logger.info("Data saved to CSV files as train_data.csv and test_data.csv.")

        



