import json
import logging

from contrib.rules import CX310, ProtocolIP
from contrib.utils import model_generator, operation_generator
from models.actions import op
from models.base import list_all_registered
from models.protocols import ProtocolStack

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('manifest')
logger.setLevel(logging.DEBUG)

logger.info(f'before loading')
with open('./input_1.json', 'r') as inputs:
    inputs_dict = json.load(inputs)
    logger.info(f'loading input: \n\t\t{inputs_dict}')

logger.info(f'after loading')

devices = {}
for device in inputs_dict['devices']:
    devices.update(model_generator(device))
print(devices)

operations = []
for operation in inputs_dict['operations']:
    operation["device"] = set(map(lambda x: devices[x], operation["device"]))
    operations.append(operation_generator(operation))
print(operations)
for func in operations:
    func()
# op(ProtocolTrunk, cx310_1, cx310_2, )
# op(ProtocolIP, group(cx310_1, cx310_2), cx310_3)
# op(ProtocolIP, cx310_3)
# logger.info(ProtocolTrunk.interfaces())
# logger.info(ProtocolStack.interfaces())
# logger.info(f'registered device: {list_all_registered()}')
# logger.info(f'CX310 registered interface: {cx310_1.interfaces()}')
# logger.info(f'CX310 registered interface type: {cx310_1.interface_types()}')
print("-----------------")
print(devices)
for logical_id in devices:
    print(type(devices[logical_id]))
    print(f"[{type(device)}_{device.slot_id} logical_id={device.logical_id}]")
    device.device_config()
    device.interface_config()

# with open('./output_test', 'w') as output:
#     json.dump(inputs_dict, output)
