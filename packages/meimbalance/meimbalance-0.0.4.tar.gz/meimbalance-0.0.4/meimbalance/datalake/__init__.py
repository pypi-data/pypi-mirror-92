# Will do the following when included:
#   - Load environment variables
#   - Get Azure credentials
#   - Define constants for the datalakes
#
import os
import tempfile
from azure.identity._credentials.managed_identity import ManagedIdentityCredential
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
from azure.datalake.store import core, lib, multithread

class Datalake:
    def __init__(self, datalake_name):
        self.datalake_name = datalake_name


class DatalakeGen2(Datalake):
    def __init__(self,datalake_name, azure_credential):
            self.azure_credential = azure_credential
            self.container_name = 'root'
            super().__init__(datalake_name)

    def open_file(self, directory_name, filename): 
        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", self.datalake_name), credential=self.azure_credential)
        file_system_client = service_client.get_file_system_client(file_system=self.container_name)
        directory_client = file_system_client.get_directory_client(directory_name)
        file_client = directory_client.get_file_client(filename)
        download = file_client.download_file()
        downloaded_bytes = download.readall()
        localfile=tempfile.TemporaryFile()
        localfile.write(downloaded_bytes)
        localfile.seek(0,0)
        
        return localfile
        

class DatalakeGen1(Datalake):
    def __init__(self,datalake_name, token):
        self.token = token
        super().__init__(datalake_name)

    def open_file(self, directory_name, filename):
        filepath=directory_name+filename

        adlFileSystem = core.AzureDLFileSystem(self.token, store_name=self.datalake_name)
        with adlFileSystem.open(filepath, 'rb') as f:
            downloaded_bytes = f.read()
            localfile=tempfile.TemporaryFile()
            localfile.write(downloaded_bytes)
            localfile.seek(0,0)
            
            return localfile

class ImbalanceDatalakes:
    def __init__(self):
        load_dotenv()
        self.azure_cretential = DefaultAzureCredential()
        try:
            self.imbalance_datalake_name=os.environ['IMBALANCE_DATALAKE_NAME']
            self.shared_datalake_gen2_name=os.environ['SHARED_DATALAKE_GEN2_NAME']
            self.shared_datalake_gen1_name=os.environ['SHARED_DATALAKE_GEN1_NAME']
            self.azure_tenant_id=os.environ['AZURE_TENANT_ID']
            self.azure_client_id=os.environ['AZURE_CLIENT_ID']
            self.azure_client_secret=os.environ['AZURE_CLIENT_SECRET']
        except:
            print('ERROR: Missing environment variables, need to declare IMBALANCE_DATALAKE_NAME, SHARED_DATALAKE_GEN2_NAME and SHARED_DATALAKE_GEN1_NAME')
            print('Hint: Put these variables in the .env file in the project root, and create a source statement in ~/.bashrc:')
            print('if [ -f ~/source/Imbalance/.env ]; then')
            print('    source ~/source/Imbalance/.env')
            print('fi')
            exit(1)
        
        token = lib.auth(tenant_id = self.azure_tenant_id, client_id = self.azure_client_id, client_secret = self.azure_client_secret)

        self.imbalance_datalake = DatalakeGen2(self.imbalance_datalake_name, self.azure_cretential)
        self.shared_datalake_gen2 = DatalakeGen2(self.shared_datalake_gen2_name, self.azure_cretential)
        self.shared_datalake_gen1 = DatalakeGen1(self.shared_datalake_gen1_name, token)
