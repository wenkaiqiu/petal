import json
import logging
import os
import requests
from db.base import Database
from db.restful_map import *

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('db.json')
logger.setLevel(logging.DEBUG)

project_path = os.path.join(os.getcwd().split("petal")[0], "petal")

restful_map = {
    'board': board_map,
    'chassis': chassis_map,
    'ethernetInterface': ethernetInterface_map,
    'fan': fan_map,
    'manager': manager_map,
    'memory': memory_map,
    'pcie': pcie_map,
    'power': power_map,
    'processor': processor_map,
    'raid': raid_map,
    'server': server_map
}
space_map = {
    'Id': 'id',
    'SpaceType': 'space_type',
    'Name': 'name',
    'Direction': 'direction',
    'Serial': 'serial',
    'X': 'x',
    'Y': 'y',
    'Z': 'z',
    'DataCenter': 'data_center',
    'CreateTime': 'create_time',
    'UpdateTime': 'update_time'
}

link_map = {
    'Id': 'id',
    'DeviceIdA': 'device_id_a',
    'PortA': 'port_a',
    'DeviceIdB': 'device_id_b',
    'PortB': 'device_b',
    'Protocol': 'usage',
    'ProVersion': 'pro_version',
    'BandWidth': 'bandwidth',
    'Unit': 'unit',
    'CreateTime': 'create_time',
    'UpdateTime': 'update_time'
}


