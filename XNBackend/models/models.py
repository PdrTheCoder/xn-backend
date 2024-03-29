# -*- coding:utf-8 -*-
from .base import db
import logging

from sqlalchemy import ForeignKey, Unicode, BOOLEAN, TIMESTAMP, String, \
    SmallInteger, Integer, Float, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from flask_bcrypt import generate_password_hash, check_password_hash
from XNBackend.api_client.air_conditioner import get_ac_data

L = logging.getLogger(__name__)

SHORT_LEN_30 = 30
MEDIUM_LEN_50 = 50
LONG_LEN_100 = 100


class TimeStampMixin:
    created_at = db.Column(TIMESTAMP, nullable=False,
                           server_default=func.current_timestamp())
    updated_at = db.Column(TIMESTAMP, onupdate=func.current_timestamp())


class CarbonMixin:
    carbon_mixin_factor = 0.33*0.68
    carbon_mixin_watt_attr_name = ''
    @property
    def carbon_emission(self):
        return getattr(self, self.carbo_mixin_watt_attr_name) \
            * self.carbon_mixin_factor


class Users(db.Model, TimeStampMixin):
    __tablename__ = 'users'
    '''sync from hik'''
    id = db.Column(Integer, primary_key=True)
    person_id = db.Column(Unicode(length=MEDIUM_LEN_50), index=True)
    person_name = db.Column(Unicode(length=SHORT_LEN_30))
    job_no = db.Column(String(MEDIUM_LEN_50))
    gender = db.Column(SmallInteger)
    org_path = db.Column(String(MEDIUM_LEN_50))
    org_index_code = db.Column(String(MEDIUM_LEN_50))
    org_name = db.Column(String(MEDIUM_LEN_50))
    certificate_type = db.Column(Integer)
    certificate_no = db.Column(String(MEDIUM_LEN_50))
    phone_no = db.Column(String(SHORT_LEN_30))
    address = db.Column(String(LONG_LEN_100))
    email = db.Column(String(MEDIUM_LEN_50))
    education = db.Column(SmallInteger)
    nation = db.Column(SmallInteger)
    photo_url = db.Column(String(LONG_LEN_100))


class UserLogins(db.Model, TimeStampMixin):
    __tablename__ = 'user_logins'
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey(Users.id, ondelete='CASCADE'))
    username = db.Column(Unicode(length=MEDIUM_LEN_50))
    password = db.Column(String(200))
    level = db.Column(SmallInteger)
    user_ref = relationship('Users', backref='user_logins')

    @property
    def level_repr(self):
        if self.level == 0:
            return 'visitor'
        if self.level == 1:
            return 'employee'
        if self.level == 2:
            return 'sub_admin'
        if self.level == 3:
            return 'admin'

    def set_password(self, password):
        self.password = generate_password_hash(password, 10).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Locators(db.Model, TimeStampMixin):
    __tablename__ = 'locators'
    internal_code = db.Column(Unicode(length=MEDIUM_LEN_50), primary_key=True)
    description = db.Column(String(LONG_LEN_100))
    floor = db.Column(Integer)
    zone = db.Column(Integer)
    # coorX, coorY and coorZ may not necessary
    coorX = db.Column(Float, nullable=True)
    coorY = db.Column(Float, nullable=True)
    coorZ = db.Column(Float, nullable=True)
    # eco mode, 0 means off, 1 means on
    eco_mode = db.Column(SmallInteger)


class TcpConfig(db.Model, TimeStampMixin):
    __tablename__ = 'tcp_config'
    id = db.Column(Integer, primary_key=True)
    ip = db.Column(String(MEDIUM_LEN_50))
    port = db.Column(Integer)
    desc = db.Column(String(100))


