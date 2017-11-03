def parse_interface_id(port_id):
    """
    暂未被使用
    :param port_id:
    :return:
    """
    subcard_number, port_number = port_id.split('/')
    return {
        'subcard_number': int(subcard_number),
        'port_number': int(port_number)
    }
