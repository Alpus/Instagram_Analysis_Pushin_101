import requests
from app import db
from app import celery
import models
import datetime


def update_users_media():
    while True:
        user = db.session.query(models.User).order_by(models.User.last_check)
        if user.last_check is None:
            user.last_check = datetime.date(year=1814, month=7, day=19)
            db.session.commit()
        if user.is_media_on_update is False and datetime.datetime.now() - user.last_check >\
                datetime.timedelta(hours=24) and requests.is_access_token_valid(user.inst_id_user):
            user.is_media_on_update = True;
            db.session.commit()
            task = requests.update_user_media.delay(user.inst_id_user)
            task.wait()

