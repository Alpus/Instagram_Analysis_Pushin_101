import requests
from app import db
import models
import datetime


while True:
    #print 'new user'
    user = db.session.query(models.User).filter(models.User.access_token != None,
                                                 models.User.is_media_on_update == False)\
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
        #print 'process user'
        user.is_media_on_update = True
        db.session.commit()
        task = requests.update_user_media.delay(user.inst_id_user)
        #print 'waiting started'
        task.wait()
        print user.login + ' updated'
        #print 'waiting end'
