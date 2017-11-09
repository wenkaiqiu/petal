import logging

from uniform_model.functions.stack import FunctionStack
from uniform_model.functions.trunk import FunctionTrunk
from uniform_model.functions.vlan import FunctionVLAN

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('app.factories.function_factory')
logger.setLevel(logging.DEBUG)


class FunctionFactory:
    __registed_functions = {
        'stack': FunctionStack,
        'trunk': FunctionTrunk,
        'vlan': FunctionVLAN
    }

    @classmethod
    def get_function_model(cls, function_name):
        return cls.__registed_functions.get(function_name, None)

    def generate(self, function_name, params):
        logger.info('<DeviceFactory> generate function instance')
        func_model = self.get_function_model(function_name)
        if func_model is not None:
            logger.info(f'<DeviceFactory> function name: {function_name}')
            return func_model(**params)
        else:
            logger.info(f'<DeviceFactory> no function {function_name}')
            return None
