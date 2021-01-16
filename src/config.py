import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.init_app()

    def init_app(self):
        self.app_env = "dev"
        if "APP_ENV" in os.environ:
            self.app_env = os.environ.get("APP_ENV")

        self.app_name = "sample-app"
        if "APP_NAME" in os.environ:
            self.app_name = os.environ.get("APP_NAME")

        self.state = None
        if "STATE" in os.environ:
            self.state = os.environ.get("STATE")

        self.aws_region = "ap-south-1"
        if "AWS_REGION" in os.environ:
            self.aws_region = os.environ.get("AWS_REGION")

        self.aws_key = None
        self.aws_secret = None
        if "AWS_KEY" in os.environ:
            self.app_key = os.environ.get("AWS_KEY")
            self.aws_secret = os.environ.get("AWS_SECRET")

        self.s3_bucket_name = "sample-app"
        if "S3_BUCKET" in os.environ:
            self.s3_bucket_name = os.environ.get("S3_BUCKET")

        self.email_id = "sample-user@gmail.com"
        if "EMAIL_ID" in os.environ:
            self.email_id = os.environ.get("EMAIL_ID")

        self.email_pass = "sample-app-pass"
        if "EMAIL_PASS" in os.environ:
            self.email_pass = os.environ.get("EMAIL_PASS")
