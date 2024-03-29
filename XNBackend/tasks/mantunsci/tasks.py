# -*- coding: utf-8 -*-
import redis
import requests
from datetime import datetime, timedelta
import logging
from XNBackend.tasks import celery
from XNBackend.tasks.utils import get_mantunsci_addr_mapping, MantunsciRealTimePower,\
    EnergyConsumeDay, ElectriConsumeHour, EnergyAlarm
from XNBackend.models import db, MantunciBox
from XNBackend.api_client.mantunsci import MantunsciAuthInMemory

mantunsci_config = celery.flask_app.config
auth_param = {
    'auth_url': mantunsci_config['MANTUNSCI_AUTH_URL'],
    'username': mantunsci_config['MANTUNSCI_USERNAME'],
    'password': mantunsci_config['MANTUNSCI_PASSWORD'],
    'app_key': mantunsci_config['MANTUNSCI_APP_KEY'],
    'app_secret': mantunsci_config['MANTUNSCI_APP_SECRET'],
    'redirect_uri': mantunsci_config['MANTUNSCI_REDIRECT_URI'],
    'router_uri': mantunsci_config['MANTUNSCI_ROUTER_URI'],
    'project_code': mantunsci_config['MANTUNSCI_PROJECT_CODE']
}

L = logging.getLogger(__name__)


@celery.task()
def periodic_realtime_power():
    mapping = get_mantunsci_addr_mapping()
    R = redis.Redis(host=mantunsci_config['REDIS_HOST'], port=mantunsci_config['REDIS_PORT'])
    s = requests.Session()
    s.auth = MantunsciAuthInMemory(
        auth_param['auth_url'],
        auth_param['username'],
        auth_param['password'],
        auth_param['app_key'],
        auth_param['app_secret'],
        auth_param['redirect_uri'],
    )

    for mb in MantunciBox.query:
        req_body = {"method": "GET_BOX_CHANNELS_REALTIME",
                    "projectCode": auth_param['project_code'],
                    "mac": mb.mac}
        realtime_mb_power = MantunsciRealTimePower(mb.mac,
                                                   mb.id,
                                                   s,
                                                   auth_param['router_uri'],
                                                   auth_param['project_code'],
                                                   R,
                                                   req_body)
        realtime_mb_power.load_data_from_response(mapping)
        realtime_mb_power.compress_records()
        realtime_mb_power.save_data()


@celery.task()
def periodic_electricity_usage_hour():
    """每天凌晨12点10分同步昨天的每小时耗电量"""
    mbs = MantunciBox.query
    s = requests.Session()
    s.auth = MantunsciAuthInMemory(
        auth_param['auth_url'],
        auth_param['username'],
        auth_param['password'],
        auth_param['app_key'],
        auth_param['app_secret'],
        auth_param['redirect_uri'],
    )
    session = db.session
    current_time = datetime.now() + timedelta(days=-1)
    for mb in mbs:
        req_body = {
            "method": "GET_BOX_HOUR_POWER",
            "projectCode": auth_param['project_code'],
            'mac': mb.mac,
            'year': current_time.year,
            'month': current_time.month,
            'day': current_time.day
        }
        elec_hour = ElectriConsumeHour(mb.mac,
                                       mb.id,
                                       s,
                                       auth_param['router_uri'],
                                       auth_param['project_code'])
        elec_hour.load_data_from_response(req_body)
        elec_hour.save_data(db_session=session)


@celery.task()
def periodic_electricity_usage_day():
    """每天凌晨获取前一天的日消耗"""
    mbs = MantunciBox.query
    session = db.session
    s = requests.Session()
    s.auth = MantunsciAuthInMemory(
        auth_param['auth_url'],
        auth_param['username'],
        auth_param['password'],
        auth_param['app_key'],
        auth_param['app_secret'],
        auth_param['redirect_uri'],
    )
    current_time = datetime.now() + timedelta(days=-1)
    for mb in mbs:
        L.debug('====================start debug=================')
        L.debug(current_time.month)
        L.debug(current_time.day)
        req_body = {
            "method": "GET_BOX_DAY_POWER",
            "projectCode": auth_param['project_code'],
            'mac': mb.mac,
            'year': current_time.year,
            'month': current_time.month,
            'day': current_time.day
        }
        elec_day = EnergyConsumeDay(mb.mac,
                                    mb.id,
                                    s,
                                    auth_param['router_uri'],
                                    auth_param['project_code'])
        elec_day.load_data_from_response(req_body)
        elec_day.compress_records()
        elec_day.save_data(db_session=session)


@celery.task()
def periodic_sync_alarm_data():
    mapping = get_mantunsci_addr_mapping()
    mbs = MantunciBox.query
    session = db.session
    s = requests.Session()
    s.auth = MantunsciAuthInMemory(
        auth_param['auth_url'],
        auth_param['username'],
        auth_param['password'],
        auth_param['app_key'],
        auth_param['app_secret'],
        auth_param['redirect_uri'],
    )
    current_time = datetime.now() + timedelta(minutes=-6)
    for mb in mbs:
        req_body = {
            "method": "GET_BOX_ALARM",
            "projectCode": auth_param['project_code'],
            "mac": mb.mac,
            "end": current_time.strftime("%Y-%m-%d %H:%M")
        }
        energy_alarm = EnergyAlarm(
            mb.mac,
            mb.id,
            s,
            auth_param['router_uri'],
            auth_param['project_code']
        )
        energy_alarm.load_data_from_response(req_body, mapping)
        energy_alarm.save_data(db_session=session)
