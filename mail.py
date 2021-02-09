import smtplib
import ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email():

    def __init__(self, user_email):
        self.user_email = user_email
        self.port = 445
        self.email = "rakteroconfirmation@gmail.com"
        self.password = input('Ad0bZmpqCo1YSRvw')

    def VerifyMail(self):

        message = MIMEMultipart("alternative")

        # Create secure SSL Text
        context = ssl.create_default_context()
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=context) as server:
            # Compose Email
            message["Subject"] = "Email Verification form raketraket.com"
            message["From"] = self.email
            message["To"] = self.user_email

            email_body = """\
            <html >
                <body >
                        <p > Hi Lou < /p >
                        <p > This is a test to link < a href = "https://phstudies.com" > PH Studies < /a > </p >
                    </body>
                </html>
                """
            body = MIMEText(email_body, "html")
            message.attach(body)

            # Server Login
            server.login(self.email, self.password)

            # Send Email
            server.sendmail(self.email, self.user_email, message.as_string())
