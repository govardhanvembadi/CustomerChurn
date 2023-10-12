## 'template.py' file contains the code to create all the necessary files and folders in project.

import os
from pathlib import Path
import logging

## setting the basic structure of logging 
logging.basicConfig(level=logging.INFO, format = '[%(asctime)s]: %(message)s')

project_name = 'ChurnPrediction' 

files = [
    '.github/workflows/.gitkeep', ## needed for a .yaml file to maintain CI/CD pipelines code.
    f"src/{project_name}/__init__.py", ##constructor file with 
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "dvc.yaml",
    "params.yaml",
    "requirements.py",
    "setup.py",
    "research/trial.ipynb"

]

for filepath in files:
    filepath = Path(filepath) ## to ensure that the path is in windows path format
    file_directory, filename = os.path.split(filepath) ## returns the name of directory and name of file

    if file_directory != "":
        os.makedirs(file_directory, exist_ok = True) ## creating the directory if it not exists

        ## logging the information that directory has created.
        logging.info(f"Creating directory: {file_directory} for the file {filename}") 

    if(not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filename} in {filepath}.")
    else:
        logging.info(f"{filename} is already exists.")


