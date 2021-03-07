import os
from mailjet_rest import Client
from flask import current_app as app

api_key = '6282c9420fb0509aa854b43b4a1fd188'
api_secret = 'c43f72aafabf6c3c7055947545b5da39'


class Mail():

    def __init__(self, email, first_name):
        self.email = email
        self.first_name = first_name

    def send_confirmation_email(self, token):
        """Handles sending of email"""

        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "raket@phstudies.com",
                        "Name": "Raket"
                    },
                    "To": [
                        {
                            "Email": self.email,
                            "Name": self.first_name
                        }
                    ],
                    "Subject": "Greetings from Raketraket.com",
                    "TextPart": "Thank you for signing up.",
                    "HTMLPart": f"<p> Please click the link below to activate your account </p> <form action = 'https://raketraket.herokuapp.com/confirm/email/{token}' method = 'POST'> <button type = 'submit'> Activate Email!</button></form>",
                    "CustomID": "AppGettingStartedTest"
                }
            ]
        }

        result = mailjet.send.create(data=data)
        return result.status_code
