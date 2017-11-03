import json
import logging
import os

from .base import Database

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('db.json')
logger.setLevel(logging.DEBUG)

project_path = os.path.join(os.getcwd().split("petal")[0], "petal")


class JSON(Database):
    """
    目前仅用于mock，故固定文件路径
    """
    json_path = {
        "models": project_path + "\contrib\mock\models.json",
        "devices": project_path + "\contrib\mock\devices.json",
        "operations": project_path + "\contrib\mock\operations.json",
    }

    @classmethod
    def set_conf(cls, conf):
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
