import boto3
from botocore.exceptions import ClientError


class minio_helper:
    def __init__(self, endpoint, access_key=None, secret_key=None, secure=True):
        self.client = boto3.resource(
            "s3",
            endpoint_url="http://127.0.0.1:9000",
            aws_access_key_id="minioadmin",
            aws_secret_access_key="miniopassword",
        )

    def bucket_exists(self, bucket_name):
        if self.client.Bucket(bucket_name) in self.client.buckets.all():
            # print(f'Bucket {bucket_name} exists.')
            return True
        else:
            # print(f'Bucket {bucket_name} does not exist.')
            return False

    def create_bucket(self, bucket_name):
        try:
            if not (self.bucket_exists(bucket_name=bucket_name)):
                bucket = self.client.create_bucket(Bucket=bucket_name)
                # print(f'Bucket {bucket_name} created successfully.')
            else:
                pass
                # print('bucket already exists')
        except Exception as e:
            print(f"Error creating bucket {bucket_name}: {str(e)}")

    def delete_bucket(self, bucket_name):
        try:
            self.client.Bucket(bucket_name).delete()
            # print(f'Bucket {bucket_name} deleted successfully.')
        except Exception as e:
            print(f"Error deleting bucket {bucket_name}: {str(e)}")

    def put_object(self, bucket, key, data):
        try:
            self.client.Object(bucket, key).put(Body=data)
            print(f"{key} uploaded successfully and available at {bucket}/{key}")
        except Exception as e:
            print(f"Error uploading object {key}: {str(e)}")

    def get_object(self, bucket, key):
        try:
            response = self.client.get_object(Bucket=bucket, Key=key)
            return response["Body"].read()
        except ClientError as e:
            # print(f"Error getting object '{key}' from MinIO: {e}")
            return None
