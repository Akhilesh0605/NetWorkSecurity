import os
import sys
import numpy as np
import pandas as pd

#defining common constant varible for traiing pipleine

TARGET_COLUMMN="Result"
PIPELINE_NAME : str ="NetworkSecurity"
ARTIFACT_DIR : str="Artifacts"
FILE_NAME :str="Phishing_Legitimate_full.csv"
TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME : str="test.csv"

# data ingestion realted constant start with DATA_INGESTION VAR NAME

DATA_INGESTION_COLLECTION_NAME: str = "PhishingData"
DATA_INGESTION_DATABASE_NAME: str = "NetworkSecurityData"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_iNGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2
