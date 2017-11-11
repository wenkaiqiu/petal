import logging

from uniform_model.devices.link import Link
from uniform_model.utils import check_necessary, fill_value

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.device')
logger.setLevel(logging.DEBUG)


class Device:
    """
    Device（设备实例的类型）。设备实例对应一个实际的物理单元（同时对应设备数据库的一条记录）。
    程序中所有设备实例都是Device类型，由Template生成。不同Template会对初始设备实例进行加工，注入对应Template所应有的属性和方法。
    如一个CX310设备实例由SwitchTemplate注入Switch共有的属性和方法方法，故不再设子类，由model_type的category属性区分设备类型。
    从属性上来说，device含有设备数据库中的model，device，wire，part，space和status的所有信息。
    """
    # vals定义约束的共有属性。key表示属性名，value表示是否必须
    vals = {
        'id': True,
        'uuid': True,
        'name': True,
        'model_type': True,
        'asset_id': False,
        'data_center': False,
        'description': False
    }
    # 内部规则，若需要对值类型检查，可在此添加规则
    inner_rules = tuple()

    def __init__(self, *args, **kwargs):
        """
        初始化方法，进行共有属性的属性检查。
        :param args:
        :param kwargs:
        """
        logger.info('<Device> init Device object')
        self._entities = dict()  # 用于保存基本属性
        self.model = None
        self.space = None
        self.status = None
        self.parent_id = None
        self.children_id = []
        self.links = []  # 为实现检查，故需实现接口
        self.functions = []

        # 1.val check
        if not check_necessary(kwargs, self.vals):
            raise Exception(f'lack necessary attribute of {type(self)}')
        # 2.fill vals
        fill_value(self._entities, kwargs, self.vals)
        # check inner rules
        if not (self._inner_check()): raise Exception('内部检查失败')

    def _inner_check(self):
        logger.info('<Device> inner check')
        # inner check
        return all(rule.apply(self, None) for rule in self.inner_rules)

    def get_entities(self):
        return self._entities

    def to_database(self):
        device_info = {'properties': {}}
        self._entities['model_type'] = self.model.model_type

        for item in self._entities:
            if item in self.vals:
                device_info.update({item: self._entities[item]})
            else:
                device_info['properties'].update({item: self._entities[item]})
        json = {
            'device': device_info,
        }
        if self.space: json.update({'space': self.space.to_database() if self.space else None})
        if self.parent_id: json.update({'part': {'parent_id': self.parent_id if self.parent_id else None}})

        return json

    def to_json(self):
        json = {}
        # 添加基础属性
        json.update({
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'model_type': self.model_type
        })
        # 添加接口属性
        interfaces = getattr(self, 'interfaces', None)
        if interfaces:
            json.update({'interfaces': []})
            for interface in interfaces.values():
                json['interfaces'].append(interface.name)
        return json

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError:
            return self._entities.get(name)
