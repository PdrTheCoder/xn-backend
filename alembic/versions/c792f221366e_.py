"""empty message

Revision ID: c792f221366e
Revises: 
Create Date: 2019-08-22 14:30:48.343852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c792f221366e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # locators
    op.create_table('locators',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('internal_code', sa.Unicode(length=50), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=True),
    sa.Column('floor', sa.Integer(), nullable=True),
    sa.Column('zone', sa.Integer(), nullable=True),
    sa.Column('coorX', sa.Float(), nullable=True),
    sa.Column('coorY', sa.Float(), nullable=True),
    sa.Column('coorZ', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('internal_code')
    )

    # users

    op.create_table('users',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Unicode(length=50), nullable=True),
    sa.Column('person_name', sa.Unicode(length=30), nullable=True),
    sa.Column('job_no', sa.String(length=50), nullable=True),
    sa.Column('gender', sa.SmallInteger(), nullable=True),
    sa.Column('org_path', sa.String(length=50), nullable=True),
    sa.Column('org_index_code', sa.String(length=50), nullable=True),
    sa.Column('org_name', sa.String(length=50), nullable=True),
    sa.Column('certificate_type', sa.Integer(), nullable=True),
    sa.Column('certificate_no', sa.String(length=50), nullable=True),
    sa.Column('phone_no', sa.String(length=30), nullable=True),
    sa.Column('address', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('education', sa.SmallInteger(), nullable=True),
    sa.Column('nation', sa.SmallInteger(), nullable=True),
    sa.Column('photo_url', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_person_id'), 'users', ['person_id'], unique=False)

    # user_logins
    op.create_table('user_logins',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('username', sa.Unicode(length=50), nullable=True),
    sa.Column('password', sa.String(length=200), nullable=True),
    sa.Column('level', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # tcp config
    op.create_table('tcp_config',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip', sa.String(length=50), nullable=True),
    sa.Column('port', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    # tracking devices
    op.create_table('tracking_devices',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('device_index_code', sa.Unicode(length=50), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('locator', sa.Unicode(length=50), nullable=True),
    sa.Column('device_type', sa.SmallInteger(), nullable=True),
    sa.Column('latest_acs_record_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['locator'], ['locators.internal_code'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tracking_devices_device_index_code'), 'tracking_devices', ['device_index_code'], unique=False)

    # acs records
    op.create_table('acs_records',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('acs_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.SmallInteger(), nullable=True),
    sa.Column('event_type', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['acs_id'], ['tracking_devices.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # appear records
    op.create_table('appear_records',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('device_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['tracking_devices.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # latest position
    op.create_table('latest_position',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('appear_record_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['appear_record_id'], ['appear_records.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # heat map snapshots
    op.create_table('heatmap_snapshots',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('device_id', sa.Integer(), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['device_id'], ['tracking_devices.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # mantunci box
    op.create_table('mantunci_box',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mac', sa.Unicode(length=50), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('latest_alarm_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mantunci_box_mac'), 'mantunci_box', ['mac'], unique=False)

    # s3_fc20
    op.create_table('s3_fc20',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('addr', sa.Integer(), nullable=True),
    sa.Column('desc', sa.Unicode(length=100), nullable=True),
    sa.Column('box_id', sa.Integer(), nullable=True),
    sa.Column('latest_record_id', sa.Integer(), nullable=True),
    sa.Column('measure_type', sa.SmallInteger(), nullable=True),
    sa.Column('locator_id', sa.Unicode(length=50), nullable=True),
    sa.ForeignKeyConstraint(['box_id'], ['mantunci_box.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['locator_id'], ['locators.internal_code'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )

    # s3_fc20 records
    op.create_table('s3_fc20_records',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('s3_fc20_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('validity', sa.BOOLEAN(), nullable=True),
    sa.Column('enable_netctr', sa.BOOLEAN(), nullable=True),
    sa.Column('oc', sa.BOOLEAN(), nullable=True),
    sa.Column('online', sa.BOOLEAN(), nullable=True),
    sa.Column('total_power', sa.Float(), nullable=True),
    sa.Column('mxgg', sa.Float(), nullable=True),
    sa.Column('mxgl', sa.Float(), nullable=True),
    sa.Column('line_type', sa.SmallInteger(), nullable=True),
    sa.Column('spec', sa.String(length=50), nullable=True),
    sa.Column('control', sa.BOOLEAN(), nullable=True),
    sa.Column('visibility', sa.BOOLEAN(), nullable=True),
    sa.Column('alarm', sa.Integer(), nullable=True),
    sa.Column('gLd', sa.Float(), nullable=True),
    sa.Column('gA', sa.Float(), nullable=True),
    sa.Column('gT', sa.Float(), nullable=True),
    sa.Column('gV', sa.Float(), nullable=True),
    sa.Column('gW', sa.Float(), nullable=True),
    sa.Column('gPF', sa.Float(), nullable=True),
    sa.Column('aA', sa.Float(), nullable=True),
    sa.Column('aT', sa.Float(), nullable=True),
    sa.Column('aV', sa.Float(), nullable=True),
    sa.Column('aW', sa.Float(), nullable=True),
    sa.Column('aPF', sa.Float(), nullable=True),
    sa.Column('bA', sa.Float(), nullable=True),
    sa.Column('bT', sa.Float(), nullable=True),
    sa.Column('bV', sa.Float(), nullable=True),
    sa.Column('bW', sa.Float(), nullable=True),
    sa.Column('bPF', sa.Float(), nullable=True),
    sa.Column('cA', sa.Float(), nullable=True),
    sa.Column('cT', sa.Float(), nullable=True),
    sa.Column('cV', sa.Float(), nullable=True),
    sa.Column('cW', sa.Float(), nullable=True),
    sa.Column('cPF', sa.Float(), nullable=True),
    sa.Column('nA', sa.Float(), nullable=True),
    sa.Column('nT', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['s3_fc20_id'], ['s3_fc20.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # box alarms
    op.create_table('box_alarms',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('box_id', sa.Integer(), nullable=False),
    sa.Column('addr', sa.Integer(), nullable=True),
    sa.Column('node', sa.String(length=50), nullable=True),
    sa.Column('alarm_or_type', sa.String(length=30), nullable=True),
    sa.Column('info', sa.String(length=50), nullable=True),
    sa.Column('type_number', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['box_id'], ['mantunci_box.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # energe consume
    op.create_table('energy_consume_by_hour',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('consume_id', sa.Integer(), nullable=False),
    sa.Column('box_id', sa.Integer(), nullable=True),
    sa.Column('s3_fc20_id', sa.Integer(), nullable=True),
    sa.Column('electricity', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['box_id'], ['mantunci_box.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['s3_fc20_id'], ['s3_fc20.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('consume_id')
    )

    # energy consume
    op.create_table('energy_consume_daily',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('consume_id', sa.Integer(), nullable=False),
    sa.Column('box_id', sa.Integer(), nullable=True),
    sa.Column('s3_fc20_id', sa.Integer(), nullable=True),
    sa.Column('electricity', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['box_id'], ['mantunci_box.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['s3_fc20_id'], ['s3_fc20.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('consume_id')
    )

    # energy consume
    op.create_table('energy_consume_monthly',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('consume_id', sa.Integer(), nullable=False),
    sa.Column('box_id', sa.Integer(), nullable=True),
    sa.Column('s3_fc20_id', sa.Integer(), nullable=True),
    sa.Column('electricity', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['box_id'], ['mantunci_box.id'], ),
    sa.ForeignKeyConstraint(['s3_fc20_id'], ['s3_fc20.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('consume_id')
    )

    # ir_sensor
    op.create_table('ir_sensors',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('batch_no', sa.Integer(), nullable=True),
    sa.Column('addr_no', sa.Integer(), nullable=True),
    sa.Column('locator', sa.Unicode(length=50), nullable=True),
    sa.Column('latest_record_id', sa.Integer(), nullable=True),
    sa.Column('threshold', sa.Integer(), nullable=True),
    sa.Column('delay', sa.Integer(), nullable=True),
    sa.Column('tcp_config_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['locator'], ['locators.internal_code'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['tcp_config_id'], ['tcp_config.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )

    # ir_sensor_status
    op.create_table('ir_sensor_status',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensor_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('status', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['sensor_id'], ['ir_sensors.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # aqi_sensors
    op.create_table('aqi_sensors',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('device_index_code', sa.Unicode(length=50), nullable=True),
    sa.Column('locator', sa.Unicode(length=50), nullable=True),
    sa.Column('latest_record_id', sa.Integer(), nullable=True),
    sa.Column('tcp_config_id', sa.Integer(), nullable=True),
    sa.Column('switch_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['locator'], ['locators.internal_code'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['tcp_config_id'], ['tcp_config.id'], ondelete='set null'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_aqi_sensors_device_index_code'), 'aqi_sensors', ['device_index_code'], unique=False)

    # aqi event count
    op.create_table('aqi_event_count',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('aqi_id', sa.Integer(), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['aqi_id'], ['aqi_sensors.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # aqi values
    op.create_table('aqi_values',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensor_id', sa.Integer(), nullable=True),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('humidity', sa.Float(), nullable=True),
    sa.Column('pm25', sa.Float(), nullable=True),
    sa.Column('co2', sa.Float(), nullable=True),
    sa.Column('tvoc', sa.Float(), nullable=True),
    sa.Column('voc', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['sensor_id'], ['aqi_sensors.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # lux sensors
    op.create_table('lux_sensors',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('batch_no', sa.Integer(), nullable=True),
    sa.Column('addr_no', sa.Integer(), nullable=True),
    sa.Column('locator', sa.Unicode(length=50), nullable=True),
    sa.Column('latest_record_id', sa.Integer(), nullable=True),
    sa.Column('tcp_config_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['locator'], ['locators.internal_code'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['tcp_config_id'], ['tcp_config.id'], ondelete='set null'),
    sa.PrimaryKeyConstraint('id')
    )

    # lux values
    op.create_table('lux_values',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensor_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sensor_id'], ['lux_sensors.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # lux event count
    op.create_table('lux_event_count',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lux_id', sa.Integer(), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['lux_id'], ['lux_sensors.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # fire alarm sensors
    op.create_table('fire_alarm_sensors',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('device_index_code', sa.Unicode(length=50), nullable=True),
    sa.Column('locator', sa.Unicode(length=50), nullable=True),
    sa.Column('latest_record_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['locator'], ['locators.internal_code'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fire_alarm_sensors_device_index_code'), 'fire_alarm_sensors', ['device_index_code'], unique=False)

    # fire alarm status
    op.create_table('fire_alarm_status',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sensor_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['sensor_id'], ['fire_alarm_sensors.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # switch panel
    op.create_table('switch_panel',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('desc', sa.Unicode(length=100), nullable=True),
    sa.Column('ip', sa.Unicode(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    # switches
    op.create_table('switches',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('device_index_code', sa.Unicode(length=50), nullable=True),
    sa.Column('channel', sa.Integer(), nullable=True),
    sa.Column('latest_record_id', sa.Integer(), nullable=True),
    sa.Column('switch_panel_id', sa.Integer(), nullable=True),
    sa.Column('control_type', sa.SmallInteger(), nullable=True),
    sa.Column('locator_id', sa.Unicode(length=50), nullable=True),
    sa.Column('level', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['locator_id'], ['locators.internal_code'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['switch_panel_id'], ['switch_panel.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_switches_device_index_code'), 'switches', ['device_index_code'], unique=False)

    # switches
    op.create_table('switch_status',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('switch_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['switch_id'], ['switches.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )

    # elevators
    op.create_table('elevators',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('device_index_code', sa.Unicode(length=50), nullable=True),
    sa.Column('locator', sa.Unicode(length=50), nullable=True),
    sa.Column('latest_record_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['locator'], ['locators.internal_code'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_elevators_device_index_code'), 'elevators', ['device_index_code'], unique=False)

    # elevator status
    op.create_table('elevator_status',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('elevator_id', sa.Integer(), nullable=True),
    sa.Column('floor', sa.Integer(), nullable=True),
    sa.Column('direction', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['elevator_id'], ['elevators.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )

    # auto controllers
    op.create_table('auto_controllers',
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('if_auto', sa.SmallInteger(), nullable=True),
    sa.Column('locator_id', sa.Unicode(length=50), nullable=True),
    sa.Column('ir_count', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['locator_id'], ['locators.internal_code'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )

    # add fk part
    op.create_foreign_key(None, 'tracking_devices', 'acs_records', ['latest_acs_record_id'], ['id'])
    op.create_foreign_key(None, 'mantunci_box', 'box_alarms', ['latest_alarm_id'], ['id'])
    op.create_foreign_key(None, 's3_fc20', 's3_fc20_records', ['latest_record_id'], ['id'])
    op.create_foreign_key(None, 'ir_sensors', 'ir_sensor_status', ['latest_record_id'], ['id'])
    op.create_foreign_key(None, 'aqi_sensors', 'aqi_values', ['latest_record_id'], ['id'])
    op.create_foreign_key(None, 'lux_sensors', 'lux_values', ['latest_record_id'], ['id'])
    op.create_foreign_key(None, 'fire_alarm_sensors', 'fire_alarm_status', ['latest_record_id'], ['id'])
    op.create_foreign_key(None, 'switches', 'switch_status', ['latest_record_id'], ['id'])
    op.create_foreign_key(None, 'elevators', 'elevator_status', ['latest_record_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
