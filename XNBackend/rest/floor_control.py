import logging
import time
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
import concurrent.futures
from XNBackend.api_client.light import sp_control_light
from XNBackend.models import SwitchPanel, AirConditioner
from XNBackend.tasks.air_condition.tasks import send_cmd_to_air_condition
from XNBackend.utils import get_socket_client, is_work_time

L = logging.getLogger(__name__)

floor_control_parser = reqparse.RequestParser()
floor_control_parser.add_argument('floor',
                                  required=True,
                                  type=int,
                                  help='please provide floor parameter')
floor_control_parser.add_argument('action',
                                  required=True,
                                  type=int,
                                  help='please provide control action, 1 means turn on, 0 means turn off.')
floor_control_parser.add_argument('resource_type',
                                  required=True,
                                  type=int,
                                  help='please provide control resource type 0 means light, 1 means air condition')


def sp_control_inline(args):
    tcp_obj = args[0]
    sp_list = args[1]
    main = args[2]
    aux = args[2]
    try:
        conn = get_socket_client(tcp_obj.ip,
                                 4196,
                                 timeout=5)
        time.sleep(0.5)
        for sp in sp_list:
            sp_control_light(conn, sp, main=main, aux=aux)
            time.sleep(0.5)
        conn.close()
    except Exception as e:
        L.exception(e)


class FloorControl(Resource):
    @jwt_required
    def patch(self):
        if is_work_time():
            return {"code": -1, "message": "can not batch control during work time."}
        args = floor_control_parser.parse_args()
        floor = args.get('floor')
        action = args.get('action')
        resource_type = args.get('resource_type')

        # light control
        if resource_type == 0:
            switch_panels = SwitchPanel.query.filter(SwitchPanel.locator_id.like(str(floor)+'%'))
            sp_collection = {}
            for sp in switch_panels:
                if sp.tcp_config is None:
                    continue
                if sp.tcp_config not in sp_collection:
                    sp_collection[sp.tcp_config] =[sp]
                else:
                    sp_collection[sp.tcp_config].append(sp)
            arg_group = [(k, v, action) for k, v in sp_collection.items()]
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(sp_control_inline, arg_group)
            return {"code": 0, "message": "light cmd sent"}

        # air condition control
        elif resource_type == 1:
            air_conditions = AirConditioner.query.filter(AirConditioner.locator_id.like(str(floor) + '%'))
            device_index_codes = [ac.device_index_code for ac in air_conditions]
            for d_code in device_index_codes:
                print(d_code)
                send_cmd_to_air_condition.apply_async(args=[d_code],
                                                      kwargs={"StartStopStatus": action},
                                                      queue="general")
            return {"code": 0, "message": "air condition cmd sent"}
