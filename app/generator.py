import logging

from uniform_model.devices.link import Link
from uniform_model.devices.link_manager import LinkManager

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('app.configure_process')
logger.setLevel(logging.DEBUG)


class ConfigurationGenerator:
    """
    用于生成配置及拓扑信息
    """
    def __init__(self):
        pass

    def _check_circle(self, functions_list, device):
        in_degrees = []
        for func in functions_list:
            in_degrees.append(len(getattr(device, func).dependencies))
        if 0 in in_degrees:
            return False
        else:
            return True

    def generate_conf(self, devices):
        logger.info('generate conf file')
        output = {}  # 存放全部设备的配置信息
        for device in devices:
            logger.info(f'generate conf file of device {device.id}')
            loc_output = []  # 存放单个设备的配置信息
            functions_list = device.functions
            if functions_list is not None:
                logger.info(f'generate conf file of {functions_list} in device {device.id}')
                for item in functions_list:
                    if item.tag:
                        logger.info(f'revoke function {item}')
                    test = item.generate_revoke_conf() if item.tag else item.generate_conf()
                    loc_output.append(test)
            output.update({device.name: loc_output})
        logger.info('generate conf file end')
        return output

    def genarate_topo(self, devices):
        logger.info('generate topo json')
        json = {"devices": [], "connections": []}
        for device in devices:
            logger.info(f'generate topo json of {device.id}')
            loc_json = json['devices']
            if device.parent_id:
                logger.info(f'find parent {device.parent_id} of {device.id}')
                loc_json = self._find_node_in_json(device.parent_id, json['devices'])
            loc_json.append({
                "id": device.id,
                "type": device.model.category,
                "attrs": device.to_json(),
            })
        for link in LinkManager.get_registed_links():
            json["connections"].append({
                "from": link.device_id_a,
                "to": link.device_id_b,
                "link_type": link.link_type,
                "attrs": link.to_json()
            })
        logger.info('generate topo json end')
        return json

    def _find_node_in_json(self, node_id, json):
        for item in json:
            if item["id"] == node_id:
                if item.get("subs", None) is None:
                    item.update({"subs": []})
                return item["subs"]
            elif item.get("subs", None) is not None:
                return self._find_node_in_json(node_id, item['subs'])
        return None

    def exist(self, link: Link, json_array):
        for item in json_array:
            check_item = (item['source'], item['target'])
            if link.device_id_a in check_item and link.device_id_b in check_item:
                return True
            else:
                return False
