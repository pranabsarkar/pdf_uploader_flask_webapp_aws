from src.database import SimpleDatabase
from src.s3 import SimpleStorage
from src.config import Config
from src.email_interface import EmailInterface
import pandas as pd


class Process:
    def __init__(self) -> None:
        self.config = Config()
        self.email_process = EmailInterface()
        self.database_process = SimpleDatabase()
        self.storage_process = SimpleDatabase()

    def user_sign_up(self, *params):
        try:
            self.database_process.insert_item_into_user_db(
                user_name=params["username"],
                age=params["age"],
                gender=params["gender"],
                email_address=params["email_address"],
                password=params["password"],
            )
            txt_description = "Thank you for the registration. Your Credentials for login are Email: {} \
                and Password: {}".format(
                params["email_address"], password=params["password"]
            )
            self.email_process.send_mail(
                txt_description, params["email_address"], "Registration of Account"
            )
            new_dict = {
                "username": params["username"],
                "age": params["age"],
                "gender": params["gender"],
                "email_address": params["email_address"],
            }
            df = pd.DataFrame([new_dict])
            df.to_csv("temp.csv")
        except Exception as e:
            print(e)
