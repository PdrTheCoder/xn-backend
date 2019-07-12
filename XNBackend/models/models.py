# -*- coding:utf-8 -*-
from .base import db

from sqlalchemy import ForeignKey, Unicode, BOOLEAN, TIMESTAMP, String, \
    SmallInteger, Integer, Float
from sqlalchemy.orm import relationship

SHORT_LEN = 30
MEDIUM_LEN = 50
LONG_LEN = 100


class TimeStampMixin:
    created_at = db.Column(TIMESTAMP)
    updated_at = db.Column(TIMESTAMP)


class CarbonMixin:
    carbon_mixin_factor = 0.33
    carbon_mixin_watt_attr_name = ''
    @property
    def carbon_emission(self):
        return getattr(self, self.carbo_mixin_watt_attr_name) * self.carbon_mixin_factor


class Users(db.Model, TimeStampMixin):
    __tablename__ = 'users'
    '''sync from hik'''
    id = db.Column(Integer, primary_key=True)
    person_id = db.Column(Unicode(length=MEDIUM_LEN), index=True)
    person_name = db.Column(Unicode(length=SHORT_LEN))
    job_no = db.Column(String(MEDIUM_LEN))
    gender = db.Column(SmallInteger)
    org_path = db.Column(String(MEDIUM_LEN))
    org_index_code = db.Column(String(MEDIUM_LEN))
    org_name = db.Column(String(MEDIUM_LEN))
    certificate_type = db.Column(Integer)
    certificate_no = db.Column(String(MEDIUM_LEN))
    phone_no = db.Column(String(SHORT_LEN))
    address = db.Column(String(LONG_LEN))
    email = db.Column(String(MEDIUM_LEN))
    education = db.Column(SmallInteger)
    nation = db.Column(SmallInteger)
    photo_url = db.Column(String(LONG_LEN))


class UserLogins(db.Model, TimeStampMixin):
    __tablename__ = 'user_logins'
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Unicode(length=MEDIUM_LEN), ForeignKey(Users.person_id,
                                                               ondelete='CASCADE'))
    username = db.Column(Unicode(length=MEDIUM_LEN))
    password = db.Column(String(MEDIUM_LEN))
    level = db.Column(SmallInteger)
    
    @property
    def leverl_repr(self):
        if self.level == 0:
            return 'visitor'
        if self.level == 1:
            return 'employee'
        if self.level == 2:
            return 'sub_admin'
        if self.level == 3:
            return 'admin'


class Locators(db.Model, TimeStampMixin):
    __tablename__ = 'locators'
    internal_code = db.Column(Unicode(length=MEDIUM_LEN), primary_key=True)
    description = db.Column(String(LONG_LEN))
    floor = db.Column(Integer)
    zone = db.Column(Integer)
    # coorX, coorY and coorZ may not necessary
    coorX = db.Column(Float, nullable=True)
    coorY = db.Column(Float, nullable=True)
    coorZ = db.Column(Float, nullable=True)


class TrackingDevices(db.Model, TimeStampMixin):
    __tablename__ = 'tracking_devices'
    id = db.Column(Integer, primary_key=True)
    device_index_code = db.Column(Unicode(length=MEDIUM_LEN), index=True)
    name = db.Column(String(MEDIUM_LEN))
    locator = db.Column(Unicode(length=MEDIUM_LEN), 
                        ForeignKey(Locators.internal_code,
                                   ondelete='SET NULL'))
    # 0 means camera, 1 means acs
    device_type = db.Column(SmallInteger)


class AcsRecords(db.Model, TimeStampMixin):
    id = db.Column(Integer, primary_key=True)
    acs_id = db.Column(Integer, ForeignKey(TrackingDevices.id,
                                           ondelete="CASCADE"))
    status = db.Column(SmallInteger)
    event_type = db.Column(Integer)


class AppearRecords(db.Model, TimeStampMixin):
    __tablename__ = 'appear_records'
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey(Users.id,
                                            ondelete='CASCADE'))
    device_id = db.Column(Integer, ForeignKey(TrackingDevices.id,
                                              ondelete="CASCADE"))


class HeatMapSnapshots(db.Model, TimeStampMixin):
    __tablename__ = 'heatmap_snapshots'
    id = db.Column(Integer, primary_key=True)
    device_id = db.Column(Integer, ForeignKey(TrackingDevices.id,
                                              ondelete="CASCADE"))
    count = db.Column(Integer)


class CircuitBreakers(db.Model, TimeStampMixin):
    __tablename__ = 'circuit_breakers'
    id = db.Column(Integer, primary_key=True)
    mac = db.Column(Unicode(length=MEDIUM_LEN), index=True)
    name = db.Column(String(SHORT_LEN))
    phone = db.Column(String(SHORT_LEN))
    locator = db.Column(Unicode(length=MEDIUM_LEN), ForeignKey(Locators.internal_code,
                                            ondelete='SET NULL'))
    room = db.Column(String(SHORT_LEN))
    unit = db.Column(String(SHORT_LEN))


