# -*- coding: utf-8 -*-
from app import db
import models
import datetime


class Ordered_liker:
    def __init__(self, number, user, count_of_likes):
        self.number = number + 1
        self.user = user
        self.count_of_likes = count_of_likes

class Ordered_media:
    def __init__(self, number, media):
        self.number = number + 1
        self.media = media

class Ordered_tag:
    def __init__(self, number, tag, count_of_media, average_count_of_likes, best_media):
        self.number = number + 1
        self.tag = tag
        self.count_of_media = count_of_media
        self.average_count_of_likes = average_count_of_likes
        self.best_media = best_media


class Ordered_filter:
    def __init__(self, number, filter_name, count_of_media, average_count_of_likes, best_media):
        self.number = number + 1
        self.filter_name = filter_name
        self.count_of_media = count_of_media
        self.average_count_of_likes = average_count_of_likes
        self.best_media = best_media


class Ordered_location:
    def __init__(self, number, location, count_of_media, average_count_of_likes, best_media):
        self.number = number + 1
        self.location = location
        self.count_of_media = count_of_media
        self.average_count_of_likes = average_count_of_likes
        self.best_media = best_media


class Ordered_user:
    def __init__(self, number, user):
        self.number = number + 1
        self.user = user



class User_information:
    def __init__(self, user, medias=None, followed_by=None, follows=None,
                 likers=None, sum_of_likes=None, count_of_likers=None,
                 median_like_count=None, most_liked_medias=None,
                 tags=None, count_of_all_tags=None,
                 count_of_unique_tags=None, filters=None,
                 count_of_filters=None, locations=None,
                 count_of_all_locations=None,
                 count_of_unique_locations=None):
        self.user = user
        self.medias = medias
        self.followed_by = followed_by
        self.follows = follows
        self.likers = likers
        self.sum_of_likes = sum_of_likes
        self.count_of_likers = count_of_likers
        self.median_like_count = median_like_count
        self.most_liked_medias = most_liked_medias
        self.tags = tags
        self.count_of_all_tags = count_of_all_tags
        self.count_of_unique_tags = count_of_unique_tags
        self.filters = filters
        self.count_of_filters = count_of_filters
        self.locations = locations
        self.count_of_all_locations = count_of_all_locations
        self.count_of_unique_locations = count_of_unique_locations
        if sum_of_likes is not None and user.count_media is not 0:
            self.average_like_count = float(sum_of_likes) / user.count_media
        else:
            self.average_like_count = None
        if user.last_check <= datetime.datetime(year=1814, month=7, day=19):
            self.ready_to_show=False
        else:
            self.ready_to_show=True


def get_users_who_liked(medias, user, followed_by):
    users_who_liked = {}
    sum_of_likes = 0

    possible_user_likes = {x:0 for x in followed_by}

    medias_with_extra_likes = user.medias.filter(models.Media.count_of_likes > 120).count()

    for follower in followed_by:
        possible_user_likes[follower] += medias_with_extra_likes

    for media in medias:
        sum_media_likes = 0
        for liker in media.liked_by:
            if liker not in users_who_liked:
                users_who_liked[liker] = 1
            else:
                users_who_liked[liker] += 1
            sum_media_likes += 1
            if liker in possible_user_likes and \
                            media.count_of_likes > 120:
                possible_user_likes[liker] -= 1

        sum_of_likes += sum_media_likes

    possible_user_likes = possible_user_likes.items()
    #possible_user_likes.sort(key=lambda x: (x[1], x[0].login))
    if user.count_media is not 0:
        for liker in possible_user_likes:
            if liker[0] in users_who_liked:
                extra_likes = liker[1] * (users_who_liked[liker[0]] / user.count_media)
                #if medias_with_extra_likes:
                #    extra_likes = int(extra_likes * (count_of_extra_likes / (medias_with_extra_likes * len(followed_by))))
                users_who_liked[liker[0]] += extra_likes

    likers = [Ordered_liker(number=number, user=liker[0], count_of_likes=liker[1])
              for number, liker in
              enumerate(sorted(users_who_liked.items(),
                               key=lambda liker: (-liker[1], liker[0].login)))]

    count_of_likers = len(likers)
    median_like_count = sorted(medias, key=lambda x: (-x.count_of_likes))[len(medias) / 2].count_of_likes
    return likers, sum_of_likes, count_of_likers, median_like_count


def get_most_liked_medias(medias):
    most_liked_medias = [Ordered_media(number, media) for number, media in enumerate(medias)]
    return most_liked_medias


