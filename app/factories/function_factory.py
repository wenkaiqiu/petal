import logging

from app.factories.base import Factory

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('app.factories.function_factory')
logger.setLevel(logging.DEBUG)


class FunctionFactory(Factory):
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