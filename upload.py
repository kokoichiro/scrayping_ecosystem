#!/usr/bin/python Python 2.7.13
#Upload local csv file to both Bigquery and Google Cloud Storage.

from apiclient import discovery
from oauth2client.client import GoogleCredentials
import datetime
credentials = GoogleCredentials.get_application_default()
service = discovery.build('storage', 'v1', credentials=credentials)
import pandas as pd
#from pandas.io import gbq
import pandas.io.gbq as gbq
import numpy as np


now = datetime.datetime.today()
today = now.strftime("%Y-%m-%d")
year,month,day = today.split("-")
today_name = year+month+day

#These configs are necessary for uploading the data to Big Query
project_id = 'iprospect-global-data-lake'
dataset_id = 'cory_airflow_test'
bq_tbl_name = 'share_price'
table_destination = dataset_id + '.' + bq_tbl_name

project_id2 = 'plenary-genre-642'
dataset_id2 = 'airflow_share_price'
bq_tbl_name2 = 'share_price'
table_destination2 = dataset_id2 + '.' + bq_tbl_name2

#gcs only requires bucket name and object name.(they don't need project and dataset)
gcs_bucket_name = 'cory-test-airflow'

target_filename = '/home/dev-cory/scrayping/data/file.csv'
upload_filename = 'share_price' + today_name +'.csv'


body = {'name': upload_filename}
req = service.objects().insert(bucket=gcs_bucket_name, body=body, media_body=target_filename)
resp = req.execute()


df_upload = pd.read_csv(target_filename)
df_upload=df_upload.assign(date = today_name)
df_upload['key_id']=df_upload['key_id'].astype(str)
df_upload['date']=df_upload['date'].astype(str)
df_upload['key_id2'] = df_upload['date'] + df_upload['key_id']
#bq_schema=gbq.generate_bq_schema(df_upload, default_type='STRING')

#gbq can upload only 10000 rows at once. So we need to have different approach when you want to upload more data at once.
#Maybe the link below is helpful to push large data into BigQuery.
#https://stackoverflow.com/questions/34201923/python-bigquery-allowlargeresults-with-pandas-io-gbq
gbq.to_gbq(df_upload, table_destination, project_id, if_exists='append',chunksize=10000)
gbq.to_gbq(df_upload, table_destination2, project_id2, if_exists='append',chunksize=10000)
