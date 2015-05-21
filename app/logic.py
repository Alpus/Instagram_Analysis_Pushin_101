# -*- coding: utf-8 -*-
from app import db
import models


def get_users_who_liked(user_id):
    user_temp = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    medias = user_temp.medias.all()
    followed_by = user_temp.followed_by
    users_who_liked = {}
    sum_of_likes = 0

    possible_user_likes = {x:0 for x in followed_by}
    for media in medias:
        for user in followed_by:
            if media.count_of_likes > 120:
                possible_user_likes[user] += 1

    for media in medias:
        sum_media_likes = 0
        for user in media.liked_by:
            if user not in users_who_liked:
                users_who_liked[user] = 1
            else:
                users_who_liked[user] += 1
            sum_media_likes += 1
            if user in possible_user_likes:
                possible_user_likes[user] -= 1

        sum_of_likes += sum_media_likes

    possible_user_likes = possible_user_likes.items()
    possible_user_likes.sort(key=lambda x: (x[1], x[0].login))
    for liker in possible_user_likes:
        if liker[0] in users_who_liked:
            users_who_liked[liker[0]] += liker[1] * (users_who_liked[liker[0]] // user_temp.count_media)

    users_who_liked = users_who_liked.items()
    users_who_liked.sort(key=lambda x: (-x[1], x[0].login))

    liker_count = len(users_who_liked)
    medias.sort(key=lambda x: (-x.count_of_likes))
    median_like_count = medias[len(medias) // 2].count_of_likes
    return users_who_liked, sum_of_likes, liker_count, median_like_count


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
        tags_likes[tag] = tags_likes[tag][1] / tags_likes[tag][0]
    tags_likes = tags_likes.items()
    tags_likes.sort(key=lambda x: (-x[1], x[0].name))
    return tags_likes


def get_follows(user_id):
    user_temp = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    user_follows = user_temp.follows.all()
    return user_follows


def get_followed_by(user_id):
    user_temp = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    user_followed_by = user_temp.followed_by
    return user_followed_by