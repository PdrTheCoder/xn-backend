"""update aqi related tables

Revision ID: c1f4a5872905
Revises: 715ccb6b1d73
Create Date: 2019-12-20 14:07:22.485669

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c1f4a5872905'
down_revision = '715ccb6b1d73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('aqi_sensors_ibfk_3', 'aqi_sensors', type_='foreignkey')
    op.drop_column('aqi_sensors', 'latest_record_id')
    op.drop_table('aqi_event_count')
    op.drop_index('ix_aqi_sensors_device_index_code', table_name='aqi_sensors')
    op.drop_column('aqi_sensors', 'device_index_code')
    op.drop_table('aqi_values')
    op.add_column('aqi_sensors', sa.Column('addr_hex', sa.Unicode(length=4), nullable=True))
    op.add_column('aqi_sensors', sa.Column('addr_int', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('aqi_sensors', sa.Column('device_index_code', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('aqi_sensors', sa.Column('latest_record_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('aqi_sensors_ibfk_3', 'aqi_sensors', 'aqi_values', ['latest_record_id'], ['id'], ondelete='SET NULL')
    op.create_index('ix_aqi_sensors_device_index_code', 'aqi_sensors', ['device_index_code'], unique=False)
    op.drop_column('aqi_sensors', 'addr_int')
    op.drop_column('aqi_sensors', 'addr_hex')
    op.create_table('aqi_event_count',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('aqi_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['aqi_id'], ['aqi_sensors.id'], name='aqi_event_count_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('aqi_values',
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', mysql.TIMESTAMP(), nullable=True),
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('sensor_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('temperature', mysql.FLOAT(), nullable=True),
    sa.Column('humidity', mysql.FLOAT(), nullable=True),
    sa.Column('pm25', mysql.DECIMAL(precision=8, scale=3), nullable=True),
    sa.Column('co2', mysql.FLOAT(), nullable=True),
    sa.Column('tvoc', mysql.FLOAT(), nullable=True),
    sa.Column('hcho', mysql.FLOAT(), nullable=True),
    sa.ForeignKeyConstraint(['sensor_id'], ['aqi_sensors.id'], name='aqi_values_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###