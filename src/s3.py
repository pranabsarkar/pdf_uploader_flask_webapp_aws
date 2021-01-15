import boto3


class SimpleStorage:
    def __init__(self) -> None:
        self.s3_client = boto3.client('s3')

    def upload(self, file_name, bucket_name, object):
        try:
            self.s3_client.upload_file(file_name, bucket_name, object)
        except Exception as e:
            print(e)
    