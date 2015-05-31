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

    #medias_with_extra_likes = 0
    medias_with_extra_likes = user_temp.medias.filter(models.Media.count_of_likes > 120).count()
    #count_of_extra_likes = 0
    #for media in medias:
        #if media.count_of_likes > 120:
            #medias_with_extra_likes += 1
            #count_of_extra_likes += media.count_of_likes - 120

    for user in followed_by:
        possible_user_likes[user] += medias_with_extra_likes

    for media in medias:
        sum_media_likes = 0
        for user in media.liked_by:
            if user not in users_who_liked:
                users_who_liked[user] = 1
            else:
                users_who_liked[user] += 1
            sum_media_likes += 1
            if user in possible_user_likes and \
                            media.count_of_likes > 120:
                possible_user_likes[user] -= 1

        sum_of_likes += sum_media_likes

    possible_user_likes = possible_user_likes.items()
    #possible_user_likes.sort(key=lambda x: (x[1], x[0].login))
    if user_temp.count_media is not 0:
        for liker in possible_user_likes:
            if liker[0] in users_who_liked:
                extra_likes = liker[1] * (users_who_liked[liker[0]] / user_temp.count_media)
                #if medias_with_extra_likes:
                #    extra_likes = int(extra_likes * (count_of_extra_likes / (medias_with_extra_likes * len(followed_by))))
                users_who_liked[liker[0]] += extra_likes

    users_who_liked = users_who_liked.items()
    users_who_liked.sort(key=lambda x: (-x[1], x[0].login))

    liker_count = len(users_who_liked)
    medias.sort(key=lambda x: (-x.count_of_likes))
    median_like_count = medias[len(medias) / 2].count_of_likes
    return users_who_liked[:50], sum_of_likes, liker_count, median_like_count


def get_most_liked_media(user_id):
    user_temp = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    most_liked_media = user_temp.medias.all()
    most_liked_media.sort(key=lambda x: -x.count_of_likes)
    return most_liked_media[:50]


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
    return user_tags[:50], tag_count_all, tag_count_unique


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
        tags_likes[tag] = float(tags_likes[tag][1]) / tags_likes[tag][0]
    tags_likes = tags_likes.items()
    tags_likes.sort(key=lambda x: (-x[1], x[0].name))
    return tags_likes[:50]


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


def get_user_filter(user_id):
     user_temp = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
     medias = user_temp.medias
     user_filters = {}
     for media in medias:
         if media.filter_media not in user_filters:
             user_filters[media.filter_media] = 1
         else:
             user_filters[media.filter_media] += 1
     user_filters = user_filters.items()
     user_filters.sort(key=lambda x: (-x[1], x[0]))
     filter_count = len(user_filters)
     return user_filters[:50], filter_count


def get_filters_likes(user_id):
    user_temp = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    medias = user_temp.medias
    filter_likes = {}
    for media in medias:
        if media.filter_media not in filter_likes:
            filter_likes[media.filter_media] = [1, media.count_of_likes, media]
        else:
            filter_likes[media.filter_media][0] += 1
            filter_likes[media.filter_media][1] += media.count_of_likes
            if (filter_likes[media.filter_media][2].count_of_likes < media.count_of_likes):
                filter_likes[media.filter_media][2] = media
    for filter in filter_likes:
        filter_likes[filter] = [float(filter_likes[filter][1]) / filter_likes[filter][0], filter_likes[filter][2]]
    filter_likes = filter_likes.items()
    filter_likes.sort(key=lambda x: (-x[1][0], x[0]))
    return filter_likes[:50]


def get_user_location(user_id):
     user_temp = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
     medias = user_temp.medias
     user_locations = {}
     location_count_all = 0
     for media in medias:
         if media.location is not None:
             if media.location not in user_locations:
                 user_locations[media.location] = 1
             else:
                 user_locations[media.location] += 1
             location_count_all += 1
     user_locations = user_locations.items()
     user_locations.sort(key=lambda x: (-x[1], x[0].name))
     location_count_unique = len(user_locations)
     return user_locations[:50], location_count_all, location_count_unique


def get_locations_likes(user_id):
    user_temp = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    medias = user_temp.medias
    location_likes = {}
    for media in medias:
        if media.location is not None:
            if media.location not in location_likes:
                location_likes[media.location] = [1, media.count_of_likes, media]
            else:
                location_likes[media.location][0] += 1
                location_likes[media.location][1] += media.count_of_likes
                if (location_likes[media.location][2].count_of_likes < media.count_of_likes):
                    location_likes[media.location][2] = media
    for location in location_likes:
        location_likes[location] = [float(location_likes[location][1]) / location_likes[location][0],
                                    location_likes[location][2]]
    location_likes = location_likes.items()
    location_likes.sort(key=lambda x: (-x[1][0], x[0].name))
    return location_likes[:50]


