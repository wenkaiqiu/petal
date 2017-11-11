import logging

from uniform_model.actions import link

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.actions.link_factory')
logger.setLevel(logging.DEBUG)


class LinkFactory:
    """
    生成link函数，流程如下：
    1.根据连接参数中的设备ID获取设备实例，并检查是否存在
    """

    def generate(self, link_info, devices):
        logger.info('<LinkFactory> generate link instance')
        # 1.获取设备实例
        device_a = devices.get(link_info['device_id_a'])
        device_b = devices.get(link_info['device_id_b'])

        if device_a is None:
            logger.error(f'device which id is {link_info["device_id_a"]} is not exit')
            raise Exception(f'device which id is {link_info["device_id_a"]} is not exit')
        if device_b is None:
            logger.error(f'device which id is {link_info["device_id_b"]} is not exit')
            raise Exception(f'device which id is {link_info["device_id_b"]} is not exit')

        link_info.update({'device_a': device_a, 'device_b': device_b})
        return lambda: link(device_a, device_b, link_info)
