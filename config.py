import os
import urllib.parse

''' This file contains the configuration settings for the application '''

## Retrieve the database URL from environment variables
database_url = os.environ.get('DATABASE_URL')

## Adjust the URL for compatibility with SQLAlchemy
## SQLAlchemy requires 'postgresql://' instead of 'postgres://'
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://')

## Retrieve CloudCube URL from environment variables
## CloudCube is used for AWS S3 bucket access in this project
cloudcube_url = os.environ.get('CLOUDCUBE_URL')
parsed_url = urllib.parse.urlparse(cloudcube_url)

## Extract AWS credentials and S3 bucket information from the CloudCube URL
aws_access_key_id = os.environ.get('CLOUDCUBE_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('CLOUDCUBE_SECRET_ACCESS_KEY')
s3_bucket_name = parsed_url.netloc.split('.')[0]
path_prefix = parsed_url.path.lstrip('/')