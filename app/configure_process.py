import json
import logging

from app.generator import ConfigurationGenerator
from app.validators import OperationValidator
from db import DatabaseFactory
from uniform_model.actions.link_factory import LinkFactory
from uniform_model.actions.operation_factory import OperationFactory
from uniform_model.devices.device_factory import DeviceFactory
from uniform_model.devices.link import Link
from uniform_model.devices.link_manager import LinkManager
from .parser import Parser

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('app.configure_process')
logger.setLevel(logging.DEBUG)

import os

project_path = os.path.join(os.getcwd().split("petal")[0], "petal")

# 配置文件路径集合
conf_path = {
    "database": project_path + "\\conf\\database.json",
    "parser": project_path + "\\conf\\parser.json",
    "visualization": project_path + "\\conf\\visualization.json",
}


def configure_database():
    """
    配置数据库基础信息,使用不同的接口。
    :return: database
    """
    # todo: Maybe：Restful API或直接操作数据库
    logger.info("configure <database> start")
    with open(conf_path["database"], "r") as database_conf_file:
        database_conf = json.load(database_conf_file)
        database = DatabaseFactory.get_database(conf=database_conf)
    logger.info("configure <database> end")
    return database


def configure_parser():
    """
    配置解析器
    :return: parser
    """
    logger.info("configure <parser> start")
    with open(conf_path["parser"], 'r') as parser_conf_file:
        parser_conf = json.load(parser_conf_file)
        parser = Parser(parser_conf)
    logger.info("configure <parser> end")
    return parser


def parse_input(parser, input_path):
    # 读取网络规划表并解析
    # 配置解析器
    logger.info("loading <panning table> start")
    with open(input_path, 'r') as input_json:
        input = json.load(input_json)
        devices_info, links_info, operations_info = parser.parse_input(input)
    logger.info("loading <panning table> end")
    return devices_info, links_info, operations_info


def instantiate_device(devices_info, database):
    """
    读取数据库，实例化设备信息,连接信息和配置信息
    :param devices_info: 规划表中的设备信息
    :param database: 数据库
    :return: 设备实例列表
    """
    logger.info("init device instances")
    device_factory = DeviceFactory()
    devices = {}

    for device_info in devices_info:
        # 从数据库获取设备信息
        device_detail = database.get_device_all_info(device_info["id"])
        device_info.update(**device_detail)
        device = device_factory.generate(device_info)
        if device is not None:
            devices.update({device.id: device})

    # 由于连接依赖设备实例，故单独处理
    links_info = database.get_links()
    for link_info in links_info:
        device_a = devices.get(link_info['device_id_a'])
        device_b = devices.get(link_info['device_id_b'])
        if device_a and device_b:
            link_info.update({'device_a': device_a, 'device_b': device_b})
            new_link = Link(**link_info)
            LinkManager.regist_link(new_link)
            device_a.links.append(new_link)
            device_b.links.append(new_link)

    return devices


def instantiate_link(links_info, devices):
    """
    根据连接信息，实例化连接，并进行连接操作
    :param links_info:
    :param devices:
    :return: None
    """
    link_factory = LinkFactory()
    for link_info in links_info:
        loc_link = link_factory.generate(link_info, devices)
        if loc_link is not None:
            loc_link()
        else:
            raise Exception(f'link() is None. {link_info}')


def instantiate_op(operations_info, devices):
    operation_factory = OperationFactory()
    operations = []
    for operation_info in operations_info:
        operation = operation_factory.generate(operation_info, devices)
        if operation is not None:
            operations.append(operation)
        else:
            raise Exception(f'op() is None. {operation_info}')
    return operations


def validate_op(operations):
    OperationValidator.validate(operations)


def generate_configuration(devices):
    logger.info('generate configuration')
    generator = ConfigurationGenerator()
    configs = generator.generate_conf(devices.values())  # 字典:{设备id：配置命令数组，每项为一个功能的配置}
    for device_name, content in configs.items():
        with open(project_path + f'\output\config-{device_name}', 'w') as output:
            if content:
                for item in content:
                    output.write(item)
                    output.write('\n')
            output.close()


def generate_topo(devices):
    generator = ConfigurationGenerator()
    post_r = generator.genarate_topo(devices.values())
    print(post_r)

    import requests
    with open(conf_path["visualization"], "r") as path_file:
        path = json.load(path_file)["base_url"]
    r = requests.post(path + "request", data={"topo_json": json.dumps(post_r)})
    print(r.text)

    import webbrowser
    webbrowser.open(path + "render/" + str(json.loads(r.text)["result"]))


def update_database(devices, links, database):
    # 写入或更新设备信息和配置信息
    for device in devices.values():
        database.update_device_all_info(device.id, device.to_database())
        for func in device.functions:
            if func.id:
                database.update_configuration(func.id, func.to_database())
            else:
                func.id = database.add_configuration(func.to_database())
    # 写入或更新连接信息
    for link in links:
        if link.id:
            database.update_link(link.id, link.to_database())
        else:
            link.id = database.add_link(link.to_database())


