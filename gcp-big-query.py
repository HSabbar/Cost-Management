import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_storage

import pyarrow 
# Explicitly create a credentials object. This allows you to use the same
# credentials for both the BigQuery and BigQuery Storage clients, avoiding
# unnecessary API calls to fetch duplicate authentication tokens.
credentials, your_project_id = google.auth.default(
                    scopes=["https://www.googleapis.com/auth/cloud-platform"]
                )
print(your_project_id)
# Make clients.
bqclient = bigquery.Client(credentials=credentials, project=your_project_id)
bqstorageclient = bigquery_storage.BigQueryReadClient(credentials=credentials)

# Download a table.
table = bigquery.TableReference.from_string(
    "projet_id.name_Ressources_BigQquery.name_table"
)
rows = bqclient.list_rows(
    table
)
dataframe_api_client = rows.to_dataframe(bqstorage_client=bqstorageclient)
print(len(dataframe_api_client))
dataframe_api_client.head()
dataframe_api_client.to_csv('data/gcp-cost-management.csv', encoding='utf-8', index=False)