import pandas as pd
import boto3
import zlib
import io
import re



bucket_name= 'hourly-detailled-report.ilki.fr' 
df_data = []

s3 = boto3.resource(
    service_name='s3',
    region_name='eu-west-3',
    aws_access_key_id= os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key= os.environ['AWS_SECRET_ACCESS_KEY']
)

def get_csv(s3, bucket_name, key):
    obj = s3.Bucket(bucket_name).Object(key).get()
    csv = zlib.decompress(obj['Body'].read(), 16+zlib.MAX_WBITS)
    return pd.read_csv(io.StringIO(csv.decode('utf-8')),  sep=',', error_bad_lines=False, index_col=False, dtype='unicode')

for i, object_summary in enumerate(s3.Bucket(bucket_name).objects.filter(Prefix="/Hourly-detailled-report/")):
    if bool(re.compile('.csv').search(object_summary.key)) and i > 1500:
        df_data.append(get_csv(s3, bucket_name, object_summary.key)) 
        
df = pd.concat(df_data)
df.to_csv('data/aws-cost-management.csv', encoding='utf-8', index=False)