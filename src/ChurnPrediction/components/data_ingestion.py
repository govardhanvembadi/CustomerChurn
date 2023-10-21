import os
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
            Downloads the data from the url specified in the config
            return: None
        """
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url = self.config.source_URL,
                filename = self.config.local_data_file
            )
            logger.info(f'Downloaded {filename} to {self.config.local_data_file} with following info {headers}')

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
    
