from models import User_Service
from models import db, Service


class ServiceType():
    def __init__(self, job):
        """Instantiate Service Type"""
        self.carpenter = job.carpenter.data
        self.painter = job.painter.data
        self.electrician = job.electrician.data
        self.plumber = job.plumber.data

    def Add_Services(self, user_id, services=""):
        """handles additional bluecollar services"""

        # delete existing service/s first then add new service/s

        for s in services:
            db.session.delete(s)
        if self.carpenter:
            carpenter = User_Service(
                user_id=user_id,
                service_id=1
            )
            db.session.add(carpenter)

        if self.painter:
            painter = User_Service(
                user_id=user_id,
                service_id=2
            )
            db.session.add(painter)

        if self.plumber:
            plumber = User_Service(
                user_id=user_id,
                service_id=3
            )
            db.session.add(plumber)

        if self.electrician:
            electrician = User_Service(
                user_id=user_id,
                service_id=4
            )
            db.session.add(electrician)

        db.session.commit()
