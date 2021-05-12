"""
Set up environment :
        $ python -m virtualenv venv
        $ .\venv\Scripts\activate.ps1

AWS : Set variable environnement  : 
        $ AWS_ACCESS_KEY_ID 000000000000000000
        $ AWS_SECRET_ACCESS_KEY 00000000000000000000000000000


AZURE : Login AZURE CLI   Set variable environnement
        $ az login 
        $ az account set -s "subscription_id"
        $ az ad sp create-for-rbac --scopes /subscriptions/$subscription_id/resourceGroups/$resourceGroup, --name $name-app-cli-auth   >> credentials.json 
        $ setx AZURE_CLIENT_ID 00000000-0000-0000-0000-000000000000
        $ setx AZURE_CLIENT_SECRET 00000000-0000-0000-0000-000000000000
        $ setx AZURE_SUBSCRIPTION_ID 00000000-0000-0000-0000-000000000000
        $ setx AZURE_TENANT_ID 00000000-0000-0000-0000-000000000000


Google cloud platform : Login 

        $setx  GOOGLE_APPLICATION_CREDENTIALS path/to/credentials.json

    
"""