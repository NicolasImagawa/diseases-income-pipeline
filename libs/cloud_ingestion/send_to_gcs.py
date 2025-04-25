import os
from google.cloud import storage
from google.oauth2 import service_account

def upload_files():
    FILE_NAMES = os.listdir("./data/clean") #It assumes there are no other folders inside the given path.

    BUCKET_NAME = "diseases-and-income-us-nimagawa"
    CRED_PATH = "./credentials.json"
    credentials = service_account.Credentials.from_service_account_file(CRED_PATH,scopes=['https://www.googleapis.com/auth/cloud-platform'])
    CHUNK_SIZE = 262144 #Minimum chunksize allowed

    for file in FILE_NAMES:
        try:
            upload_blob(BUCKET_NAME, file, credentials, CHUNK_SIZE)
        except PermissionError:
            print(f"ERROR - Permission denied, please check if the administrador gave you the correct permissions for this operation.")
        except FileNotFoundError:
            print(f"ERROR - {file} not found, please check the script or the folder path for possible errors.")
        except Exception as error:
            print(f"ERROR - The following error has occurred:\n {error}\n")

def upload_blob(bucket_name, file_name, credentials, CHUNK_SIZE):
    #"""Uploads a file to the bucket."""
    path = "./data/clean/"
    # The ID of your GCS bucket
    bucket_name = bucket_name
    # The path to your file to upload
    source_file_path = f"{path}{file_name}"
    # The ID of your GCS object
    destination_blob_name = file_name

    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name, chunk_size=CHUNK_SIZE)

    generation_match_precondition = 0

    blob.upload_from_filename(source_file_path, if_generation_match=generation_match_precondition)

    print(
        f"File {file_name} uploaded as {destination_blob_name}."
    )

if __name__ == "__main__":
    upload_files()
