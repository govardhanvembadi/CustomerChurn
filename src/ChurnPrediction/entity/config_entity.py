from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen = True)
class DataIngestionConfig:
    root_dir: Path
    dvc_file_path: Path
    local_data_file: Path


@dataclass
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: str
    data_dir: Path
    schema: dict


@dataclass(frozen = True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    train_data_path: Path
    test_data_path: Path


@dataclass(frozen = True)
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    test_data_path: Path
    model_path: Path
    C: float
    max_iter: int
    penalty: str
    solver: str
    target_column: str


@dataclass
class EvaluationConfig:
    model_path : Path
    test_data_path : Path
    all_params : dict
    target_column : str
    scores_path : Path
    tracking_uri: str
    experiment_name: str