import requests
from app import db
from app import celery
import models
import datetime


def update_users_media():
    while True:
        user = db.session.query(models.User).filter(models.User.access_token != None,
                                                     models.User.is_media_on_update == False)\
                                                     .order_by(models.User.last_check).first()
        if user.last_check is None:
            user.last_check = datetime.date(year=1814, month=7, day=19)
            db.session.commit()
        if datetime.datetime.now() - user.last_check > datetime.timedelta(hours=24):
            user.is_media_on_update = True;
            db.session.commit()
            requests.update_user_media.delay(user.inst_id_user).wait()
