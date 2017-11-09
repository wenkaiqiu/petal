import logging

from app.factories.base import Factory
from uniform_model import link

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('app.factories.link_factory')
logger.setLevel(logging.DEBUG)


class LinkFactory(Factory):
    """
    生成link函数，验证device是否存在，是否匹配，
    """

    def generate(self, link_info, devices):
        logger.info("<LinkFactory> generate link instance")
        print(link_info)
        device_a = devices.get(link_info['device_id_a'])
        device_b = devices.get(link_info['device_id_b'])

        if device_a is None:
            return None, f"device which id is {link_info['device_id_a']} is not exit"
        if device_b is None:
            return None, f"device which id is {link_info['device_id_b']} is not exit"

        return lambda: link(device_a, device_b, link_info), None
