from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig  
from networksecurity.entity.artifact_entity import DataIngestionArtifact  

import os
import sys
import pymongo
import numpy as np
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            logging.info(f"Fetching data from database: {database_name}, collection: {collection_name}")
            data = list(collection.find())
            logging.info(f"Number of records fetched: {len(data)}")
            
            df = pd.DataFrame(data)
            if df.empty:
                logging.warning("The DataFrame is empty. No data found in the collection.")
            if "_id" in df.columns.to_list():
                df.drop(columns=['_id'], axis=1, inplace=True)
            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self,df:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            df.to_csv(feature_store_file_path,index=False,header=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def split_data_as_train_test(self,df:pd.DataFrame):
        try:
            if df.empty:
                raise ValueError("The dataframe is empty. Ensure the data source contains records before splitting.")
            
            train_set, test_set = train_test_split(
                df, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Successfully split the data into train and test set")
            logging.info("exited the split_data_as_train_test method of DataIngestion class")

            dir_path=os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("Created the directory for train and test file path")

            train_set.to_csv(
                self.data_ingestion_config.train_file_path,index=False,header=True
            )
            if os.path.exists(self.data_ingestion_config.train_file_path):
                logging.info(f"Train file saved successfully: {self.data_ingestion_config.train_file_path}")
            test_set.to_csv(
                self.data_ingestion_config.test_file_path,index=False,header=True
            )
            logging.info("Successfully saved train and test file")
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            logging.info("called the dataingestion artifact")
            dataingestionartifact = DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
                )
            logging.info("Data ingestion completed successfully")
            return dataingestionartifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)