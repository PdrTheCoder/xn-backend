"""modify appearance table 2nd

Revision ID: 67fe14066bdd
Revises: 049951156461
Create Date: 2019-12-08 01:09:26.979436

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '67fe14066bdd'
down_revision = '049951156461'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appear_records', sa.Column('cameraIndexCode', sa.Unicode(length=100), nullable=True))
    op.alter_column('appear_records', 'certificateNum',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.Unicode(length=100),
               existing_nullable=True)
    op.alter_column('appear_records', 'certificateType',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.Unicode(length=100),
               existing_nullable=True)
    op.alter_column('appear_records', 'deviceName',
               existing_type=mysql.VARCHAR(length=30),
               type_=sa.Unicode(length=100),
               existing_nullable=True)
    op.drop_column('appear_records', 'deviceIndexCode')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appear_records', sa.Column('deviceIndexCode', mysql.VARCHAR(length=30), nullable=True))
    op.alter_column('appear_records', 'happenTime',
               existing_type=mysql.TIMESTAMP(),
               nullable=True)
    op.alter_column('appear_records', 'deviceName',
               existing_type=sa.Unicode(length=100),
               type_=mysql.VARCHAR(length=30),
               existing_nullable=True)
    op.alter_column('appear_records', 'certificateType',
               existing_type=sa.Unicode(length=100),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=True)
    op.alter_column('appear_records', 'certificateNum',
               existing_type=sa.Unicode(length=100),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=True)
    op.drop_column('appear_records', 'cameraIndexCode')
    # ### end Alembic commands ###