class RESTFul(Database):
    prefix = None
    part_info = {}
    json_path = {
        'configuration': project_path + '\\contrib\\mock\\configuration.json',
    }

    @classmethod
    def set_conf(cls, conf):
        cls.prefix = f'{conf["db_protocol"]}://{conf["db_host"]}:{conf["db_port"]}'

    @classmethod
    def get_device_all_info(cls, device_id):
        logger.info(f'get all device info')
        device_info = cls.get_device_info(device_id)
        parent_space_info = cls.get_parent_and_space(device_id)
        device_info.update(parent_space_info)
        logger.info(f'get all device info of {device_id}: {device_info}')

        return device_info

    @classmethod
    def update_device_all_info(cls, device_id, params):
        logger.info(f' update device all info: {params}')
        # cls.update_device_info(device_id, params)
        # if 'part' in params and 'space' in params:
        #     if 'id' in params['space']:
        #         cls.update_parent_and_space(device_id, params['part']['parent_id'], params['space'])
        #     else:
        #         cls.add_parent_and_space(device_id, params['part']['parent_id'], params['space'])

    @classmethod
    def get_device_info(cls, device_id):
        uri = f'{cls.prefix}/redfish/v1/rich/inventory/{device_id}'
        res = requests.get(uri).json()
        logger.info(f'get device info of {device_id}: {res}')
        category = 'server'
        # category = res['Category']
        loc_map = restful_map[category]
        info = {'model': {}, 'status': {}}
        for k, v in loc_map['model'].items():
            if v in res:
                info['model'].update({k: res[v]})
        for k, v in loc_map['device'].items():
            if v in res:
                info.update({k: res[v]})
        for k, v in loc_map['status'].items():
            if v in res:
                info['status'].update({k: res[v]})
            if 'Status' in res and v in res['Status']:
                info['status'].update({k: res['Status'][v]})
        # 定制修改
        category = cls.get_category(device_id)
        if category == 'switchPlane':
            category = 'switch'
            info['model'].update({'model_type': 'switchPlane'})
        if category == 'switchPort':
            category = 'port'
            info['model'].update({'model_type': 'switchPort'})
        if category == 'server':
            info.update({'id': device_id})
        info.update({'model_type': category})
        info['model'].update({'category': category})
        # 填充Name
        if 'name' not in info:
            if 'PlaneName' in res:
                info.update({'name': res['PlaneName']})
            if 'PortName' in res:
                info.update({'name': res['PortName']})
        return info

    @classmethod
    def get_category(cls, device_id):
        logger.info(f'get category of {device_id}')
        uri = f'{cls.prefix}/redfish/v1/rich/inventory/zhongkeyuan/001?id={device_id}'
        return requests.get(uri).json()['Category']

    @classmethod
    def update_device_info(cls, device_id, params):
        logger.info(f'update device info of {device_id}: {params}')
        uri = f'{cls.prefix}/redfish/v1/rich/inventory/{device_id}'
        category = params['model']
        loc_map = restful_map[category]
        info = {'Status': {}}
        for item in params['device']:
            if not item == 'model_type':
                info.update({loc_map['device'][item]: params['device'][item]})
        for item in params['status']:
            info['Status'].update({loc_map['status'][item]: params['status'][item]})
        request_info = {'DeviceInfo': info}
        res = requests.patch(uri, json.dumps(request_info))
        return res

    @classmethod
    def get_wire(cls, device_a, port_a, device_b, port_b):
        logger.info(f'get wire of {(device_a, port_a, device_b, port_b)}')
        uri = f'{cls.prefix}/redfish/v1/rich/inventory/zhongkeyuan/002'
        request_info = {
            "DeviceIdA": device_a,
            "DeviceIdB": device_b,
            "PortA": port_a,
            "PortB": port_b
        }
        res = requests.post(uri, json.dumps(request_info)).json()['WireInfo']
        re = {}
        for item in res:
            re.update({link_map[item]: res[item]})
        return re

    @classmethod
    def get_links(cls):
        uri = cls.prefix + '/redfish/v1/rich/inventory/zhongkeyuan/003'
        request_info = {
            "Filter": {
                "Protocol": "vlan",
                "BandWidth": [0, 13]
            },
            "Skip": 0,
            "Top": 10
        }
        res = requests.post(uri, json.dumps(request_info)).json()['Wires']
        re = []
        for item in res:
            re.append({
                'bandwidth': item['BandWidth'],
                'device_id_a': item['DeviceIdA'],
                'device_id_b': item['DeviceIdB'],
                'port_a': item['PortIdA'],
                'port_b': item['PortIdB'],
                'pro_version': item['ProVersion'],
                'protocol': item['Protocol'],
                'unit': item['Unit']
            })

        logger.info(f'get links: {re}')
        return re

    @classmethod
    def add_link(cls, params):
        logger.info(f'add link of {params}')
        uri = f'{cls.prefix}/redfish/v1/rich/inventory/wire'
        link_info = {
            'DeviceIdA': params['device_id_a'],
            'PortA': [params['port_a']],
            'DeviceIdB': params['device_id_b'],
            'PortB': [params['port_b']],
            'LinkInfo': [
                {
                    'Protocol': params['usage'] if 'usage' in params else '',
                    'ProVersion': params['pro_version'] if 'pro_version' in params else '',
                    'BandWidth': params['bandwidth'] if 'bandwidth' in params else '',
                    'Unit': params['unit'] if 'unit' in params else ''
                }
            ]
        }
        res = requests.post(uri, link_info)

    @classmethod
    def update_link(cls, link_id, params):
        logger.info(f"update link of {link_id}: {params}")
        uri = f'{cls.prefix}/redfish/v1/rich/inventory/wire'
        link_info = {
            'DeviceIdA': params['device_id_a'],
            'PortA': [params['port_a']],
            'DeviceIdB': params['device_id_b'],
            'PortB': [params['port_b']],
            'LinkInfo': [
                {
                    'Protocol': params['usage'] if 'usage' in params else '',
                    'ProVersion': params['pro_version'] if 'pro_version' in params else '',
                    'BandWidth': params['bandwidth'] if 'bandwidth' in params else '',
                    'Unit': params['unit'] if 'unit' in params else ''
                }
            ]
        }
        res = requests.patch(uri, json.dumps(link_info))

    @classmethod
    def get_paths(cls, src, des):
        logger.info(f'get routes from {src} to {des}')
        uri = f'{cls.prefix}/redfish/v1/rich/inventory/wire/router/routers?deviceida={src}&deviceidb={des}'
        res = requests.get(uri).json()['Routers']
        return res
    @classmethod
    def get_parent_and_space(cls, device_id):
        uri = f'{cls.prefix}/redfish/v1/rich/inventory/{device_id}/space'
        res = requests.get(uri).json()["DeviceSpace"]
        logger.info(f'get parent&space of {device_id}: {res}')
        if not res:
            return {}
        space_info = {}
        for k, v in res['SpaceInfo'].items():
            space_info.update({space_map[k]: v})
        res_info = {
            'space': space_info,
            'parent_id': res['ParentDeviceID']
        }
        return res_info

    @classmethod
    def add_parent_and_space(cls, device_id, parent_id, space_info):
        logger.info(f"add parent of {device_id}: {parent_id}")
        logger.info(f"add space of {device_id}: {space_info}")
        uri = f'{cls.prefix}/redfish/v1/rich/inventory/part'
        part_info = {}
        for k, v in space_map.items():
            if v in space_info:
                part_info.update({k: space_info[v]})
        request_info = {
            'DeviceID': parent_id,
            'PartInfo': [
                {
                    'ChildDeviceID': device_id,
                    'SpaceInfo': part_info
                }
            ]
        }
        res = requests.post(uri, json.dumps(request_info))

    @classmethod
    def update_parent_and_space(cls, device_id, parent_id, space_info):
        # 特别的，在RESTFUL接口中params需要包含parent_id,device_id
        logger.info(f"update parent of {device_id}: {parent_id}")
        logger.info(f"update space of {device_id}: {space_info}")
        uri = f'{cls.prefix}/redfish/v1/rich/inventory/part/{parent_id}'
        loc_space_info = {}
        for k, v in space_map.items():
            if v in space_info:
                loc_space_info.update({k: space_info[v]})
        request_info = {
            'PartInfo': [
                {
                    'ChildDeviceID': device_id,
                    'SpaceInfo': loc_space_info
                }
            ]
        }
        res = requests.patch(uri, json.dumps(request_info))

    @classmethod
    def get_manager(cls, device_id):
        uri = f'{cls.prefix}/redfish/v1/rich/inventory/devicemanager/{device_id}'
        res = requests.get(uri)
        logger.info(f"get managers of {device_id}: {res.json()['UserID']}")
        return res.json()['UserID']

    @classmethod
    def get_device_configurations(cls, device_id):
        with open(cls.json_path["configuration"]) as configuration_json:
            configurations = json.load(configuration_json)
        device_configurations = list(filter(lambda x: x['device_id'] == device_id, configurations))
        logger.info(f"get configurations of {device_id}: {device_configurations}")
        return device_configurations

    @classmethod
    def add_configuration(cls, params):
        logger.info(f'add configuration with params: {params}')
        with open(cls.json_path["configuration"], 'r') as configuration_json:
            configurations = json.load(configuration_json)
        with open(cls.json_path["configuration"], 'w') as configuration_json:
            conf_id = int(configurations[-1]['id']) if configurations else 0
            params.update({'id': str(conf_id + 1)})
            configurations.append(params)
            json.dump(configurations, configuration_json)
        return conf_id

    @classmethod
    def update_configuration(cls, conf_id, params):
        logger.info(f'update configuration of conf_id <{conf_id}> with params: {params}')
        with open(cls.json_path["configuration"], 'r') as configuration_json:
            configurations = json.load(configuration_json)
        with open(cls.json_path['configuration'], 'w') as configuration_json:
            item = cls.find_in_list(configurations, lambda x: x['id'] == conf_id)
            if item:
                item.update(params)
            json.dump(configurations, configuration_json)
