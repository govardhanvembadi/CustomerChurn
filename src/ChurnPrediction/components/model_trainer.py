import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from ChurnPrediction import logger
import joblib
import os
from ChurnPrediction.entity.config_entity import ModelTrainerConfig


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train(self):
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)

        train_X = train_data.drop([self.config.target_column], axis = 1)
        train_y = np.ravel(train_data[[self.config.target_column]])
        test_X = test_data.drop([self.config.target_column], axis = 1)
        test_y = np.ravel(test_data[[self.config.target_column]])

        model = LogisticRegression(
            C = self.config.C,
            max_iter = self.config.max_iter, 
            penalty = self.config.penalty, 
            solver = self.config.solver
        )

        model.fit(train_X, train_y)

        joblib.dump(model, Path(self.config.model_path))


        