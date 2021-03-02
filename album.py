import os
import uuid
from models import db, Album
from flask import g
from PIL import Image, UnidentifiedImageError


class MyAlbum():

    def __init__(self, path, ext):
        """Instantiate Image Class"""
        self.path = path
        self.ext = ext

    def validate_profile(self, images):
        """Handles changing of profile image of user"""
        try:
            # Remove current profile image stored
            if not g.user.profile == "default-icon.png":
                try:
                    os.remove(self.path + g.user.profile)
                except FileNotFoundError as error:
                    print("No image found!")

            # Resize profile image using pillow
            try:
                image = Image.open(images)
            except UnidentifiedImageError as error:
                image = Image.open(images.filename)
            image.thumbnail((400, 400))
            filename = str(uuid.uuid4().hex) + '.png'

            # Save image to folder
            image.save(os.path.join(self.path + filename))

            # Update database
            return filename
        except:
            return "default-icon.png"

    def validate_album(self, images):
        """Handles image upload for bluecollar album"""
        for image in images:

            # Resize image
            img = Image.open(image)
            img.thumbnail((1200, 1200))
            file_ext = os.path.splitext(image.filename)[1]
            filename = str(uuid.uuid4().hex) + file_ext
            img.save(os.path.join(self.path + filename))

            # add image link to database
            add_image = Album(
                filename=filename,
                user_id=g.user.id
            )
            db.session.add(add_image)
            db.session.commit()
        return True
