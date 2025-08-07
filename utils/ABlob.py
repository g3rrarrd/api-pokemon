import os
import re
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_SAK")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")

class ABlob:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        self.container_client = self.blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER)

        self.account_name = self.blob_service_client.account_name
        self.account_key = re.search(r'AccountKey=([^;]+)', AZURE_STORAGE_CONNECTION_STRING).group(1)

    def generate_sas(self, id: int):
        blob_name = f"poke_reporte_{id}.csv"
        sas_token = generate_blob_sas(
            account_name=self.account_name,
            container_name=AZURE_STORAGE_CONTAINER,
            blob_name=blob_name,
            account_key=self.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=24)
        )
        
        url = f"https://{self.account_name}.blob.core.windows.net/{AZURE_STORAGE_CONTAINER}/{blob_name}?{sas_token}"
        return url
    
    def delete_blob(self, id: int):
        blob_name = f"poke_reporte_{id}.csv"
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.delete_blob()

