from flask_restful import Resource, reqparse
from XNBackend.task.hik.acs import *
from XNBackend.task.hik.task import acs_control 
from XNBackend.models.models import db, TrackingDevices, Locators, Door

acs_parser = reqparse.RequestParser()
acs_parser.add_argument('room_no', required=True, type=str)

acs_get_parser = reqparse.RequestParser()
acs_get_parser.add_argument('floor',
                            required=True,
                            type=str,
                            help='wrong floor parameter')


class AcsControl(Resource):
    def patch(self):
        args = acs_parser.parse_args()
        room_no = int(args.get('room_no'))

        device = TrackingDevices.query.filter(
            TrackingDevices.locator_body.has(zone=room_no)
        ).first()
        if not device:
            return ('can not find door acs device', 400)
        acs_control.delay(device.device_index_code, 2)
        return ('order has been initiated', 200)


class Acs(Resource):
    def get(self):
        args = acs_get_parser.parse_args()
        floor = args.get('floor')
        doors = Door.query.filter(Door.room_no_internal.like(floor+'%'))
        total_count = doors.count()
        total_open = doors.filter(Door.status == 1)
        total_open_count = total_open.count()
        status_dict = dict()
        for d in doors:
            status_dict[d.room_no_internal] = d.status
        return {
            'total': total_count,
            'open': total_open_count,
            'detail': status_dict
        }


class AcsEvent(Resource):
    def post(self):
        args = acs_post_parser.parse_args()
        method = args.get('method')
        params = args.get('params')['events'][0]
        print(params)
        '''
        if params.get('eventTypes') == '196893':
            face_recognition.delay(params['data']['ExtEventCardNo'], params['srcName'])
        elif params.get('eventTypes') == '198919':
            door_control.delay()
        elif params.get('eventTypes') == '198657':
            door_destroy.delay()
        '''





