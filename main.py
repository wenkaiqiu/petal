import json
import logging
from functools import reduce

from app.database import Database
from app.factories import DeviceFactory, LinkFactory, OperationFactory
from app.generator import ConfigurationGenerator
from app.parser import Parser
from app.validators import OperationValidator
from models.devices import DeviceManager
from models.interfaces import InterfaceManager
from models.models import ModelManager, Model

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

# 配置解析器
logger.info("configure <parser> start")
parser_conf_path = "./conf/parser.json"
with open(parser_conf_path, 'r') as parser_conf_file:
    parser_conf = json.load(parser_conf_file)
parser = Parser(parser_conf)
logger.info("configure <parser> end")

# 读取网络规划表并解析
# 配置解析器
logger.info("loading <input> start")
input_path = "./mock/input_1.json"
with open(input_path, 'r') as input_json:
    input = json.load(input_json)
    devices_info, links_info, operations_info = parser.parse_input(input)
logger.info("loading <input> end")

# 配置数据库基础信息
logger.info("configure <database> start")
database_conf_path = "./conf/database.json"
with open(database_conf_path, "r") as database_conf_file:
    database_conf = json.load(database_conf_file)
    Database.set_conf(database_conf)
logger.info("configure <database> end")

# 配置ModelManager
logger.info("configure <ModelManager> start")
model_conf_path = "./conf/model.json"
with open(model_conf_path, "r") as model_conf_json:
    model_conf = json.load(model_conf_json)
    ModelManager.set_conf(model_conf)
logger.info("configure <ModelManager> end")

# 配置Model
logger.info("configure <Model> start")
device_conf_path = "./conf/device.json"
with open(device_conf_path, "r") as device_conf_json:
    device_conf = json.load(device_conf_json)
    Model.set_device_conf(device_conf)
logger.info("configure <Model> end")

# 配置Interface
logger.info("configure <Interface> start")
interface_conf_path = "./conf/interface.json"
with open(interface_conf_path, "r") as interface_conf_json:
    interface_conf = json.load(interface_conf_json)
    InterfaceManager.set_conf(interface_conf)
logger.info("configure <Interface> end")

# 设备实例化
logger.info("init device instances")
device_factory = DeviceFactory()
devices = {}
devices_failure = []
for device_info in devices_info:
    device, failure = device_factory.generate(device_info)
    if device is not None:
        devices.update({device.id: device})
    if failure is not None:
        devices_failure.append(failure)

print("current registed device: " + str(DeviceManager.list_all_registered()))

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

operation_factory = OperationFactory()
operations = []
operations_failure = []
for operation_info in operations_info:
    operation, failure = operation_factory.generate(operation_info, devices)
    if operation is not None:
        operations.append(operation)
    if failure is not None:
        operations_failure.append(failure)

operation_validator = OperationValidator()
op_failure = operation_validator.validate(operations)

generator = ConfigurationGenerator()
configs = generator.generate(devices.values())

for config in configs:
    # print(config)
    for name, content in config.items():
        # print(content)
        with open(f"./output/config-{name}", "w") as output:
            if not content:
                output.close()
            else:
                for item in content:
                    # print(item)
                    res = map(lambda a: a + "\n", reduce(lambda x, y: x + y, item.values()))
                    for line in res:
                        output.write(line)
            output.close()
