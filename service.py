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

        # Get carpenter id
        cid = Service.query.filter(Service.name == 'Carpenter').first()
        if self.carpenter:
            carpenter = User_Service(
                user_id=user_id,
                service_id=cid.id
            )
            db.session.add(carpenter)

        # Get painter id
        pid = Service.query.filter(Service.name == 'Painter').first()
        if self.painter:
            painter = User_Service(
                user_id=user_id,
                service_id=pid.id
            )
            db.session.add(painter)

        # Get plumber id
        plid = Service.query.filter(Service.name == 'Plumber').first()
        if self.plumber:
            plumber = User_Service(
                user_id=user_id,
                service_id=plid.id
            )
            db.session.add(plumber)

        # Get plumber id
        eid = Service.query.filter(Service.name == 'Electrician').first()
        if self.electrician:
            electrician = User_Service(
                user_id=user_id,
                service_id=eid.id
            )
            db.session.add(electrician)

        db.session.commit()
