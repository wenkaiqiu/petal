import logging

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('uniform_model.devices.device')
logger.setLevel(logging.DEBUG)


class Device:
    """
    Device（设备实例的类型）。设备实例对应一个实际的物理单元（同时对应设备数据库的一条记录）。
    程序中所有设备实例都是Device类型，由Template生成。不同Template会对初始设备实例进行加工，注入对应Template所应有的属性和方法。
    如一个CX310设备实例由SwitchTemplate注入Switch共有的属性和方法方法，故不再设子类，由model属性区分设备类型。
    从属性上来说，device含有设备数据库中的model，device，wire，part，space和status的所有信息。
    """
    def __init__(self, *args, **kwargs):
        self.id = kwargs["id"]
        self.uuid = kwargs["uuid"]
        self.name = kwargs["name"]
        self.model_type = kwargs["model_type"]
        self.parent_id = kwargs["parent_id"]
        self.links = {}

    def link(self, link_to, link_info):
        link = {
            "name": link_info["name"],
            "id": link_info["id"],
            "to_id": link_to.id,
            "to": link_to,
            "link_type": link_info["link_type"],
            "usage": link_info["usage"] if "usage" in link_info.keys() else ""
        }
        self.links.update({link['to_id']: link})

    def get_attrs_json(self):
        json = {}
        # 添加基础属性
        json.update({
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "model_type": self.model_type
        })
        # 添加接口属性
        interfaces = getattr(self, "interfaces", None)
        if interfaces:
            json.update({"interfaces": []})
            for interface in interfaces.values():
                json["interfaces"].append(interface.name)
        return json
