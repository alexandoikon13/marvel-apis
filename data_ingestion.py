from config import database_url, aws_access_key_id, aws_secret_access_key, s3_bucket_name, path_prefix
import pandas as pd
import boto3
from io import BytesIO
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Characters, Comics, Events, Series, Stories

## Setting up the S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

## Create SQLAlchemy engine and session
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

## Table mapping for ingestion
table_mapping = {
    'Characters': Characters,
    'Comics': Comics,
    'Events': Events,
    'Series': Series,
    'Stories': Stories
}

def read_csv_from_s3(file_name):
    ''' Read a CSV file from S3 and return a pandas DataFrame '''
    key = f"{path_prefix}/{file_name}.csv"
    response = s3_client.get_object(Bucket=s3_bucket_name, Key=key)
    return pd.read_csv(BytesIO(response['Body'].read()))

def record_exists(session, model, record_id):
    ''' Check if a record already exists in the database '''
    return session.query(model).filter_by(character_id=record_id).first() is not None

def ingest_data():
    ''' Ingest data from S3 into the database '''
    for table_name, model in table_mapping.items():
        print(f"Ingesting data for {table_name}...")
        try:
            df = read_csv_from_s3(table_name)
            records = df.to_dict(orient='records')

            for record in records:
                if not record_exists(session, model, record['character_id']):
                    obj = model(**record)
                    session.add(obj)

            session.commit()
            print(f"Data ingestion successful for {table_name}!")
        except Exception as e:
            session.rollback()
            print(f"Failed to ingest data for {table_name}: {e}")
        finally:
            session.close()
