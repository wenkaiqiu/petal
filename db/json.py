import json
import logging
import os

from .base import Database

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('db.json')
logger.setLevel(logging.DEBUG)

project_path = os.path.join(os.getcwd().split("petal")[0], "petal")


class JSON(Database):
    """
    用于访问JSON文件的数据库类，实现抽象父类Database定义的接口
    """
    # 目前仅用于mock，故固定文件路径，而不是从conf文件读取
    json_path = {
        "model": project_path + "\contrib\mock\model.json",
        "device": project_path + "\contrib\mock\device.json",
        "configuration": project_path + "\contrib\mock\configuration.json",
        "part": project_path + "\contrib\mock\part.json",
        "space": project_path + "\contrib\mock\space.json",
        "wire": project_path + "\contrib\mock\wire.json",
        "status": project_path + "\contrib\mock\status.json",
    }

    @classmethod
    def set_conf(cls, conf):
        # 对JSON类无用，故仅打印
        logger.info("<JSON> set_conf")

    @classmethod
    def get_models(cls):
        with open(cls.json_path["models"]) as models_json:
            models = json.load(models_json)

        logger.info(f"get model: {models}")
        return models

    @classmethod
    def get_operations(cls, device_id):
        with open(cls.json_path["operations"]) as operations_json:
            operations = json.load(operations_json)

        logger.info(f"get model: {operations}")
        return list(filter(lambda x: x['device_id'] == device_id, operations))

    @classmethod
    def get_all_device_detail(cls):
        with open(cls.json_path["devices"]) as devices_json:
            devices = json.load(devices_json)

        logger.info(f"get devices: {devices}")
        return devices

    @classmethod
    def get_device_detail(cls, device_id):
        with open(cls.json_path["devices"]) as devices_json:
            devices = json.load(devices_json)
        device = list(filter(lambda x: x["id"] == device_id, devices))
        logger.info(f"get device: {device}")
        if device:
            return device[0]
        else:
            return None
