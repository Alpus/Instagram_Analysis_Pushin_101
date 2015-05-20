# -*- coding: utf-8 -*-
from app import db
import models


def get_users_who_liked(user_id):
    user_temp = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    medias = user_temp.medias.all()
    users_who_liked = {}
    sum_of_likes = 0
    for media in medias:
        for user in media.liked_by:
            if user not in users_who_liked:
                users_who_liked[user] = 1
            else:
                users_who_liked[user] += 1
            sum_of_likes += 1
    users_who_liked = users_who_liked.items()
    users_who_liked.sort(key=lambda x: (-x[1], x[0].login))
    liker_count = len(users_who_liked)
    return users_who_liked, sum_of_likes, liker_count


def get_most_liked_media(user_id):
    user_temp = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    most_liked_media = user_temp.medias.all()
    most_liked_media.sort(key=lambda x: -x.count_of_likes)
    return most_liked_media


def get_user_tags(user_id):
    user_temp = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    medias = user_temp.medias.all()
    user_tags = {}
    tag_count_all = 0
    for media in medias:
        for tag in media.tags:
            if tag not in user_tags:
                user_tags[tag] = 1
            else:
                user_tags[tag] += 1
            tag_count_all += 1
    user_tags = user_tags.items()
    user_tags.sort(key=lambda x: (-x[1], x[0].name))
    tag_count_unique = len(user_tags)
    return user_tags, tag_count_all, tag_count_unique


def get_tags_likes(user_id):
    user_temp = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    medias = user_temp.medias.all()
    tags_likes = {}
    for media in medias:
        for tag in media.tags:
            if tag not in tags_likes:
                tags_likes[tag] = [1, media.count_of_likes]
            else:
                tags_likes[tag][0] += 1
                tags_likes[tag][1] += media.count_of_likes
    for tag in tags_likes:
        tags_likes[tag] = float(tags_likes[tag][1]) / float(tags_likes[tag][0])
    tags_likes = tags_likes.items()
    tags_likes.sort(key=lambda x: (-x[1], x[0].name))
    tag_count_unique = len(tags_likes)
    return tags_likes
