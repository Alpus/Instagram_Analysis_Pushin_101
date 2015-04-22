from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
inst_profiles = Table('inst_profiles', post_meta,
    Column('id_user', Integer, primary_key=True, nullable=False),
    Column('access_token', String(length=100)),
    Column('login', String(length=100), nullable=False),
    Column('full_name', String(length=100), nullable=False),
    Column('profile_picture', String(length=100)),
    Column('bio', String(length=100)),
    Column('website', String(length=100)),
    Column('registration_date', DateTime, nullable=False),
    Column('last_visit', DateTime, nullable=False),
    Column('rating', Integer, nullable=False, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['inst_profiles'].columns['last_visit'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['inst_profiles'].columns['last_visit'].drop()
