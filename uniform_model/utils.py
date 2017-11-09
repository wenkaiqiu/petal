def check_necessary(info, necessary_dict):
    return all(key in info for key in necessary_dict if necessary_dict[key])


def fill_value(entities, info, dict):
    for key in dict:
        if key in info:
            entities[key] = info[key]


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
