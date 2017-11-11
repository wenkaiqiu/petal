import json
import os


def test():
    data = {
        "id": "20101",
        "uuid": "Port_10101",
        "name": "10GE",
        "model_type": "10GE",
        'asset_id': '123',
        'data_center': '123',
        "description": "",
        "type": "Ethernet",
        "interface_type": "internal",
        "speed": "10",
        "unit": "GE",
        "subcard_number": 1,
        "port_number": 1
    }
    convert(data)
    print(data)


def convert(data):
    dicts = ['id', 'uuid', 'name', 'model_type', 'asset_id', 'data_center', 'description', 'properties']
    properties = {}
    for k, v in data.items():
        if k not in dicts:
            properties.update({k: v})
    for k in properties:
        data.pop(k)
    if 'properties' not in data:
        data.update({'properties': properties})
    else:
        data['properties'].update(properties)
    print(data)


def main():
    project_path = os.path.join(os.getcwd().split("petal")[0], "petal")
    device_path = project_path+'\\contrib\\mock\\device.json'
    with open(device_path, 'r') as device_json:
        devices = json.load(device_json)
        for device in devices:
            convert(device)
    with open(device_path, 'w') as device_json:
        json.dump(devices, device_json)

if __name__ == '__main__':
    # test()
    main()