class TrackingDevices(db.Model, TimeStampMixin):
    __tablename__ = 'tracking_devices'
    id = db.Column(Integer, primary_key=True)
    device_index_code = db.Column(Unicode(length=MEDIUM_LEN_50), index=True)
    name = db.Column(String(MEDIUM_LEN_50))
    locator = db.Column(Unicode(length=MEDIUM_LEN_50),
                        ForeignKey(Locators.internal_code,
                                   ondelete='SET NULL'))
    # 0 means camera, 1 means acs
    device_type = db.Column(SmallInteger)
    locator_body = relationship('Locators', foreign_keys=[locator])
    latest_acs_record_id = db.Column(Integer,
                                     ForeignKey('acs_records.id',
                                                ondelete='SET NULL'))
    acs_record = relationship("AcsRecords",
                              foreign_keys=[latest_acs_record_id])


class AcsRecords(db.Model, TimeStampMixin):
    __tablename__ = "acs_records"
    id = db.Column(Integer, primary_key=True)
    acs_id = db.Column(Integer, ForeignKey(TrackingDevices.id,
                                           ondelete="CASCADE"))
    # status =1 means open status=0 means closing
    status = db.Column(SmallInteger)
    event_type = db.Column(Integer)
    event_id = db.Column(Unicode(length=LONG_LEN_100))
    acs = relationship('TrackingDevices', foreign_keys=[acs_id])


class Door(db.Model, TimeStampMixin):
    __tablename__ = "door"
    door_index_code = db.Column(Unicode(length=LONG_LEN_100), primary_key=True)
    status = db.Column(SmallInteger)
    room_no_internal = db.Column(Unicode(length=LONG_LEN_100))
    room_no_external = db.Column(Unicode(length=LONG_LEN_100))
    desc = db.Column(Unicode(length=LONG_LEN_100))


class AppearRecords(db.Model, TimeStampMixin):
    __tablename__ = 'appear_records'
    id = db.Column(Integer, primary_key=True)
    faceId = db.Column(Integer)
    name = db.Column(Unicode(length=MEDIUM_LEN_50))
    sex = db.Column(Unicode(length=SHORT_LEN_30))
    certificateType = db.Column(Unicode(length=LONG_LEN_100))
    certificateNum = db.Column(Unicode(length=LONG_LEN_100))
    facePicture = db.Column(Unicode(length=300))
    cameraIndexCode = db.Column(Unicode(length=LONG_LEN_100))
    deviceName = db.Column(Unicode(length=LONG_LEN_100))
    eventType = db.Column(Integer)
    happenTime = db.Column(TIMESTAMP)
    # 0 means important target, 1 means stranger
    type = db.Column(SmallInteger)
    active = db.Column(SmallInteger, default=1)


class LatestPosition(db.Model, TimeStampMixin):
    __tablename__ = 'latest_position'
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey(Users.id,
                                            ondelete='CASCADE'))
    appear_record_id = db.Column(Integer, ForeignKey(AppearRecords.id,
                                                     ondelete='SET NULL'))
    user = relationship('Users', backref='latest_position_pointer')
    appear_record = relationship('AppearRecords')


class HeatMapSnapshots(db.Model, TimeStampMixin):
    __tablename__ = 'heatmap_snapshots'
    id = db.Column(Integer, primary_key=True)
    device_id = db.Column(Integer, ForeignKey(TrackingDevices.id,
                                              ondelete="CASCADE"))
    count = db.Column(Integer)
    device = relationship('TrackingDevices', backref="heatmap_snapshots")


class MantunciBox(db.Model, TimeStampMixin):
    __tablename__ = 'mantunci_box'
    id = db.Column(Integer, primary_key=True)
    mac = db.Column(Unicode(length=MEDIUM_LEN_50), index=True)
    name = db.Column(String(SHORT_LEN_30))
    phone = db.Column(String(SHORT_LEN_30))
    locator_id = db.Column(Unicode(length=MEDIUM_LEN_50),
                           ForeignKey(Locators.internal_code,
                                      ondelete='SET NULL'))
    locator = relationship('Locators', foreign_keys=[locator_id])


