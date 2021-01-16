import boto3
import datetime
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key


class SimpleDatabase:
    def __init__(self) -> None:
        self.db_client = boto3.resource("dynamodb", region_name="us-east-1")

    def insert_item_into_storage_db(self, **params):
        try:
            table = self.db_client.Table("storage_db")
            table.put_item(
                Item={
                    "s3_key_name": params["s3_key_name"],
                    "original_name": params["original_name"],
                    "created_time": str(datetime.datetime.now()),
                }
            )
        except ClientError as e:
            print(e)

    def search_item_user_db(self, **params):
        try:
            table = self.db_client.Table("user_db")
            result = table.query(
                KeyConditionExpression=Key("email_address").eq(params["email_address"])
            )
        except ClientError as e:
            print(e)
        else:
            return result["Items"][0]

    def insert_item_into_user_db(self, **params):
        try:
            table = self.db_client.Table("user_db")
            table.put_item(
                Item={
                    "user_name": params["user_name"],
                    "age": params["age"],
                    "gender": params["gender"],
                    "email_address": params["email_address"],
                    "password": params["password"],
                }
            )
        except ClientError as e:
            print(e)
