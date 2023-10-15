import os
import urllib.request as request
import pandas as pd
from pathlib import Path
from ChurnPrediction import logger
from ChurnPrediction.entity.config_entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            logger.info("DataValidation started")
            validation_status = None
            data = pd.read_csv(self.config.data_dir)
            all_cols = list(data.drop(['Churn'], axis = 1).columns)
            all_schema_cols = self.config.schema

            for col in all_cols:
                if (col not in all_schema_cols.keys()) or (all_schema_cols[col] != data[col].dtype):
                    #logger.info(f"{col} :  {all_schema_cols[col]} !=  {data[col].dtype}")
                    validation_status = False
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f'Validation status: {validation_status}')

                else:
                    #logger.info(f"{col} :  {all_schema_cols[col]} ==  {data[col].dtype}")
                    validation_status = True
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f'Validation status: {validation_status}')
                    
            return validation_status
            
        except Exception as  e:
            raise e