class CircuitRecords(db.Model, TimeStampMixin):
    __tablename__ = 'circuit_records'
    id = db.Column(Integer, primary_key=True)
    circuit_breaker_id = db.Column(Integer, ForeignKey(CircuitBreakers.id,
                                                       ondelete='CASCADE'))
    addr = db.Column(Integer)
    title = db.Column(String(MEDIUM_LEN))
    validity = db.Column(BOOLEAN)
    enable_netctr = db.Column(BOOLEAN)
    oc = db.Column(BOOLEAN)
    online = db.Column(BOOLEAN)
    total_power = db.Column(Float)
    mxgg = db.Column(Float)
    mxgl = db.Column(Float)
    line_type = db.Column(SmallInteger)
    spec = db.Column(String(MEDIUM_LEN))
    control = db.Column(BOOLEAN)
    visibility = db.Column(BOOLEAN)
    alarm = db.Column(Integer)
    gLd = db.Column(Float)
    gA = db.Column(Float)
    gT = db.Column(Float)
    gV = db.Column(Float)
    gW = db.Column(Float)
    gPF = db.Column(Float)
    aA = db.Column(Float)
    aT = db.Column(Float)
    aV = db.Column(Float)
    aW = db.Column(Float)
    aPF = db.Column(Float)
    bA = db.Column(Float)
    bT = db.Column(Float)
    bV = db.Column(Float)
    bW = db.Column(Float)
    bPF = db.Column(Float)
    cA = db.Column(Float)
    cT = db.Column(Float)
    cV = db.Column(Float)
    cW = db.Column(Float)
    cPF = db.Column(Float)
    nA = db.Column(Float)
    nT = db.Column(Float)


class LatestCircuitRecord(db.Model):
    __tablename__ = 'latest_circuit_record'
    id = db.Column(Integer, primary_key=True)
    circuit_id = db.Column(Integer, ForeignKey(CircuitBreakers.id,
                                               ondelete='CASCADE'), index=True)
    circuit_record_id = db.Column(Integer, ForeignKey(CircuitRecords.id,
                                                      ondelete='SET NULL'))
    circuit_breaker = relationship('CircuitBreaker', backref='latest_record')
    circuit_record = relationship('CircuitRecord')


class CircuitAlarms(db.Model, TimeStampMixin):
    __tablename__ = 'circuit_alarms'
    id = db.Column(Integer, primary_key=True)
    circuit_breaker_id = db.Column(Integer, ForeignKey(CircuitBreakers.id, 
                                                       ondelete='CASCADE'),
                                   nullable=False)
    addr = db.Column(Integer)
    node = db.Column(String(MEDIUM_LEN))
    alarm_or_type = db.Column(String(SHORT_LEN))
    info = db.Column(String(MEDIUM_LEN))
    type_number = db.Column(SmallInteger)

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
            9: '漏电保护功能正常'
        }
        return alarm_info_mapping[self.type_number]


class LatestAlarm(db.Model, TimeStampMixin):
    __tablename__ = 'latest_alarms'
    id = db.Column(Integer, primary_key=True)
    circuit_id = db.Column(Integer, ForeignKey(CircuitBreakers.id,
                                               ondelete='CASCADE'), index=True)
    circuit_alarm_id = db.Column(Integer, ForeignKey(CircuitAlarms.id, 
                                                     ondelete='SET NULL'))
    circuit = relationship('CircuitBreaker')
    alarm = relationship('CircuitAlarms')


class EnergyConsumeDaily(db.Model, TimeStampMixin, CarbonMixin):
    __tablename__ = 'energy_consume_daily'
    carbon_mixin_watt_attr_name = 'electricity'
    consume_id = db.Column(Integer, primary_key=True)
    circuit_breaker = db.Column(Integer, ForeignKey(CircuitBreakers.id,
                                                    ondelete='CASCADE'))
    addr = db.Column(Integer)
    electricity = db.Column(Float)
    # 统计时刻电量, 单位 KWH
    # total_electricity = db.Column(Float)


class EnegyConsumeMonthly(db.Model, TimeStampMixin):
    __tablename__ = 'energy_consume_monthly'
    consume_id = db.Column(Integer, primary_key=True)
    circuit_breaker = db.Column(Integer, ForeignKey(CircuitBreakers.id))
    addr = db.Column(Integer)
    electricity = db.Column(Float)
    # 统计时刻电量, 单位 KWH
    # total_electricity = db.Column(Float)


class IRSensorStatus(db.Model, TimeStampMixin):
    __tablename__ = 'ir_sensor_status'
    id = db.Column(Integer, primary_key=True)
    sensor_id = db.Column(Integer, ForeignKey("ir_sensors.id",
                                              ondelete="CASCADE"))
    value = db.Column(BOOLEAN)
    sensor = relationship('IRSensors')


# TODO 是查询还是推送
class IRSensors(db.Model, TimeStampMixin):
    __tablename__ = 'ir_sensors'
    id = db.Column(Integer, primary_key=True)
    device_index_code = db.Column(Unicode(length=MEDIUM_LEN), index=True)
    locator = db.Column(Unicode(length=MEDIUM_LEN), ForeignKey(Locators.internal_code,
                                            ondelete='SET NULL'))
    latest_record_id = db.Column(Integer, ForeignKey(IRSensorStatus.id,
                                                     ondelete="SET NULL"))
    latest_record = relationship('IRSensorStatus')


