import os
import dvc.api
import urllib.request as request
from pathlib import Path
from ChurnPrediction import logger
from zipapp import zipfile
from ChurnPrediction.utils.common import get_size
from ChurnPrediction.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        """
            Downloads the data from the dvc tracked repository(url provided).
            dvc.api.open() function from the dvc API will help in downloading the latest version of data according to 
            hash id present in the data.csv.dvc file. 
            return: None
        """
        if not os.path.exists(self.config.local_data_file):
            with dvc.api.open(self.config.dvc_file_path, repo = "https://github.com/Govardhan211103/CustomerChurn", mode = "rb") as dvc_file:
                with open(self.config.local_data_file, "wb") as local_file:
                    local_file.write(dvc_file.read())
            logger.info(f'Downloaded data version from {self.config.dvc_file_path} to {self.config.local_data_file}')

        else:
            logger.info(f'File {self.config.local_data_file} already exists')

    def extraact_zip_file(self):
        """
            Unzips the downloaded file
            return: None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
    
