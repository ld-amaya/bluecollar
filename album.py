import os
import uuid
import sys
from models import db, Image
from flask import g


class Album():

    def __init__(self, path, ext):
        """Instantiate Image Class"""
        self.path = path
        self.ext = ext

    def validate_profile(self, images):
        """Handles changing of profile image of user"""
        try:
            file_ext = os.path.splitext(images.filename)[1]
            filename = str(uuid.uuid4().hex) + file_ext
            # Remove current profile image stored
            if not g.user.profile == "default-icon.png":
                try:
                    os.remove(self.path + g.user.profile)
                except FileNotFoundError as error:
                    print("No image found!")
            # Save image to folder
            images.save(os.path.join(self.path + filename))

            # Update database
            g.user.profile = filename
            db.session.add(g.user)
            db.session.commit()
            return True
        except:
            return False

    def validate_album(self, images):
        """Handles image upload for bluecollar album"""
        for image in images:
            # Upload image to folder
            file_ext = os.path.splitext(image.filename)[1]
            filename = str(uuid.uuid4().hex) + file_ext
            image.save(os.path.join(self.path + filename))
            # add image link to database
            album = Image(
                name=filename,
                user_id=g.user.id
            )
            db.session.add(album)
            db.session.commit()
        return True
