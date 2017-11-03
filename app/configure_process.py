import json
import logging
from functools import reduce

# from .factories import DatabaseFactory
from app.factories import DeviceFactory, LinkFactory, OperationFactory, DatabaseFactory
from app.generator import ConfigurationGenerator
from .parser import Parser

from app.validators import OperationValidator
from uniform_model import TemplateManager, DeviceManager
from uniform_model.templates.port import InterfaceManager
from uniform_model.templates import Template

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('app.configure_process')
logger.setLevel(logging.DEBUG)

import os
project_path = os.path.join(os.getcwd().split("petal")[0], "petal")

# 配置文件路径集合
conf_path = {
    "database": project_path + "\conf\database.json",
    "device": project_path + "\conf\device.json",
    "interface": project_path + "\conf\interface.json",
    "model": project_path + "\conf\model.json",
    "parser": project_path + "\conf\parser.json"
}


def configure_database():
    """
    配置数据库基础信息
    :return: database
    """
    logger.info("configure <database> start")
    with open(conf_path["database"], "r") as database_conf_file:
        database_conf = json.load(database_conf_file)
        database = DatabaseFactory().generate(conf=database_conf)
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


def configure_template():
    """
    配置ModelManager
    :return: None
    """
    logger.info("configure <ModelManager> start")
    with open(conf_path["model"], "r") as model_conf_json:
        model_conf = json.load(model_conf_json)
        TemplateManager.set_conf(model_conf)
    logger.info("configure <ModelManager> end")


def configure_device():
    # 配置Model
    logger.info("configure <Model> start")
    with open(conf_path["device"], "r") as device_conf_json:
        device_conf = json.load(device_conf_json)
        Template.set_device_conf(device_conf)
    logger.info("configure <Model> end")


def configure_interface():
    # 配置Interface
    logger.info("configure <Interface> start")
    with open(conf_path["interface"], "r") as interface_conf_json:
        interface_conf = json.load(interface_conf_json)
        InterfaceManager.set_conf(interface_conf)
    logger.info("configure <Interface> end")


def parse_input(parser, input_path):
    # 读取网络规划表并解析
    # 配置解析器
    logger.info("loading <input> start")
    with open(input_path, 'r') as input_json:
        input = json.load(input_json)
        devices_info, links_info, operations_info = parser.parse_input(input)
    logger.info("loading <input> end")
    return devices_info, links_info, operations_info


def instantiate_device(devices_info, database, tag):
    # 设备实例化
    logger.info("init device instances")
    device_factory = DeviceFactory(database, tag)
    devices = {}
    devices_failure = []
    for device_info in devices_info:
        device, failure = device_factory.generate(device_info)
        if device is not None:
            devices.update({device.id: device})
        if failure is not None:
            devices_failure.append(failure)
    return devices


def instantiate_link(links_info, devices):
    link_factory = LinkFactory()
    links = []
    links_failure = []
    for link_info in links_info:
        link, failure = link_factory.generate(link_info, devices)
        if link is not None:
            links.append(link)
            failure = link()  # 执行连接接操作, 错误在下面一起处理
        if failure is not None:
            links_failure.append(failure)
    return links


def instantiate_op(operations_info, devices):
    operation_factory = OperationFactory()
    operations = []
    operations_failure = []
    for operation_info in operations_info:
        operation, failure = operation_factory.generate(operation_info, devices)
        if operation is not None:
            operations.append(operation)
        if failure is not None:
            operations_failure.append(failure)
    return operations

def validate_op(operations):
    operation_validator = OperationValidator()
    op_failure = operation_validator.validate(operations)


def generate_configuration(devices):
    generator = ConfigurationGenerator()
    configs = generator.generate(devices.values())
    for config in configs:
        # print(config)
        for name, content in config.items():
            # print(content)
            with open(project_path + f"\output\config-{name}", "w") as output:
                if not content:
                    output.close()
                else:
                    for item in content:
                        # print(item)
                        # res = map(lambda a: a + "\n", reduce(lambda x, y: x + y, item.values()))
                        for line in item:
                            output.write(line)
                output.close()

def generate_topo(devices):
    generator = ConfigurationGenerator()
    post_r = generator.genarate_topo(devices.values())
    print(post_r)

    import requests
    r = requests.post("http://127.0.0.1:5000/request", data={"topo_json": json.dumps(post_r)})
    print(r.text)

    import webbrowser
    webbrowser.open("http://127.0.0.1:5000/render/" + str(json.loads(r.text)["result"]))


def processor(input_path, tag=False):
    database = configure_database()
    parser = configure_parser()
    configure_template()
    configure_device()
    configure_interface()
    devices_info, links_info, operations_info = parse_input(parser, input_path)
    devices = instantiate_device(devices_info, database, tag)
    print("current registed device: " + str(DeviceManager.list_all_registered()))
    links = instantiate_link(links_info, devices)
    operations = instantiate_op(operations_info, devices)
    validate_op(operations)
    generate_configuration(devices)
    generate_topo(devices)
