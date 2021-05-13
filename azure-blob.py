from io import BytesIO
from urllib.parse import urlparse
from azure.storage.blob import BlobServiceClient
import pandas as pd
import os 


def azure_download_obj_blob(url=None):

    if url:
        blob_url = "https://csb10037ffe9f617530.blob.core.windows.net"
        blob_service_client = BlobServiceClient(account_url=blob_url , credential=os.environ["BLOL_ACC_KEY"]) 

        path = urlparse(url).path
        path = path.split("/")
        container = path[1]
        blob = '/'.join(path[2:])
        #print(container, blob)
        blob_client = blob_service_client.get_blob_client(container=container, blob=blob)
        with BytesIO() as input_blob:
            blob_client.download_blob().download_to_stream(input_blob)
            input_blob.seek(0)
            df = pd.read_csv(input_blob)
        return df
    else:
        return None

print('Start getting data from Azure')
path_obj = "/exports/dialympn/CostManangement/20210401-20210430/CostManangement_0fe527e1-a9b3-4b88-8075-cc788c672c78.csv"
df = azure_download_obj_blob(path_obj)
df.to_csv('data/Azure-blob-cost-management.csv', encoding='utf-8', index=False)
print('finished getting data from Azure')
