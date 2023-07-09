from google.cloud import storage
import pandas as pd
from io import BytesIO, StringIO


class gcs_utils:
    """
    Gcs helpers utility module. This module enables to perfrom
    operations on gcs [uploading, downloading, exists check, connecting to gcs bucket]
    """

    def _init_(self, gcs_uri) -> None:
        """
        Default constructor for gcs_utils modules

        Args:
            gcs_uri (str): gcs uri string for the blob
        """
        self.gcs_uri = gcs_uri
        self.bucket_name, self.blob_name = self.split_gcs_path(self.gcs_uri)
        self.bucket = self.connect_bucket()
        self.storage_client = storage.Client()

    def split_gcs_path(self, path):
        """
        Splits the gcs path into bucket name and blob uri string.

        Args:
            path (str): gcs uri string for the blob

        Returns:
            str : it returns two values for bucket name and blob name
        """
        bucket_name = path.split("//")[1].split("/")[0]
        blob_name = "/".join(path.split("//")[1].split("/")[1:])
        return bucket_name, blob_name

    def connect_bucket(self):
        """
        Connects to gcs bucket

        Returns:
            gcs bucket: gcs bucket connection
        """
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        return bucket

    def download_as_file_bytes(self, blob_name):
        """
        Downloads gcs files as bytes

        Args:
            gcs_uri (str): gcs uri for the blob to download

        Returns:
            bytes: data of the blob at gcs uri
        """
        blob = self.bucket.get_blob(blob_name)
        data = blob.download_as_bytes()
        return BytesIO(data)

    def check_gcs_blob_existence(self, gcs_uri):
        """
        checks if the blob exists at gcs uri

        Args:
            gcs_uri (str): gcs uri for the blob

        Returns:
            bool: True if Exists otherwise false
        """
        _, blob_name = self.split_gcs_path(gcs_uri)
        return storage.Blob(bucket=self.bucket, name=blob_name).exists(
            self.storage_client
        )

    def file_name_filter(self, name, blob_name):
        """
        checks if blob name starts with name

        Args:
            name (str):name string that needs to be checked
            blob_name (str): string that needs to be present in name

        Returns:
            bool: True if blob name starts with name otherwise False
        """
        return name.startswith(blob_name)

    def get_file_list(self):
        """
        returns list of files inside a bucket

        Returns:
            list: returns list of files name that starts with blob names in bucket.
        """
        blobs = self.storage_client.list_blobs(self.bucket_name)
        files = [
            blob.name
            for blob in blobs
            if self.file_name_filter(blob.name, self.blob_name)
        ]
        return sorted(files)

    def download_file_as_string(self, blob_name):
        """
        Downloads gcs files as string

        Args:
            gcs_uri (str): gcs uri for the blob to download

        Returns:
            str: data of the blob at gcs uri
        """
        blob = self.bucket.get_blob(blob_name)
        file = blob.download_as_string()
        return StringIO(file)

    def put_objects(self, data, gcs_uri):
        """
        Uploads file to desired gcs_uri

        Args:
            data (object): data that needs to be uploaded.
            gcs_uri (str): gcs uri at which DataFrame needs to be dumped.
        """
        bucket_name, blob_name = self.split_gcs_path(gcs_uri)
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(data)
        return True
