from ChurnPrediction.constants import *
from ChurnPrediction.utils.common import read_yaml, create_directory
from ChurnPrediction.entity.config_entity import (  DataIngestionConfig, 
                                                    DataValidationConfig, 
                                                    DataTransformationConfig, 
                                                    ModelTrainerConfig,
                                                    EvaluationConfig)

class ConfigurationManager:
    def __init__(
            self,
            config_filepath = CONFIG_FILE_PATH,
            params_filepath = PARAMS_FILE_PATH,
            schema_filepath = SCHEMA_FILE_PATH
    ):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directory([self.config.artifacts_root])
    

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directory([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir = config.root_dir,
            source_URL= config.source_URL,
            local_data_file = config.local_data_file
        )

        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        create_directory([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir = config.root_dir,
            data_dir = config.data_dir,
            STATUS_FILE = config.STATUS_FILE,
            schema = schema
        )

        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation

        create_directory([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir = config.root_dir,
            data_path = config.data_path,
            train_data_path = config.train_data_path,
            test_data_path = config.test_data_path
        )

        return data_transformation_config
    

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        params = self.params.LogisticRegression
        schema = self.schema.TARGET_COLUMN

        create_directory([config.root_dir])
        
        model_trainer_config = ModelTrainerConfig(
            root_dir = config.root_dir,
            train_data_path = config.train_data_path,
            test_data_path = config.test_data_path,
            model_path = config.model_path,
            C = params.C,
            max_iter = params.max_iter,
            penalty = params.penalty,
            solver = params.solver,
            target_column = list(schema.keys())[0]
        )

        return model_trainer_config
    

    def get_evaluation_config(self) -> EvaluationConfig:
        config = self.config.model_evaluation
        params = self.params.LogisticRegression
        schema = self.schema.TARGET_COLUMN
        
        evaluation_config = EvaluationConfig(
            model_path = config.model_path,
            test_data_path = config.test_data_path,
            all_params = params,
            target_column = list(schema.keys())[0],
            scores_path = config.scores_path
        )

        return evaluation_config

    
