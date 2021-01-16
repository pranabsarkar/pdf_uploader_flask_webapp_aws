from src.config import Config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class EmailInterface:
    def __init__(self) -> None:
        self.config = Config()
        self.mime_multipart = MIMEMultipart()
        self.server = smtplib.SMTP("smtp.gmail.com: 587")

    def send_mail(self, message, to_email, sub_email):
        try:
            self.mime_multipart["From"] = self.config.email_id
            self.mime_multipart["To"] = to_email
            self.mime_multipart["Subject"] = sub_email
            self.mime_multipart.attach(MIMEText(message, "plain"))
            self.server.starttls()
            self.server.login(self.mime_multipart["From"], self.config.email_pass)
            self.server.sendmail(
                self.mime_multipart["From"],
                self.mime_multipart["To"],
                self.mime_multipart.as_string(),
            )
            self.server.quit()
        except Exception as e:
            print(e)