class S3FC20(db.Model, TimeStampMixin):
    __tablename__ = 's3_fc20'
    id = db.Column(Integer, primary_key=True)
    addr = db.Column(Integer)
    desc = db.Column(Unicode(LONG_LEN_100))
    box_id = db.Column(Integer, ForeignKey(MantunciBox.id,
                                           ondelete="SET NULL"))
    box = relationship('MantunciBox')
    # 0 means light, 1 means ac, 2 means power socket
    measure_type = db.Column(SmallInteger)
    locator_id = db.Column(Unicode(length=MEDIUM_LEN_50),
                           ForeignKey(Locators.internal_code,
                                      ondelete='SET NULL'))
    locator = relationship('Locators', foreign_keys=[locator_id])


class BoxAlarms(db.Model, TimeStampMixin):
    __tablename__ = 'box_alarms'
    id = db.Column(Integer, primary_key=True)
    box_id = db.Column(Integer, ForeignKey(MantunciBox.id,
                                           ondelete='CASCADE'),
                       nullable=False)
    addr = db.Column(Integer)
    node = db.Column(String(MEDIUM_LEN_50))
    alarm_or_type = db.Column(String(SHORT_LEN_30))
    info = db.Column(String(MEDIUM_LEN_50))
    type_number = db.Column(SmallInteger)
    time = db.Column(TIMESTAMP)
    box = relationship('MantunciBox', foreign_keys=[box_id])

    @property
    def alarm_type(self):
        alarm_info_mapping = {
            1: '未知',
            2: '短路报警',
            3: '漏电报警',
            4: '过载报警',
            5: '过压报警',
            6: '欠压报警',
            7: '温度报警',
            8: '浪涌报警',
            9: '漏电保护功能正常',
            10: '漏电保护自检未完成',
            11: '打火报警',
            12: '漏电预警',
            13: '电流预警',
            14: '过压预警',
            15: '欠压预警',
            16: '通讯报警'
        }
        return alarm_info_mapping[self.type_number]


class EnergyConsumeByHour(db.Model, TimeStampMixin, CarbonMixin):
    """use updated_at to indicate statistic range"""
    __tablename__ = 'energy_consume_by_hour'
    carbon_mixin_watt_attr_name = 'electricity'
    consume_id = db.Column(Integer, primary_key=True)
    s3_fc20_id = db.Column(Integer, ForeignKey(S3FC20.id,
                                               ondelete='SET NULL'))
    electricity = db.Column(Float)
    s3_fc20 = relationship('S3FC20', foreign_keys=[s3_fc20_id])


class EnergyConsumeDaily(db.Model, TimeStampMixin, CarbonMixin):
    """use updated_at to indicate statistic range"""
    __tablename__ = 'energy_consume_daily'
    carbon_mixin_watt_attr_name = 'electricity'
    consume_id = db.Column(Integer, primary_key=True)
    s3_fc20_id = db.Column(Integer, ForeignKey(S3FC20.id,
                                               ondelete='SET NULL'))
    electricity = db.Column(Float)
    s3_fc20 = relationship('S3FC20', foreign_keys=[s3_fc20_id])


class EnegyConsumeMonthly(db.Model, TimeStampMixin):
    """use updated_at to indicate statistic range"""
    __tablename__ = 'energy_consume_monthly'
    consume_id = db.Column(Integer, primary_key=True)
    s3_fc20_id = db.Column(Integer, ForeignKey(S3FC20.id,
                                               ondelete='SET NULL'))
    electricity = db.Column(Float)
    s3_fc20 = relationship('S3FC20', foreign_keys=[s3_fc20_id])


class IRSensors(db.Model, TimeStampMixin):
    __tablename__ = 'ir_sensors'
    id = db.Column(Integer, primary_key=True)
    batch_no = db.Column(db.Integer)
    addr_no = db.Column(db.Integer)
    locator = db.Column(Unicode(length=MEDIUM_LEN_50),
                        ForeignKey(Locators.internal_code,
                                   ondelete='SET NULL'))
    threshold = db.Column(db.Integer)
    delay = db.Column(db.Integer)
    tcp_config_id = db.Column(Integer, ForeignKey(TcpConfig.id, ondelete='SET NULL'))
    tcp_config = relationship('TcpConfig', foreign_keys=[tcp_config_id])
    locator_body = relationship('Locators', foreign_keys=[locator])
    # 1 means detected; 0 means no detected
    status = db.Column(db.SmallInteger)


