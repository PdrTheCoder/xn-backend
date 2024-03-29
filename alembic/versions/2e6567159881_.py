"""empty message

Revision ID: 2e6567159881
Revises: 36df34b30986
Create Date: 2019-09-18 13:12:57.900636

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2e6567159881'
down_revision = '36df34b30986'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('aqi_values', sa.Column('hcho', sa.Float(), nullable=True))
    op.alter_column('aqi_values', 'pm25',
               existing_type=mysql.FLOAT(),
               type_=sa.DECIMAL(precision=8, scale=3),
               existing_nullable=True)
    op.drop_column('aqi_values', 'voc')
    # ### end Alembic commands ###


def downgrade():
    pass
