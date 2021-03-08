import os
import uuid
import boto3
from models import db, Album
from flask import g
from PIL import Image, UnidentifiedImageError
from decouple import config

BUCKET = config('AWS_BUCKET')
BUCKET_URL = config('AWS_OBJECT_URL')
ACCESS_KEY = config('AWS_ACCESS_KEY')
SECRET_KEY = config('AWS_API_SECRET')

s3 = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)


class MyAlbum():

    def __init__(self, path, ext):
        """Instantiate Image Class"""
        self.path = path
        self.ext = ext

    def validate_profile(self, images):
        """Handles changing of profile image of user"""
        try:
            # Remove current profile image stored
            if "default-icon.png" not in g.user.profile:
                s3key = g.user.profile("/")
                try:
                    s3.delete_object(Bucket=BUCKET, Key=s3key[3])
                except FileNotFoundError as error:
                    print("No image found!")

            # Resize profile image using pillow
            try:
                image = Image.open(images)
            except UnidentifiedImageError as error:
                image = Image.open(images.filename)
            image.thumbnail((400, 400))
            filename = str(uuid.uuid4().hex) + '.png'

            # Save temp image to local folder
            s3file = os.path.join(self.path + filename)
            image.save(s3file)

            # upload file to amazon s3
            s3.upload_file(
                Bucket=BUCKET,
                Filename=s3file,
                Key=filename
            )
            # Update database
            return BUCKET_URL + filename
        except:
            return BUCKET_URL + "default-icon.png"

    def validate_album(self, images):
        """Handles image upload for bluecollar album"""
        for image in images:

            # Resize image
            img = Image.open(image)
            img.thumbnail((1200, 1200))
            file_ext = os.path.splitext(image.filename)[1]
            filename = str(uuid.uuid4().hex) + file_ext

            # Save temp image to local folder
            s3file = os.path.join(self.path + filename)
            img.save(s3file)

            # Upload image to amazon s3
            s3.upload_file(
                Bucket=BUCKET,
                Filename=s3file,
                Key=filename
            )

            # add image link to database
            add_image = Album(
                filename=BUCKET_URL + filename,
                user_id=g.user.id
            )
            db.session.add(add_image)
            db.session.commit()
        return True

    def delete_image(filename):
        """Handles image deletion from Amazon S3"""

        try:
            s3key = filename.split('/')
            s3.delete_object(Bucket=BUCKET, Key=s3key[3])
            return True
        except:
            return False
