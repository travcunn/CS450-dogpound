from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
friend = Table('friend', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id1', INTEGER),
    Column('user_id2', INTEGER),
)

friends = Table('friends', post_meta,
    Column('friender_id', Integer),
    Column('friendee_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['friend'].drop()
    post_meta.tables['friends'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['friend'].create()
    post_meta.tables['friends'].drop()
