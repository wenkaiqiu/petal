import logging

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('parser')
logger.setLevel(logging.DEBUG)

map_device = {
    "id": "id",
    "uuid": "uuid",
    "name": "name",
    "model_type": "model_name",
    "description": "description",
    "parent_id": "parent_id"
}

map_link = {
    "id": "id",
    "name": "name",
    "device_id_a": "device_id_a",
    "device_id_b": "device_id_b",
    "port_a": "port_a",
    "port_b": "port_b",
    "link_type": "link_type",
    "usage": "usage",
}

map_operation = {
    "type": "type",
    "devices": "devices",
    "params": "params"
}
class Parser:
    """
    解析网络规划表，并将内容提取转换为程序内部格式。
    parser.conf文件记录了解析器可解析的字段，字段名对应规划表内容。
    上部三个map记录了输入字段到程序内部使用字段的映射
    """
    def __init__(self, conf):
        self.device_conf, self.link_conf, self.operation_conf = self._set_conf(conf)
        logger.info(f'<device_conf>: {self.device_conf}')
        logger.info(f'<link_conf>: {self.link_conf}')
        logger.info(f'<operation_conf>: {self.operation_conf}')

    def _set_conf(self, conf):
        """
        配置参数，决定读取的json字段
        :param conf: 配置字典
        :return:
        """
        device_conf = filter(lambda x: conf["T_Device"][x], conf["T_Device"])
        link_conf = filter(lambda x: conf["T_Link"][x], conf["T_Link"])
        operation_conf = filter(lambda x: conf["T_Operation"][x], conf["T_Operation"])
        return list(device_conf), list(link_conf), list(operation_conf)

    def parse_input(self, input):
        devices = self._parse_devices(input["devices"])
        links = self._parse_links(input["links"])
        operations = self._parse_operations(input["operations"])

        logger.info(f'<parsed_devices>: {devices}')
        logger.info(f'<parsed_links>: {links}')
        logger.info(f'<parsed_operations>: {operations}')
        return devices, links, operations

    def _parse_devices(self, devices):
        new_devices = []
        for device in devices:
            new_device = map(lambda conf: (map_device[conf], device[conf]), self.device_conf)
            new_devices.append(dict(new_device))
        return new_devices

    def _parse_links(self, links):
        # print(links)
        new_links = []
        for link in links:
            new_link = map(lambda conf: (map_link[conf], link[conf]), filter(lambda x: x in self.link_conf, link))
            new_links.append(dict(new_link))
        # print(new_links)
        return new_links

    def _parse_operations(self, operations):
        new_operations = []
        for operation in operations:
            new_operation = map(lambda conf: (map_operation[conf], operation[conf]), self.operation_conf)
            new_operations.append(dict(new_operation))
        return new_operations