class AQISensors(db.Model, TimeStampMixin):
    __tablename__ = 'aqi_sensors'
    id = db.Column(Integer, primary_key=True)
    addr_int = db.Column(Integer)
    addr_hex = db.Column(Unicode(length=4))
    locator = db.Column(Unicode(length=MEDIUM_LEN_50),
                        ForeignKey(Locators.internal_code,
                                   ondelete='SET NULL'))
    locator_body = relationship('Locators')
    tcp_config_id = db.Column(Integer, ForeignKey(TcpConfig.id,
                                                  ondelete='set null'))
    tcp_config = relationship('TcpConfig', foreign_keys=[tcp_config_id])


class LuxValues(db.Model, TimeStampMixin):
    __tablename__ = 'lux_values'
    # 只有主动查询
    id = db.Column(Integer, primary_key=True)
    sensor_id = db.Column(Integer, ForeignKey("lux_sensors.id",
                                              ondelete='CASCADE'))
    value = db.Column(Integer)
    sensor = relationship('LuxSensors', foreign_keys=[sensor_id])


class LuxSensors(db.Model, TimeStampMixin):
    __tablename__ = 'lux_sensors'
    id = db.Column(Integer, primary_key=True)
    batch_no = db.Column(db.Integer)
    addr_no = db.Column(db.Integer)
    locator = db.Column(Unicode(length=MEDIUM_LEN_50),
                        ForeignKey(Locators.internal_code,
                                   ondelete='SET NULL'))
    latest_record_id = db.Column(Integer, ForeignKey(LuxValues.id,
                                                     ondelete="SET NULL"))
    latest_record = relationship('LuxValues', foreign_keys=[latest_record_id])
    locator_body = relationship('Locators')
    tcp_config_id = db.Column(Integer, ForeignKey(TcpConfig.id,
                                                  ondelete='set null'))
    tcp_config = relationship('TcpConfig', foreign_keys=[tcp_config_id])


class LuxEventCount(db.Model):
    __tablename__ = 'lux_event_count'
    id = db.Column(Integer, primary_key=True)
    lux_id = db.Column(Integer, ForeignKey(LuxSensors.id,
                                           ondelete="CASCADE"))
    count = db.Column(Integer)


class FireAlarmStatus(db.Model, TimeStampMixin):
    __tablename__ = 'fire_alarm_status'
    id = db.Column(Integer, primary_key=True)
    sensor_id = db.Column(Integer, ForeignKey('fire_alarm_sensors.id',
                                              ondelete='CASCADE'))
    value = db.Column(SmallInteger)
    sensor = relationship('FireAlarmSensors', foreign_keys=[sensor_id])


class FireAlarmSensors(db.Model, TimeStampMixin):
    __tablename__ = 'fire_alarm_sensors'
    id = db.Column(Integer, primary_key=True)
    device_index_code = db.Column(Unicode(length=MEDIUM_LEN_50), index=True)
    locator = db.Column(Unicode(length=MEDIUM_LEN_50),
                        ForeignKey(Locators.internal_code,
                                   ondelete='SET NULL'))
    latest_record_id = db.Column(Integer,
                                 ForeignKey('fire_alarm_status.id',
                                            ondelete='SET NULL'))
    latest_record = relationship('FireAlarmStatus',
                                 foreign_keys=[latest_record_id])
    locator_body = relationship('Locators')


