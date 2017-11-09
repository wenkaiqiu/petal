import logging
from itertools import chain

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('app.parser')
logger.setLevel(logging.DEBUG)

"""
_map_device, _map_link, _map_operation记录了规划表内字段名到程序内部使用的字段名的映射。key为规划表字段名，value为程序内部使用的字段名，故不应修改value的值。
"""
_map_device = {
    'id': 'id',
    'uuid': 'uuid',
    'name': 'name',
    'description': 'description',
    'model_type': 'model_name',
    'parent_id': 'parent_id',
    'space': 'space',
    'status': 'status',
    'manager': 'manager'
}

_map_link = {
    'id': 'id',
    'name': 'name',
    'device_id_a': 'device_id_a',
    'device_id_b': 'device_id_b',
    'port_a': 'port_a',
    'port_b': 'port_b',
    'link_type': 'link_type',
    'usage': 'usage',
    'bandwidth': 'bandwidth',
    'unit': 'unit',
    'length': 'length'
}

_map_operation = {
    'type': 'type',
    'devices': 'devices',
    'params': 'params'
}


class Parser:
    """
    解析网络规划表，并将内容提取转换为程序内部格式。
    parser.conf文件记录了解析器可解析的字段，字段名对应规划表内容。
    上部三个map记录了输入字段到程序内部使用字段的映射
    """

    def __init__(self, conf):
        logger.info(f'init parser')
        self.device_conf, self.link_conf, self.operation_conf = self._set_conf(conf)
        logger.info(f'<device_conf>: {self.device_conf}')
        logger.info(f'<link_conf>: {self.link_conf}')
        logger.info(f'<operation_conf>: {self.operation_conf}')

    def _set_conf(self, conf):
        """
        配置解析器，用于决定读取的json字段以及哪些为必要字段
        :param conf: 配置内容
        :return:
        """
        logger.info(f'set conf')
        device_conf = conf['T_Device']
        link_conf = conf['T_Link']
        operation_conf = conf['T_Operation']
        return device_conf, link_conf, operation_conf

    def parse_input(self, planning_table):
        """
        解析规划表，通用流程如下：
        1. 检查是否必要字段都在：查看conf中value为true的字段是否都在
        2. 过滤解析的字段：仅读取在conf中记录的字段
        3. 映射为内部字段名

        程序会在遍历过程中将错误收到error_list中，推迟到遍历完成后统一处理。遍历完成后，程序raise所有错误，并在configure_process.py中打印

        :param planning_table: 规划表，dict格式
        :return: 解析后的设备信息，连接信息和配置信息
        """
        logger.info('start parse input')
        devices, devices_error = self._parse_devices(planning_table['devices'])
        links, links_error = self._parse_links(planning_table['links'])
        operations, op_error = self._parse_operations(planning_table['operations'])
        if any(chain(devices_error, links_error, op_error)):
            info = []
            for error in chain(devices_error, links_error, op_error):
                info.append(str(error)+'\n')
            raise KeyError('KeyError: lack necessary info in planning table.', info)
        logger.info(f'reading <parsed_devices>: {devices}')
        logger.info(f'reading <parsed_links>: {links}')
        logger.info(f'reading <parsed_operations>: {operations}')
        return devices, links, operations

    def _check_necessary(self, info, conf_type):
        conf = None
        if conf_type == 'device':
            conf = self.device_conf
        elif conf_type == 'link':
            conf = self.link_conf
        elif conf_type == 'operation':
            conf = self.operation_conf

        for item in filter(lambda x: conf[x], conf):
            if item not in info:
                return False
        return True

    def _parse_devices(self, devices_table):
        new_devices = []
        error_list = []
        for index, device in enumerate(devices_table):
            try:
                if self._check_necessary(device, 'device'):
                    new_device = map(lambda name: (_map_device[name], device[name]),  # 元组(<新名字>, <值>)
                                     filter(lambda item: item in self.device_conf,
                                            device))  # 使用filter函数过滤字段，使用map函数进行映射
                    new_devices.append(dict(new_device))  # 元组转为字典
                else:
                    raise KeyError(f'lacking necessary info in  No.{index+1} of device info of planning table.')
            except KeyError as e:
                error_list.append(e)
        return new_devices, error_list

    def _parse_links(self, links_table):
        new_links = []
        error_list = []
        for index, link in enumerate(links_table):
            try:
                if self._check_necessary(link, 'link'):
                    new_link = map(lambda name: (_map_link[name], link[name]),  # 元组(<新名字>, <值>)
                                   filter(lambda item: item in self.link_conf, link))  # 使用filter函数过滤字段，使用map函数进行映射
                    new_links.append(dict(new_link))  # 元组转为字典
                else:
                    raise KeyError(f'lacking necessary info in  No.{index+1} of link info of planning table.')
            except KeyError as e:
                error_list.append(e)
        return new_links, error_list

    def _parse_operations(self, operations_table):
        new_operations = []
        error_list = []
        try:
            for index, operation in enumerate(operations_table):
                if self._check_necessary(operation, 'operation'):
                    new_operation = map(lambda name: (_map_operation[name], operation[name]),  # 元组(<新名字>, <值>)
                                        filter(lambda item: item in self.operation_conf,
                                               operation))  # 使用filter函数过滤字段，使用map函数进行映射
                    new_operations.append(dict(new_operation))
                else:
                    raise KeyError(f'lacking necessary info in  No.{index+1} of operation info of planning table.')
        except KeyError as e:
            error_list.append(e)
        return new_operations, error_list


if __name__ == '__main__':
    test_conf = {
        'T_Device': {
            'id': True,
            'name': False
        },
        'T_Link': {
            'id': True,
            'name': False
        },
        'T_Operation': {
            'id': True,
            'name': False
        }
    }
    test_input = {
        'devices': [
            {
                'id': 1,
            },
            {
                'id': 1,
                'name': 'test'
            },
            {
                'name': 'test'
            },
        ],
        'links': [
            {
                'id': 1,
            },
            {
                'id': 1,
                'name': 'test'
            },
            {
                'name': 'test'
            },
        ],
        'operations': [
            {
                'id': 1,
            },
            {
                'id': 1,
                'name': 'test'
            },
            {
                'name': 'test'
            },
        ]
    }
    parser = Parser(test_conf)
    try:
        devices_info, links_info, operations_info = parser.parse_input(test_input)
        print(devices_info, links_info, operations_info)
    except Exception as e:
        logger.error(e.args[0] + ' Details:')
        for item in e.args[1]:
            logger.error(item)
