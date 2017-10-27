import json
import logging

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('database')
logger.setLevel(logging.DEBUG)


class Database:
    @classmethod
    def set_conf(cls, conf):
        logger.info("<Database> set_conf")
        # todo: 完善, 包括database.json
        pass

    @classmethod
    def get_models(cls):
        with open("./mock/models.json") as models_json:
            models = json.load(models_json)

        logger.info(f"get models: {models}")
        return models

    @classmethod
    def get_all_device_detail(cls):
        with open("./mock/devices.json") as devices_json:
            devices = json.load(devices_json)

        logger.info(f"get devices: {devices}")
        return devices

    @classmethod
    def get_device_detail(cls, device_id):
        with open("./mock/devices.json") as devices_json:
            devices = json.load(devices_json)

        device = list(filter(lambda x: x["id"] == device_id, devices))[0]
        logger.info(f"get device: {device}")
        return device
