import logging

from uniform_model.devices.link import Link

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
    vals = {'id': True, 'uuid': True, 'name': True, 'model_type': True}
    # 内部规则，若需要对值类型检查，可在此添加规则
    inner_rules = tuple()

    def __init__(self, *args, **kwargs):
        """
        初始化方法，进行共有属性的属性检查。
        :param args:
        :param kwargs:
        """
        self._entities = dict(this=dict())  # 用于保存基本属性
        self.model = None
        self.space = None
        self.status = dict()
        self.links = []
        self.functions = []

        # val check
        if not all(val in kwargs for val in self.vals if self.vals[val]): raise KeyError(
            'lack necessary attribute of device')

        # fill vals
        for key in self.vals: self._entities['this'][key] = kwargs[key]
        if not (self._inner_check()): raise Exception('内部检查失败')

    def _inner_check(self):
        # inner check
        return all(rule.apply(self, None) for rule in self.inner_rules)

    def _check_link(self, link):
        """
        检查连接是否重复或冲突
        :param link:
        :return:
        """
    def add_link(self, link: Link):
        """
        添加链接
        :param link: Link类型对象
        :return:
        """
        self.links.append(link)

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
            return self._entities['this'].get(name)
