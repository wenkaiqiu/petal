def parse_interface_id(port_id):
    subcard_number, port_number = port_id.split('/')
    return {
        'subcard_number': int(subcard_number),
        'port_number': int(port_number)
    }
