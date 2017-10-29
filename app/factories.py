import logging
from functools import reduce

from app.database import Database
from models.actions import link, op, group
from models.devices import DeviceGroup
from models.functions import FunctionStack
from models.models import ModelManager
from utils.exceptions import error_string

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('factories')
logger.setLevel(logging.DEBUG)


class DeviceFactory:
    def __init__(self):
        logger.info("register models")
        # 注册Model，目前实行全注册
        # todo: 以后可改为按需注册
        models_info = Database.get_models()
        for model_info in models_info:
            ModelManager.register_model(model_info)

    def get_device_detail(self, device_info):
        return Database.get_device_detail(device_info["id"])

    def generate(self, device_info):
        """
        根据Model生成Device
        :param device_info:
        :return:
        """
        logger.info("<DeviceFactory> generate device instance")
        model_name = device_info["model_name"]
        # todo: 可能需要处理异常
        device_detail = self.get_device_detail(device_info)
        try:
            device = ModelManager.get_model(model_name).generate(device_detail)
        except AttributeError as e:
            print(e)
            return None, error_string(0, model_name)  # todo: error_code待定
        except Exception as e:
            print(e)
            return None, error_string(1, device_info)
        return device, None


class LinkFactory:
    """
    生成link函数，验证device是否存在，是否匹配，
    """

    def generate(self, link_info, devices):
        logger.info("<LinkFactory> generate link instance")
        device_a = devices.get(link_info['device_id_a'])
        device_b = devices.get(link_info['device_id_b'])

        if device_a is None:
            return None, f"device which id is {link_info['device_id_a']} is not exit"
        if device_b is None:
            return None, f"device which id is {link_info['device_id_b']} is not exit"

        return lambda: link(device_a, device_b, link_info), None


class FunctionFactory:
    __registed_functions = {
        "stack": FunctionStack
    }

    @classmethod
    def get_function_model(cls, function_name):
        return cls.__registed_functions.get(function_name, None)

    def generate(self, function_name):
        logger.info("<DeviceFactory> generate function instance")
        model = self.get_function_model(function_name)
        if model is not None:
            logger.info(f"<DeviceFactory> function name: {function_name}")
            return model()
        else:
            logger.info(f"<DeviceFactory> no function {function_name}")
            return None


class OperationFactory:
    """
    生成op函数，验证device是否支持该operation
    """

    def generate(self, operation_info, devices):
        logger.info("<OperationFactory> generate operation instance")
        print("operation_info['devices']: " + str(operation_info['devices']))
        # 获取设备实例
        op_devices = list(map(
            lambda x: devices.get(x) if not isinstance(x, list) else group(
                *list(map(lambda y: devices.get(y), x))),
            operation_info['devices']))
        for device in reduce(lambda a, b: a + b,
                             map(lambda y: [y] if not isinstance(y, DeviceGroup) else y.group, op_devices)):
            if device is None:
                return None, f"device which id is {operation_info['device_id_a']} is not exit"
        model = FunctionFactory.get_function_model(operation_info["type"])
        if model is None:
            return None, operation_info["type"]
        return lambda: op(model, *op_devices, **operation_info), None