class SwitchPanel(db.Model, TimeStampMixin):
    __tablename__ = 'switch_panel'
    id = db.Column(Integer, primary_key=True)
    batch_no = db.Column(db.Integer)
    addr_no = db.Column(db.Integer)
    desc = db.Column(Unicode(length=LONG_LEN_100))
    # when panel_type is 0 means four control, when panel_type is 1 means double control
    panel_type = db.Column(SmallInteger)
    tcp_config_id = db.Column(Integer, ForeignKey(TcpConfig.id,
                                                  ondelete='set null'))
    tcp_config = relationship('TcpConfig', foreign_keys=[tcp_config_id])
    locator_id = db.Column(Unicode(length=MEDIUM_LEN_50),
                           ForeignKey(Locators.internal_code,
                                      ondelete='SET NULL'))
    locator = relationship('Locators')


class Switches(db.Model, TimeStampMixin):
    __tablename__ = 'switches'
    id = db.Column(Integer, primary_key=True)
    channel = db.Column(Integer)
    switch_panel_id = db.Column(Integer,
                                ForeignKey('switch_panel.id',
                                           ondelete='SET NULL'))
    status = db.Column(SmallInteger)
    switch_panel = relationship('SwitchPanel', foreign_keys=[switch_panel_id], backref='belong_switches')
    desc = db.Column(String(100))

    @property
    def four_control_type_readable(self):
        if self.channel == 1:
            return u'main light'
        elif self.channel == 2:
            return u'acs'
        elif self.channel == 3:
            return u'auto'
        elif self.channel == 4:
            return u'aux light'

    @property
    def double_control_type_readable(self):
        if self.channel == 1:
            return u'main light'
        elif self.channel == 2:
            return u'auto'


class Relay(db.Model, TimeStampMixin):
    __tablename__ = 'relay'
    id = db.Column(Integer, primary_key=True)
    device_index_code = db.Column(Unicode(length=MEDIUM_LEN_50), index=True)
    addr = db.Column(Integer)
    channel = db.Column(Integer)
    switch_id = db.Column(Integer, ForeignKey('switches.id',
                                              ondelete='SET NULL'))
    switch = relationship('Switches', foreign_keys=[switch_id], backref='belong_relays')
    locator_id = db.Column(Unicode(length=MEDIUM_LEN_50),
                           ForeignKey(Locators.internal_code,
                                      ondelete='SET NULL'))
    locator = relationship('Locators')
    tcp_config_id = db.Column(Integer, ForeignKey(TcpConfig.id,
                                                  ondelete='set null'))
    tcp_config = relationship('TcpConfig', foreign_keys=[tcp_config_id])
    IPAddr = db.Column(String(100))


class ElevatorStatus(db.Model, TimeStampMixin):
    __tablename__ = 'elevator_status'
    id = db.Column(Integer, primary_key=True)
    elevator_id = db.Column(Integer, ForeignKey('elevators.id',
                                                ondelete='CASCADE'))
    floor = db.Column(Integer)
    direction = db.Column(SmallInteger)
    elevator = relationship('Elevators', foreign_keys=[elevator_id])

    @property
    def readable_direction(self):
        mapping = {1: "up",
                   2: "down",
                   0: "stop"}
        return mapping[self.direction]


class Elevators(db.Model, TimeStampMixin):
    __tablename__ = 'elevators'
    id = db.Column(Integer, primary_key=True)
    device_index_code = db.Column(Unicode(length=MEDIUM_LEN_50), index=True)
    locator = db.Column(Unicode(length=MEDIUM_LEN_50),
                        ForeignKey(Locators.internal_code,
                                   ondelete='SET NULL'))
    latest_record_id = db.Column(Integer, ForeignKey('elevator_status.id',
                                                     ondelete='SET NULL'))
    latest_record = relationship('ElevatorStatus',
                                 foreign_keys=[latest_record_id])


class Notification(db.Model, TimeStampMixin):
    __tablename__ = 'notification'
    id = db.Column(Integer, primary_key=True)
    content = db.Column(Unicode(400))
    color = db.Column(Unicode(50))
    title = db.Column(Unicode(50))


