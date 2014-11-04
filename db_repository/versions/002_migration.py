from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
bark = Table('bark', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('barkBody', String(length=140)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nickname', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
    Column('firstName', VARCHAR),
    Column('lastName', VARCHAR),
    Column('password', VARCHAR),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['bark'].create()
    pre_meta.tables['user'].columns['nickname'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['bark'].drop()
    pre_meta.tables['user'].columns['nickname'].create()
