import json
import logging
import os

from db.base import Database

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('db.json')
logger.setLevel(logging.DEBUG)

project_path = os.path.join(os.getcwd().split("petal")[0], "petal")


# print(project_path)


class JSON(Database):
    """
    用于访问JSON文件的数据库类，实现抽象父类Database定义的接口
    """
    # 目前仅用于mock，故固定文件路径，而不是从conf文件读取
    json_path = {
        'model': project_path + '\\contrib\\mock\\model.json',
        'device': project_path + '\\contrib\\mock\\device.json',
        'configuration': project_path + '\\contrib\\mock\\configuration.json',
        'part': project_path + '\\contrib\\mock\\part.json',
        'space': project_path + '\\contrib\\mock\\space.json',
        'wire': project_path + '\\contrib\\mock\\wire.json',
        'status': project_path + '\\contrib\\mock\\status.json',
        'manager': project_path + '\\contrib\\mock\\manager.json'
    }

    @classmethod
    def set_conf(cls, conf):
        # 对JSON类无用，故仅打印
        logger.info("<JSON> set_conf")

    @classmethod
    def get_device_all_info(cls, device_id):
        # 补全信息
        device_info = cls.get_device_info(device_id)
        if 'properties' in device_info:
            properties = device_info.pop('properties')
            device_info.update(properties)
        model_info = cls.get_model(device_info['model_type']) if device_info['model_type'] else None
        device_info.update({'model': model_info})
        device_info.update({'status': cls.get_status(device_id)})
        part_info = cls.get_parent(device_id)
        device_info.update({'parent_id': part_info['parent_id'] if part_info else None})
        device_info.update({'space': cls.get_space(device_id)})
        device_info.update({'manager': cls.get_manager(device_id)})
        device_info.update({'functions': cls.get_device_configurations(device_id)})

        # 定制修改
        device_info.update({'model_type': model_info['category'] if model_info else 'other'})
        return device_info

    @classmethod
    def update_device_all_info(cls, device_id, params):
        logger.info(f' update device all info: {params}')
        cls.update_device_info(device_id, params['device'])
        if 'part' in params:
            if cls.get_parent(device_id):
                cls.update_parent(device_id, params['part'])
            else:
                cls.add_parent(device_id, params['part']['parent_id'])
        if 'space' in params:
            if 'id' in params['space']:
                cls.update_space(params['space']['id'], params['space'])
            else:
                cls.add_space(device_id, params['space'])

    @classmethod
    def get_device_info(cls, device_id):
        with open(cls.json_path["device"]) as device_json:
            devices = json.load(device_json)
        device_info = list(filter(lambda x: x['id'] == device_id, devices))
        device_info = device_info[0] if device_info else None
        logger.info(f"get device_info of {device_id}: {device_info}")
        return device_info

    @classmethod
    def update_device_info(cls, device_id, params):
        logger.info(f'update device_info of <{device_id}> with params: {params}')
        with open(cls.json_path["device"], 'r') as device_json:
            devices = json.load(device_json)
        with open(cls.json_path['device'], 'w') as device_json:
            item = cls.find_in_list(devices, lambda x: x['id'] == device_id)
            if item:
                item.update(params)
            json.dump(devices, device_json)

    @classmethod
    def get_model(cls, model_type):
        with open(cls.json_path["model"]) as model_json:
            models = json.load(model_json)
        model_info = list(filter(lambda x: x['model_type'] == model_type, models))
        model_info = model_info[0] if model_info else None
        logger.info(f"get model_info of {model_type}: {model_info}")
        return model_info

    @classmethod
    def get_links(cls):
        with open(cls.json_path["wire"]) as link_json:
            links = json.load(link_json)
            links = links
        logger.info(f"get links_info of: {links}")
        return links

    @classmethod
    def add_link(cls, params):
        logger.info(f'add link with params: {params}')
        with open(cls.json_path["wire"], 'r') as link_json:
            links = json.load(link_json)
        with open(cls.json_path["wire"], 'w') as link_json:
            conf_id = int(links[-1]['id']) if links else 0
            params.update({'id': str(conf_id + 1)})
            links.append(params)
            json.dump(links, link_json)

    @classmethod
    def update_link(cls, link_id, params):
        logger.info(f'update link of link_id <{link_id}> with params: {params}')
        with open(cls.json_path["wire"], 'r') as link_json:
            links = json.load(link_json)
        with open(cls.json_path['wire'], 'w') as link_json:
            item = cls.find_in_list(links, lambda x: x['id'] == link_id)
            if item:
                item.update(params)
            json.dump(links, link_json)

    @classmethod
    def get_status(cls, device_id):
        with open(cls.json_path["status"]) as status_json:
            status = json.load(status_json)
        status_info = list(filter(lambda x: x['device_id'] == device_id, status))
        status_info = status_info if status_info else None
        logger.info(f"get status_info of {device_id}: {status_info}")
        # 转成程序所需格式
        converted_status = {}
        if status_info is not None:
            for item in status_info:
                converted_status.update({item['status_type'].lower(): item['status_value']})
        return converted_status

    @classmethod
    def get_space(cls, device_id):
        part_info = cls.get_parent(device_id)
        space_id = part_info['space_id'] if part_info else None
        if not space_id:
            return None
        with open(cls.json_path["space"]) as space_json:
            spaces = json.load(space_json)
        space_info = list(filter(lambda x: x['id'] == space_id, spaces))
        space_info = space_info[0] if space_info else None
        logger.info(f"get space_info of {device_id}: {space_info}")
        return space_info

    @classmethod
    def add_space(cls, device_id, params):
        logger.info(f'add space of {device_id} with space_info: {params}')
        # 先添加space记录
        with open(cls.json_path['space'], 'r') as space_json:
            spaces = json.load(space_json)
        with open(cls.json_path['space'], 'w') as space_json:
            space_id = int(spaces[-1]['id']) if spaces else 0
            params.update({'id': str(space_id + 1)})
            spaces.append(params)
            json.dump(spaces, space_json)
        # 再处理part中的space_id
        if cls.get_parent(device_id):
            cls.update_parent(device_id, {'space_id': params['id']})
        else:
            cls.add_parent(device_id, '')
        return space_id

    @classmethod
    def update_space(cls, space_id, params):
        logger.info(f'update space_info of space_id <{space_id}> with params: {params}')
        with open(cls.json_path["space"], 'r') as space_json:
            spaces = json.load(space_json)
        with open(cls.json_path['space'], 'w') as space_json:
            item = cls.find_in_list(spaces, lambda x: x['id'] == space_id)
            if item:
                item.update(params)
            json.dump(spaces, space_json)

    @classmethod
    def get_parent(cls, device_id):
        with open(cls.json_path["part"]) as part_json:
            parts = json.load(part_json)
        part_info = list(filter(lambda x: x['device_id'] == device_id, parts))
        part_info = part_info[0] if part_info else None
        logger.info(f"get part_info of {device_id}: {part_info}")
        return part_info

    @classmethod
    def add_parent(cls, device_id, parent_id):
        logger.info(f'add parent of {device_id} with parent_id: {parent_id}')
        with open(cls.json_path["part"], 'r') as part_json:
            parts = json.load(part_json)
        with open(cls.json_path["part"], 'w') as part_json:
            parts.append({
                'device_id': device_id,
                'parent_id': parent_id,
                'space_id': ''
            })
            json.dump(parts, part_json)

    @classmethod
    def update_parent(cls, device_id, params):
        logger.info(f'update parent of <{device_id}> with params: {params}')
        with open(cls.json_path["part"], 'r') as part_json:
            parts = json.load(part_json)
        with open(cls.json_path['part'], 'w') as part_json:
            item = cls.find_in_list(parts, lambda x: x['device_id'] == device_id)
            if item:
                item.update(params)
            json.dump(parts, part_json)

    @classmethod
    def get_manager(cls, device_id):
        with open(cls.json_path["manager"]) as manager_json:
            managers = json.load(manager_json)
        manager = list(filter(lambda x: x['device_id'] == device_id, managers))
        logger.info(f"get manager_info of {device_id}: {manager}")
        return manager

    @classmethod
    def get_device_configurations(cls, device_id):
        with open(cls.json_path["configuration"]) as configuration_json:
            configurations = json.load(configuration_json)
        device_configurations = list(filter(lambda x: x['device_id'] == device_id, configurations))
        logger.info(f"get configurations of {device_id}: {device_configurations}")
        return device_configurations

    @classmethod
    def add_configuration(cls, params):
        logger.info(f'add configuration with params: {params}')
        with open(cls.json_path["configuration"], 'r') as configuration_json:
            configurations = json.load(configuration_json)
        with open(cls.json_path["configuration"], 'w') as configuration_json:
            conf_id = int(configurations[-1]['id']) if configurations else 0
            params.update({'id': str(conf_id + 1)})
            configurations.append(params)
            json.dump(configurations, configuration_json)

    @classmethod
    def update_configuration(cls, conf_id, params):
        logger.info(f'update configuration of conf_id <{conf_id}> with params: {params}')
        with open(cls.json_path["configuration"], 'r') as configuration_json:
            configurations = json.load(configuration_json)
        with open(cls.json_path['configuration'], 'w') as configuration_json:
            item = cls.find_in_list(configurations, lambda x: x['id'] == conf_id)
            if item:
                item.update(params)
            json.dump(configurations, configuration_json)

    @staticmethod
    def find_in_list(array, func):
        for item in array:
            if func(item):
                return item
        else:
            return None