def get_tags(medias):
    user_tags = {}
    count_of_all_tags = 0
    for media in medias:
        for tag in media.tags:
            if tag not in user_tags:
                user_tags[tag] = [1, media.count_of_likes, media]
            else:
                user_tags[tag][0] += 1
                user_tags[tag][1] += media.count_of_likes
                if media.count_of_likes > user_tags[tag][2].count_of_likes:
                    user_tags[tag][2] = media
            count_of_all_tags += 1
    user_tags = [Ordered_tag(number=number, tag=tag[0], count_of_media=tag[1][0],
                             average_count_of_likes=float(tag[1][1])/tag[1][0], best_media=tag[1][2]) for number, tag in
                 enumerate(sorted(user_tags.items(), key=lambda tag: (-tag[1][0], tag[0].name)))]
    count_of_unique_tags = len(user_tags)
    return user_tags, count_of_all_tags, count_of_unique_tags


def get_filter(medias):
    user_filters = {}
    for media in medias:
        filter = media.filter_media
        if filter not in user_filters:
            user_filters[filter] = [1, media.count_of_likes, media]
        else:
            user_filters[filter][0] += 1
            user_filters[filter][1] += media.count_of_likes
            if media.count_of_likes > user_filters[filter][2].count_of_likes:
                user_filters[filter][2] = media
    user_filters = [Ordered_filter(number=number, filter_name=filter[0], count_of_media=filter[1][0],
                             average_count_of_likes=float(filter[1][1])/filter[1][0],
                                best_media=filter[1][2]) for number, filter in
                 enumerate(sorted(user_filters.items(), key=lambda filter: (-filter[1][0], filter[0])))]
    count_of_filters = len(user_filters)
    return user_filters, count_of_filters


def get_locations(medias):
    user_locations = {}
    count_of_all_locations = 0
    for media in medias:
        location = media.location
        if location not in user_locations:
            user_locations[location] = [1, media.count_of_likes, media]
        else:
            user_locations[location][0] += 1
            user_locations[location][1] += media.count_of_likes
            if media.count_of_likes > user_locations[location][2].count_of_likes:
                user_locations[location][2] = media
        count_of_all_locations += 1
    user_locations = [Ordered_location(number=number, location=location[0], count_of_media=location[1][0],
                             average_count_of_likes=float(location[1][1])/location[1][0],
                                  best_media=location[1][2]) for number, location in
                 enumerate(sorted(user_locations.items(), key=lambda location: (-location[1][0], location[0])))]
    count_of_unique_locations = len(user_locations)
    return user_locations, count_of_all_locations, count_of_unique_locations


def get_user_information(user_id):
    user = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    if user.last_check <= datetime.datetime(year=1814, month=7, day=19):
        return User_information(user=user)

    medias = user.medias.order_by(models.Media.count_of_likes.desc()).all()
    followed_by = user.followed_by
    follows = user.follows
    likers, sum_of_likes, count_of_likers, \
    median_like_count = get_users_who_liked(medias=medias, user=user, followed_by=followed_by)
    most_liked_medias = get_most_liked_medias(medias=medias)
    tags, count_of_all_tags, count_of_unique_tags = get_tags(medias=medias)
    filters, count_of_filters = get_filter(medias=medias)
    locations, count_of_all_locations,\
    count_of_unique_locations = get_locations(medias)

    return User_information(user=user, medias=medias,followed_by=followed_by,
                            follows=follows, likers=likers, sum_of_likes=sum_of_likes,
                            count_of_likers=count_of_likers, median_like_count=median_like_count,
                            most_liked_medias=most_liked_medias, tags=tags,
                            count_of_all_tags=count_of_all_tags, count_of_unique_tags=count_of_unique_tags,
                            filters=filters, count_of_filters=count_of_filters,
                            locations=locations, count_of_all_locations=count_of_all_locations,
                            count_of_unique_locations=count_of_unique_locations)

def get_top_users():
    users = \
        db.session.query(models.User).filter(models.User.access_token != None)\
            .order_by(models.User.count_media.desc()).all()
    top_users = [Ordered_user(number=number, user=user) for number, user in enumerate(users)]
    return top_users

def is_user_ready_to_show(user_id):
    user = \
        db.session.query(models.User).filter(models.User.inst_id_user ==
                                             user_id).first()
    if user.last_check <= datetime.datetime(year=1814, month=7, day=19):
        return False
    else:
        return True
