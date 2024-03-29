"""empty message

Revision ID: c3abbbd81271
Revises: 80575bc6e9d3
Create Date: 2019-08-25 08:15:31.748498

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c3abbbd81271'
down_revision = '80575bc6e9d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('air_conditioner',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('auto_controller_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['auto_controller_id'], ['auto_controllers.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('relay_status',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('relay_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.SmallInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('relay',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('device_index_code', sa.Unicode(length=50), nullable=True),
    sa.Column('channel', sa.Integer(), nullable=True),
    sa.Column('latest_record_id', sa.Integer(), nullable=True),
    sa.Column('control_type', sa.SmallInteger(), nullable=True),
    sa.Column('switch_id', sa.Integer(), nullable=True),
    sa.Column('locator_id', sa.Unicode(length=50), nullable=True),
    sa.Column('tcp_config_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['latest_record_id'], ['relay_status.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['locator_id'], ['locators.internal_code'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['switch_id'], ['switches.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['tcp_config_id'], ['tcp_config.id'], ondelete='set null'),
    sa.PrimaryKeyConstraint('id')
    )
    # sa.ForeignKeyConstraint(['relay_id'], ['relay.id'], ondelete='CASCADE'),
    op.create_index(op.f('ix_relay_device_index_code'), 'relay', ['device_index_code'], unique=False)
    op.drop_constraint('switches_ibfk_3', 'switches', type_='foreignkey')
    op.drop_constraint('switches_ibfk_4', 'switches', type_='foreignkey')
    op.drop_table('switch_status')
    op.add_column('auto_controllers', sa.Column('end_time', sa.Time(), nullable=True))
    op.add_column('auto_controllers', sa.Column('ir_sensor_id', sa.Integer(), nullable=True))
    op.add_column('auto_controllers', sa.Column('lux_sensor_id', sa.Integer(), nullable=True))
    op.add_column('auto_controllers', sa.Column('start_time', sa.Time(), nullable=True))
    op.add_column('auto_controllers', sa.Column('switch_panel_id', sa.Integer(), nullable=True))
    op.drop_constraint('auto_controllers_ibfk_2', 'auto_controllers', type_='foreignkey')
    op.drop_constraint('auto_controllers_ibfk_1', 'auto_controllers', type_='foreignkey')
    op.create_foreign_key(None, 'auto_controllers', 'switch_panel', ['switch_panel_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key(None, 'auto_controllers', 'lux_sensors', ['lux_sensor_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key(None, 'auto_controllers', 'ir_sensors', ['ir_sensor_id'], ['id'], ondelete='SET NULL')
    op.drop_column('auto_controllers', 'locator_id')
    op.drop_column('auto_controllers', 'tcp_config_id')
    op.add_column('switch_panel', sa.Column('device_index_code', sa.Unicode(length=50), nullable=True))
    op.create_index(op.f('ix_switch_panel_device_index_code'), 'switch_panel', ['device_index_code'], unique=False)
    op.add_column('switches', sa.Column('status', sa.SmallInteger(), nullable=True))
    op.drop_index('ix_switches_device_index_code', table_name='switches')   
    op.drop_column('switches', 'control_type')
    op.drop_column('switches', 'latest_record_id')
    op.drop_column('switches', 'device_index_code')
    # ### end Alembic commands ###


