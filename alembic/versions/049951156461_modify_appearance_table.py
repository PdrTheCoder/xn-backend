"""modify appearance table

Revision ID: 049951156461
Revises: bb3f808b6fd5
Create Date: 2019-12-08 01:01:51.907959

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '049951156461'
down_revision = 'bb3f808b6fd5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appear_records', sa.Column('certificateNum', sa.Unicode(length=50), nullable=True))
    op.add_column('appear_records', sa.Column('certificateType', sa.Unicode(length=50), nullable=True))
    op.add_column('appear_records', sa.Column('deviceIndexCode', sa.Unicode(length=30), nullable=True))
    op.add_column('appear_records', sa.Column('deviceName', sa.Unicode(length=30), nullable=True))
    op.add_column('appear_records', sa.Column('eventType', sa.Integer(), nullable=True))
    op.add_column('appear_records', sa.Column('faceId', sa.Integer(), nullable=True))
    op.add_column('appear_records', sa.Column('facePicture', sa.Unicode(length=300), nullable=True))
    op.add_column('appear_records', sa.Column('happenTime', sa.TIMESTAMP(), nullable=True))
    op.add_column('appear_records', sa.Column('name', sa.Unicode(length=50), nullable=True))
    op.add_column('appear_records', sa.Column('sex', sa.Unicode(length=30), nullable=True))
    op.drop_constraint('appear_records_ibfk_1', 'appear_records', type_='foreignkey')
    op.drop_constraint('appear_records_ibfk_2', 'appear_records', type_='foreignkey')
    op.drop_column('appear_records', 'device_id')
    op.drop_column('appear_records', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appear_records', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('appear_records', sa.Column('device_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('appear_records_ibfk_2', 'appear_records', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('appear_records_ibfk_1', 'appear_records', 'tracking_devices', ['device_id'], ['id'], ondelete='CASCADE')
    op.drop_column('appear_records', 'sex')
    op.drop_column('appear_records', 'name')
    op.drop_column('appear_records', 'happenTime')
    op.drop_column('appear_records', 'facePicture')
    op.drop_column('appear_records', 'faceId')
    op.drop_column('appear_records', 'eventType')
    op.drop_column('appear_records', 'deviceName')
    op.drop_column('appear_records', 'deviceIndexCode')
    op.drop_column('appear_records', 'certificateType')
    op.drop_column('appear_records', 'certificateNum')
    # ### end Alembic commands ###