class AQIValues(db.Model, TimeStampMixin):
    __tablename__ = 'aqi_values'
    # 只有主动查询
    id = db.Column(Integer, primary_key=True)
    sensor_id = db.Column(Integer, ForeignKey("aqi_sensors.id",
                                              ondelete="CASCADE"))
    temperature = db.Column(Float)
    humidity = db.Column(Float)
    pm25 = db.Column(Float)
    co2 = db.Column(Float)
    tvoc = db.Column(Float)
    voc = db.Column(Float)
    sensor = relationship('AQISensors')


class AQISensors(db.Model, TimeStampMixin):
    __tablename__ = 'aqi_sensors'
    id = db.Column(Integer, primary_key=True)
    device_index_code = db.Column(Unicode(length=MEDIUM_LEN), index=True)
    locator = db.Column(Unicode(length=MEDIUM_LEN), ForeignKey(Locators.internal_code,
                                            ondelete='SET NULL'))
    latest_record_id = db.Column(Integer, ForeignKey(AQIValues.id,
                                                     ondelete="SET NULL"))
    latest_record = relationship('AQIValues')


class LuxValues(db.Model, TimeStampMixin):
    __tablename__ = 'lux_values'
    # 只有主动查询
    id = db.Column(Integer, primary_key=True)
    sensor_id = db.Column(Integer, ForeignKey("lux_sensors.id",
                                              ondelete='CASCADE'))
    value = db.Column(Integer)
    sensor = relationship('LuxSensors')


class LuxSensors(db.Model, TimeStampMixin):
    __tablename__ = 'lux_sensors'
    id = db.Column(Integer, primary_key=True)
    device_index_code = db.Column(Unicode(length=MEDIUM_LEN), index=True)
    locator = db.Column(Unicode(length=MEDIUM_LEN), ForeignKey(Locators.internal_code,
                                            ondelete='SET NULL'))
    latest_record_id = db.Column(Integer, ForeignKey(LuxValues.id,
                                                     ondelete="SET NULL"))
    latest_record = relationship('LuxValues')


class FireAlarmStatus(db.Model, TimeStampMixin):
    __tablename__ = 'fire_alarm_status'
    id = db.Column(Integer, primary_key=True)
    sensor_id = db.Column(Integer, ForeignKey('fire_alarm_sensors.id',
                                              ondelete='CASCADE'))
    value = db.Column(SmallInteger)
    sensor = relationship('FireAlarmSensors')


class FireAlarmSensors(db.Model, TimeStampMixin):
    __tablename__ = 'fire_alarm_sensors'
    id = db.Column(Integer, primary_key=True)
    device_index_code = db.Column(Unicode(length=MEDIUM_LEN), index=True)
    locator = db.Column(Unicode(length=MEDIUM_LEN),
                        ForeignKey(Locators.internal_code,
                                   ondelete='SET NULL'))
    latest_record_id = db.Column(Integer, 
                                 ForeignKey('fire_alarm_status.id',
                                            ondelete='SET NULL'))
    latest_record = relationship('FireAlarmStatus')


class SwitchStatus(db.Model, TimeStampMixin):
    __tablename__ = 'switch_status'
    id = db.Column(Integer, primary_key=True)
    sensor_id = db.Column(Integer, ForeignKey('switches.id',
                                              ondelete='CASCADE'))
    value = db.Column(SmallInteger)
    load = db.Column(Integer)
    sensor = relationship('Switches')


class Switches(db.Model, TimeStampMixin):
    __tablename__ = 'switches'
    id = db.Column(Integer, primary_key=True)
    device_index_code = db.Column(Unicode(length=MEDIUM_LEN), index=True)
    channel = db.Column(Integer)
    locator = db.Column(Unicode(length=MEDIUM_LEN), 
                        ForeignKey(Locators.internal_code,
                                   ondelete='SET NULL'))
    latest_record_id = db.Column(Integer,
                                 ForeignKey('switch_status.id',
                                            ondelete='SET NULL'))
    latest_record = relationship('SwitchStatus')


class ElevatorStatus(db.Model, TimeStampMixin):
    __tablename__ = 'elevator_status'
    id = db.Column(Integer, primary_key=True)
    elevator_id = db.Column(Integer, ForeignKey('elevators.id',
                                                ondelete='CASCADE'))
    floor = db.Column(Integer)
    direction = db.Column(SmallInteger)
    elevator = relationship('Elevators')

    @property
    def direction(self):
        mapping = {1: "up",
                   2: "down",
                   0: "stop"}
        return mapping(self.direction)


class Elevators(db.Model, TimeStampMixin):
    __tablename__ = 'elevators'
    id = db.Column(Integer, primary_key=True)
    device_index_code = db.Column(Unicode(length=MEDIUM_LEN), index=True)
    locator = db.Column(Unicode(length=MEDIUM_LEN), ForeignKey(Locators.internal_code,
                                            ondelete='SET NULL'))
