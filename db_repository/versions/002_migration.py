#!flask/bin/python
from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Medias = Table('Medias', pre_meta,
               Column('id_media', INTEGER, primary_key=True, nullable=False),
               Column('inst_id_media', VARCHAR(length=50), nullable=False),
               Column('type_media', VARCHAR(length=50), nullable=False),
               Column('caption', VARCHAR(length=100), nullable=False),
               Column('filter_media', VARCHAR(length=50), nullable=False),
               Column('link', VARCHAR(length=255), nullable=False),
               Column('created_time', DATETIME, nullable=False),
               Column('image_low', VARCHAR(length=255), nullable=False),
               Column('image_thumbnail', VARCHAR(length=255), nullable=False),
               Column('image_standart', VARCHAR(length=255), nullable=False),
               Column('id_user', INTEGER),
               Column('id_location', INTEGER),
               )

Medias = Table('Medias', post_meta,
               Column('id_media', Integer, primary_key=True, nullable=False),
               Column('inst_id_media', String(length=50), nullable=False),
               Column('type_media', String(length=50), nullable=False),
               Column('caption', String(length=100), nullable=False),
               Column('filter_media', String(length=50), nullable=False),
               Column('link', String(length=255), nullable=False),
               Column('created_time', DateTime, nullable=False),
               Column('image_low', String(length=255), nullable=False),
               Column('image_thumbnail', String(length=255), nullable=False),
               Column('image_standard', String(length=255), nullable=False),
               Column('id_user', Integer),
               Column('id_location', Integer),
               )


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Medias'].columns['image_standart'].drop()
    post_meta.tables['Medias'].columns['image_standard'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Medias'].columns['image_standart'].create()
    post_meta.tables['Medias'].columns['image_standard'].drop()
