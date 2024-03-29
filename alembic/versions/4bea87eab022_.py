"""empty message

Revision ID: 4bea87eab022
Revises: 725b0ca8cd5f
Create Date: 2019-11-11 15:58:35.446837

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4bea87eab022'
down_revision = '725b0ca8cd5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('air_conditioner', 'ac_on',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.SmallInteger(),
               existing_nullable=True)
    op.alter_column('air_conditioner', 'desired_speed',
               existing_type=mysql.FLOAT(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('air_conditioner', 'desired_temperature',
               existing_type=mysql.FLOAT(),
               type_=sa.SmallInteger(),
               existing_nullable=True)
    op.alter_column('air_conditioner', 'if_online',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.SmallInteger(),
               existing_nullable=True)
    op.alter_column('air_conditioner', 'temperature',
               existing_type=mysql.FLOAT(),
               type_=sa.Integer(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    return
    # ### end Alembic commands ###
