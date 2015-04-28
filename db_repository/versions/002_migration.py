from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Comments = Table('Comments', post_meta,
    Column('id_comment', String(length=100), primary_key=True, nullable=False),
    Column('created_time', String(length=100), nullable=False),
    Column('text', String(length=100), nullable=False),
    Column('id_media', String(length=100)),
    Column('id_user', String(length=100)),
)

Medias = Table('Medias', post_meta,
    Column('id_media', String(length=100), primary_key=True, nullable=False),
    Column('type_media', String(length=100), nullable=False),
    Column('caption', String(length=100), nullable=False),
    Column('filter_media', String(length=100), nullable=False),
    Column('link', String(length=100), nullable=False),
    Column('created_time', String(length=100), nullable=False),
    Column('image_low', String(length=100), nullable=False),
    Column('image_thumbnail', String(length=100), nullable=False),
    Column('image_standart', String(length=100), nullable=False),
    Column('id_user', String(length=100)),
    Column('id_location', String(length=100)),
)

Tags = Table('Tags', post_meta,
    Column('id_tag', Integer, primary_key=True, nullable=False),
    Column('count', Integer, nullable=False),
    Column('name', String(length=100), nullable=False),
)

likes = Table('likes', post_meta,
    Column('id_media', String(length=100)),
    Column('id_user', String(length=100)),
)

location = Table('location', post_meta,
    Column('id_location', String(length=100), primary_key=True, nullable=False),
    Column('name', String(length=100), nullable=False),
    Column('latitude', Float, nullable=False),
    Column('longitude', Float, nullable=False),
)

marks = Table('marks', post_meta,
    Column('id_media', String(length=100)),
    Column('id_user', String(length=100)),
)

media_tags = Table('media_tags', post_meta,
    Column('id_media', String(length=100)),
    Column('id_tag', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Comments'].create()
    post_meta.tables['Medias'].create()
    post_meta.tables['Tags'].create()
    post_meta.tables['likes'].create()
    post_meta.tables['location'].create()
    post_meta.tables['marks'].create()
    post_meta.tables['media_tags'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Comments'].drop()
    post_meta.tables['Medias'].drop()
    post_meta.tables['Tags'].drop()
    post_meta.tables['likes'].drop()
    post_meta.tables['location'].drop()
    post_meta.tables['marks'].drop()
    post_meta.tables['media_tags'].drop()