def processor(input_path):
    database = configure_database()
    parser = configure_parser()
    try:
        devices_info, links_info, operations_info = parse_input(parser, input_path)
    except KeyError as e:
        logger.error(e.args[0] + ' Details:')
        for item in e.args[1]:
            logger.error(item)
        raise
    devices = instantiate_device(devices_info, database)
    print("current registed device: " + str(devices))
    instantiate_link(links_info, devices)
    operations = instantiate_op(operations_info, devices)
    validate_op(operations)
    generate_configuration(devices)
    links = LinkManager.get_registed_links()
    update_database(devices, links, database)
    generate_topo(devices)


def processor2(src_device_id, des_device_id, conditions, params):
    min_bandwidth = conditions['bandwidth']
    # database = configure_database()
    # paths = database.get_paths(src_device_id, des_device_id)
    from contrib.mock.paths import paths
    devices = []
    device_path = []
    botten = {}
    for index, path in enumerate(paths):
        device_path.append([])
        for line in path:
            device_a = line['DeviceIdA']
            device_b = line['DeviceIdB']
            if device_a not in devices:
                devices.append(device_a)
            if device_b not in devices:
                devices.append(device_b)
            device_path[index].append((device_a, device_b))
            port_a = line['PortIdA']
            port_b = line['PortIdB']
            a_to_b = (device_a, device_b)
            b_to_a = (device_b, device_a)
            # 瓶颈参数获取
            loc = None
            loc_port = None
            if a_to_b in botten:
                loc = botten[a_to_b]
                loc_port = (port_a, port_b)
            elif b_to_a in botten:
                loc = botten[b_to_a]
                loc_port = (port_b, port_a)
            else:
                botten.update({a_to_b: {}})
                loc = botten[a_to_b]
                loc_port = (port_a, port_b)

            if loc_port not in loc:
                # wire_info = database.get_wire(device_a, port_a, device_b, port_b)
                # loc.append({loc_port: wire_info})
                loc.update({loc_port: {'bandwidth': '10'}})
                if loc_port == ('C3', 'E1'):
                    loc.update({loc_port: {'bandwidth': '5'}})
                if loc_port == ('C4', 'E2'):
                    loc.update({loc_port: {'bandwidth': '5'}})
    print(botten)
    print(devices)
    new_device_path = []
    for item in device_path:
        if item not in new_device_path:
            new_device_path.append(item)
    new_device_path.sort(key=lambda d: len(d))
    print(new_device_path)

    # 选取待配置设备,并生成配置项
    operations = []
    for i in range(len(new_device_path)):
        for line in new_device_path[i]:
            tag = True
            count = 0
            ports_collection = {line[0]: [], line[1]: []}
            for j in botten[line]:
                # print(int(botten[line][j]['bandwidth']))
                if int(botten[line][j]['bandwidth']) >= int(min_bandwidth):
                    tag = True
                    vlan_id = params['params']['vlan_id']
                    operations.append({
                        'devices': list(line),
                        'type': params['type'],
                        'params': [
                            {'vlan_id': vlan_id, 'vlan_type': 'interface', 'ports': [{'port_id': j[0], 'link_type': 'access'}]},
                            {'vlan_id': vlan_id, 'vlan_type': 'interface', 'ports': [{'port_id': j[1], 'link_type': 'access'}]}
                        ]
                    })
                    break
                else:
                    count += int(botten[line][j]['bandwidth'])
                    print(count)
                    ports_collection[line[0]].append(j[0])
                    ports_collection[line[1]].append(j[1])
                    if count >= int(min_bandwidth):
                        tag = True
                        operations.append({
                            'devices': list(line),
                            'type': 'trunk',
                            'params': [
                                {
                                    "trunk_port": [
                                        {
                                            "trunk_id": "1",
                                            "physical_port": ports_collection[line[0]]
                                        }
                                    ]
                                },
                                {
                                    "trunk_port": [
                                        {
                                            "trunk_id": "1",
                                            "physical_port": ports_collection[line[1]]
                                        }
                                    ]
                                }
                            ]})
                        operations.append({
                            'devices': list(line),
                            'type': params['type'],
                            'params': [
                                {'vlan_id': vlan_id, 'vlan_type': 'interface', 'ports': [{'port_id': 'eth-trunk 1', 'link_type': 'trunk'}]},
                                {'vlan_id': vlan_id, 'vlan_type': 'interface', 'ports': [{'port_id': 'eth-trunk 1', 'link_type': 'trunk'}]}
                            ]
                        })
                        break

                tag = False
        if tag:
            break
    print(operations)

    devices_info = list(map(lambda x: {'id':x}, devices))
    print(devices_info)

    database = configure_database()
    devices = instantiate_device(devices_info, database)
    print("current registed device: " + str(devices))
    operations2 = instantiate_op(operations, devices)
    validate_op(operations2)
    generate_configuration(devices)
    links = LinkManager.get_registed_links()
    update_database(devices, links, database)
    generate_topo(devices)