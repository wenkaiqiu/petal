import logging

from app.factories.base import Factory
from db.base import Database
from uniform_model import TemplateManager
from utils.exceptions import error_string

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('app.factories.device_factory')
logger.setLevel(logging.DEBUG)


class DeviceFactory(Factory):
    def __init__(self, database):
        logger.info("register uniform_model")
        # 注册Model，目前实行全注册
        # todo: 以后可改为按需注册
        self.database = database
        models_info = self.database.get_models()
        for model_info in models_info:
            TemplateManager.register_model(model_info)

    def get_device_detail(self, device_info):
        return self.database.get_device_detail(device_info["id"])

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
        device_detail.update({"parent_id": device_info["parent_id"]})
        # try:
        device = TemplateManager.get_model(model_name).generate(device_detail)
        # except AttributeError as e:
        #     print(e)
        #     return None, error_string(0, model_name)  # todo: error_code待定
        # except Exception as e:
        #     print(e)
        #     return None, error_string(1, device_info)
        return device, None