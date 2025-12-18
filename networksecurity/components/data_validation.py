from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import sys, os

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            columns = self._schema_config.get("columns", [])  # If schema is {"columns": [...]}
            number_columns = len(columns)
            logging.info(f"Required number of columns: {number_columns}")
            logging.info(f"Dataframe has columns: {dataframe.shape[1]}")
            if len(dataframe.columns) == number_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_sample_dist = ks_2samp(d1, d2)
                if threshold < is_sample_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column: {
                    "p_value": float(is_sample_dist.pvalue),
                    "drift_status": is_found
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report, replace=True)
            return status  # Add return statement
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:  # Fix: Return type to DataValidationArtifact
        try:
            logging.info("Data validation has been started")  # Fix: "DAta" -> "Data"
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            # Remove duplicate: self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)  # Already done in __init__
            logging.info("Reading training and test data for validation")
            train_dataframe = self.read_data(train_file_path)
            test_dataframe = self.read_data(test_file_path)

            logging.info("Validating number of columns in training data")
            status = self.validate_number_of_columns(train_dataframe)
            status_test = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = f"Train dataframe does not contain all columns"  # Fix: "datafame" -> "dataframe"
                raise ValueError(error_message)  # Add: Raise exception
            if not status_test:
                error_message = f"Test dataframe does not contain all columns"  # Fix: "datafame" -> "dataframe"
                raise ValueError(error_message)  # Add: Raise exception

            logging.info("Number of columns are validated successfully")
            logging.info("Checking Data Drift")
            
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            logging.info("Data validation completed successfully")
            return data_validation_artifact  # Add return statement
        except Exception as e:
            raise NetworkSecurityException(e, sys)