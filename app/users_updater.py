import requests
from app import db
import models
import datetime


while True:
    #print 'new user'
    user = db.session.query(models.User).filter(models.User.access_token != None,
                                                 models.User.is_media_on_update == 0)\
                                                 .order_by(models.User.last_check).first()
    db.session.commit()
    #print user.login
    #print user.last_check
    #print datetime.datetime.now() - user.last_check > datetime.timedelta(hours=24)
    #print user.access_token
    #print requests.is_access_token_valid(user.inst_id_user)
    if user.last_check is None:
        user.last_check = datetime.date(year=1814, month=7, day=19)
        db.session.commit()
    if datetime.datetime.now() - user.last_check > datetime.timedelta(hours=24) and\
        requests.is_access_token_valid(user.inst_id_user):
        print user.login + ' started'
        user.is_media_on_update += 3
        db.session.commit()

        task_followed_by = requests.update_user_followed_by.delay(user.inst_id_user)
        print 'Followed by started'
        task_follows = requests.update_user_follows.delay(user.inst_id_user)
        print 'Follows started'
        task_media = requests.update_user_media.delay(user.inst_id_user)
        print 'Medias by started'

        task_followed_by.wait()
        print 'Followed by ended'
        task_follows.wait()
        print 'Follows ended'
        task_media.wait()
        print 'Medias ended'

        db.session.commit()
        print user.login + ' updated \n \n'
        #print 'waiting end'
