from azure.mgmt.consumption import ConsumptionManagementClient
from azure.identity import AzureCliCredential

from itertools import tee
from datetime import datetime 
import pandas as pd

import os
import re
import json
import yaml

"""
    Reference : 
        AzureCliCredential : https://docs.microsoft.com/en-us/python/api/azure-identity/azure.identity.aio.azureclicredential?view=azure-python
        ConsumptionManagementClient : https://docs.microsoft.com/en-us/python/api/azure-mgmt-consumption/azure.mgmt.consumption.consumptionmanagementclient?view=azure-python

    Authenticate and authorize Python apps on Azure : https://docs.microsoft.com/fr-fr/azure/developer/python/azure-sdk-authenticate
"""

class Usage:

    def __init__(self):
        subscriptionId = os.environ['AZURE_SUBSCRIPTION_ID']
        self.scope = "subscriptions/" + subscriptionId

        azure_credential = AzureCliCredential()
        self.consumption_client =  ConsumptionManagementClient(azure_credential, subscriptionId)

    def run_by_date(self, date_filter, path_csv_file):
        usages = self.consumption_client.usage_details.list(self.scope, filter=date_filter ) #, metric="usage")
        self.save_json_csv(usages, path_csv_file)

    def save_json_csv(self, usages, path_csv_file):
        print("start create csv ....")
        data, _ = tee(usages)
        rows_data = []
        
        for a_rows in data: 
            a_rows = str(a_rows).replace("datetime.datetime(", "'datetime.datetime(").replace(">)", ">)'").replace('0, 0,', '')
            a_rows = yaml.load(a_rows, Loader=yaml.Loader)

            a_rows['date'] = a_rows['date'].replace(" 0,", "0,")
            a_rows['billing_period_start_date'] = datetime.strptime(re.search('\((.*),', a_rows['billing_period_start_date']).group(1), '%Y, %m, %d')
            a_rows['billing_period_end_date'] =  datetime.strptime(re.search('\((.*),', a_rows['billing_period_end_date']).group(1), '%Y, %m, %d')
            a_rows['date'] =  datetime.strptime(re.search('\((.*),', a_rows['date']).group(1), '%Y, %m, %d')

            rows_additional_info = {'UsageType':'', 'ImageType':'', 'ServiceType':'', 'VMName':'', 'VMProperties':'', 'VCPUs':'', 'CPUs':'', 'StorageService':'', 
                   'ResourceType':'', 'PipelineType':'', 'DataTransferDirection':'', 'DataCenter':'','NetworkBucket':'', 'ContainerId':'', 'CRPVMId':'', 
                   'UsageResourceKind':'', 'EmittingService':'', 'AHB':'', 'vCores':'', 'SLO':'', 'UniqueResourceId':'', 'ResourceCategory':''}

            if a_rows["additional_info"] != 'None':
                raws_add_info = yaml.load(a_rows["additional_info"], Loader=yaml.Loader)
                rows_additional_info.update(raws_add_info)


            rows_data.append(list(a_rows.values()) + list(rows_additional_info.values()))
            
        columnes  = list(a_rows.keys()) + list(rows_additional_info.keys())
        df = pd.DataFrame(data=rows_data, columns=columnes)
        df.to_csv(path_csv_file, encoding='utf-8', index=False)
        
        
        


def run():
    azure_usage = Usage()
    path_csv_file = 'data/Azure-cost-management.csv'
    date_filter = "properties/usageStart ge '2021-04-01' AND properties/usageStart lt '2021-04-30'" 
    
    print("Get data by date range '2021-05-01' and '2021-06-01'")
    azure_usage.run_by_date(date_filter, path_csv_file)    
    print('finished getting data from Azure')

    #print("Get data by billing period 202105")
    #azure_usage.run_by_billing_period("202105")



if __name__ == "__main__":
    run()