class AutoControllers(db.Model, TimeStampMixin):
    __tablename__ = 'auto_controllers'
    id = db.Column(Integer, primary_key=True)
    # 0 means manual 1 means auto
    if_auto = db.Column(SmallInteger)
    ir_count = db.Column(SmallInteger)
    start_time = db.Column(Time)
    end_time = db.Column(Time)
    switch_panel_id = db.Column(Integer,
                                ForeignKey('switch_panel.id',
                                           ondelete='SET NULL'))
    switch_panel = relationship('SwitchPanel', foreign_keys=[switch_panel_id])
    ir_sensor_id = db.Column(Integer,
                                ForeignKey('ir_sensors.id',
                                           ondelete='SET NULL'))
    ir_sensor = relationship('IRSensors', foreign_keys=[ir_sensor_id])
    lux_sensor_id = db.Column(Integer,
                              ForeignKey('lux_sensors.id',
                                         ondelete='SET NULL'))
    lux_sensor = relationship('LuxSensors', foreign_keys=[lux_sensor_id])


class AirConditioner(db.Model, TimeStampMixin):
    __tablename__ = 'air_conditioner'
    device_index_code = db.Column(Unicode(length=MEDIUM_LEN_50), primary_key=True)
    desired_speed = db.Column(Integer)
    if_online = db.Column(SmallInteger)
    desired_mode = db.Column(SmallInteger)
    temperature = db.Column(Integer)
    ac_on = db.Column(SmallInteger)
    desired_temperature = db.Column(SmallInteger)
    locator_id = db.Column(Unicode(length=MEDIUM_LEN_50), ForeignKey(Locators.internal_code,
                                                                     ondelete='SET NULL'))
    locator = relationship('Locators')

    @staticmethod
    def extract_data(ac_data):
        data_dict = dict()
        data_dict['device_index_code'] = ac_data['deviceCode']
        data_dict['if_online'] = ac_data['online']
        for d in ac_data['variantDatas']:
            if d['code'] == 'FanSpeedSet':
                data_dict['set_speed'] = int(d['value'])
                continue
            if d['code'] == 'ModeCmd':
                data_dict['set_mode'] = int(d['value'])
                continue
            if d['code'] == 'RoomTemp':
                data_dict['temperature'] = int(d['value'])
                continue
            if d['code'] == 'StartStopStatus':
                data_dict['ac_on'] = True if int(d['value']) else False
                continue
            if d['code'] == 'TempSet':
                data_dict['set_temperature'] = int(d['value'])
        return data_dict

    def apply_values(self, data):
        assert self.device_index_code == data.get('deviceCode')
        if data.get('errCode', 0) != 0:
            reason = data.get('errMsg')
            L.info(f'Failed to get values of ac reason: {reason}')
            return

        data_in_dict = self.extract_data(data)
        self.if_online = 1 if data_in_dict['if_online'] else 0
        self.desired_speed = data_in_dict.get('set_speed')
        self.desired_mode = data_in_dict.get('set_mode')
        self.temperature = data_in_dict.get('temperature')
        self.ac_on = data_in_dict.get('ac_on')
        self.desired_temperature = data_in_dict.get('set_temperature')

    def update_values(self):
        ret = get_ac_data([self.device_index_code])
        self.apply_values(ret['data'][0])


class UniAlarms(db.Model, TimeStampMixin):
    __tablename__ = 'uni_alarms'
    internal_id = db.Column(Integer, primary_key=True, autoincrement=True)
    external_id = db.Column(Unicode(length=LONG_LEN_100))
    happen_time = db.Column(TIMESTAMP)
    cancel_time = db.Column(TIMESTAMP)
    # 0 mean electric alarm;
    # 1 means acs alarm;
    # 2 means elevator alarm
    alarm_group = db.Column(SmallInteger)
    alarm_code = db.Column(Integer)
    alarm_content = db.Column(Unicode(length=LONG_LEN_100))
    room = db.Column(Unicode(length=10))
    floor = db.Column(Integer)
    extra = db.Column(Unicode(length=200))
    # 0 means confirmed, 1 means not confirm
    active = db.Column(SmallInteger)
    # 1~3 1 means danger, 3 means less important
    level = db.Column(SmallInteger)

