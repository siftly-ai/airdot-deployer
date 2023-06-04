from google.cloud import storage
from google.oauth2 import service_account
from googleapiclient import discovery
from google import auth
from datetime import datetime, timedelta
import json
import pickle


file_ = open("/Users/abhinav.singh-mbp/Downloads/token.json", mode="rb").read()

private_json = json.loads(file_)

from pprint import pprint


def get_gcs_bucket(config):
    storage_client = storage.Client()
    return storage_client.bucket("gs://model-ml-deployer")


def generate_upload_signed_url_v4(bucket_name, blob_name):
    """Generates a v4 signed URL for uploading a blob using HTTP PUT.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    # bucket_name = 'your-bucket-name'
    # blob_name = 'your-object-name'

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=5),
        # Allow PUT requests using this URL.
        method="PUT",
        content_type="application/octet-stream",
    )

    return url


# credentials, project = auth.default(

# )
# credentials.refresh(auth.transport.requests.Request())

# credentials = service_account.Credentials.from_service_account_info(private_json)

# #credentials.refresh(auth.transport.requests.Request())


# expiration_timedelta = timedelta(minutes=3)

# storage_client = storage.Client(credentials=credentials)
# bucket = storage_client.bucket('model-ml-deployer')
# blob = bucket.blob("test-folder2/test_model.pkl")
# test_dict = {'test_key':'test_value'}
# file = pickle.dumps(test_dict)
# blob.upload_from_string(file)

# signed_url = blob.generate_signed_url(
#     expiration=expiration_timedelta,
#     service_account_email=credentials.service_account_email,
#     access_token=credentials.token,
# )

# print('signed url', signed_url)


# pickle.dump()


storage_client = storage.Client()
bucket = storage_client.bucket("model-ml-deployer")
blob = bucket.blob("116997773269197393190/lm.pkl")
lm = pickle.loads(blob.download_as_string())
