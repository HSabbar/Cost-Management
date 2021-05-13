# Cost Management
## Set up environment
        
        $ python -m virtualenv venv 
        $ .\venv\Scripts\activate.ps1
        $ pip install -r requirements.txt
        

## AWS 
  #### Set variable environnement 
       $ setx AWS_ACCESS_KEY_ID 000000000000000000
       $ settttttttx     AWS_SECRET_ACCESS_KEY 00000000000000000000000000000 
       


## AZURE 

   ##### S'authentifie avec Azure CLI  
   ###### Installer Azure CLI sur Windows avec commande PowerShell : https://docs.microsoft.com/fr-fr/cli/azure/install-azure-cli-windows?tabs=azure-powershell#powershell-command
        $ Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'; rm .\AzureCLI.msi
        $ az login 
        $ az account set -s "subscription_id"
        $ az ad sp create-for-rbac --scopes /subscriptions/$subscription_id/resourceGroups/$resourceGroup, --name $name-app-cli-auth   >> credentials.json 
   
   #### Set variable environnement 
        $ setx AZURE_CLIENT_ID 00000000-0000-0000-0000-000000000000
        $ setx AZURE_CLIENT_SECRET 00000000-0000-0000-0000-000000000000
        $ setx AZURE_SUBSCRIPTION_ID 00000000-0000-0000-0000-000000000000
        $ setx AZURE_TENANT_ID 00000000-0000-0000-0000-000000000000
        


## Google cloud platform  
  #### Set variable environnement 
<<<<<<< HEAD
  ###### Créer un compte de service plus une clé suivi les étapes : https://cloud.google.com/billing/v1/requests 
=======
  ###### CrÃ©er un compte de service plus une clÃ© suivi les Ã©tapes : https://cloud.google.com/billing/v1/requests 
>>>>>>> af8bc4f094741f1f12965a8f3b0f9d5a7b3d0f0a
       $ setx  GOOGLE_APPLICATION_CREDENTIALS path/to/credentials.json

    
