import logging

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.space')
logger.setLevel(logging.DEBUG)


class Space:
    """
    与数据库中的space表对应
    """
    vals = {
        'space_type': True,     # 空间类型
        'name': False,           # 空间名称
        'direction': False,      # 设备在此空间中的方位
        'serial': False,        # 槽位号等
        'x': False,              # 相对于父设备的x坐标
        'y': False,              # 相对于父设备的y坐标
        'z': False,              # 相对于父设备的z坐标
        'data_center': False,    # 数据中心
    }
    inner_rules = tuple()

    def __init__(self, **kwargs):
        logger.info('<Space> init Space object')
        self._entities = dict()
        # 1.val check
        if not all(val in kwargs for val in self.vals if self.vals[val]):
            raise Exception('lack necessary attribute of Space')
        # 2.fill vals
        for key in self.vals: self._entities[key] = kwargs[key]
        # 3.inner check
        if not (self._inner_check()): raise Exception('内部检查失败')

    def _inner_check(self):
        logger.info('<Space> inner check')
        # inner check
        return all(rule.apply(self, None) for rule in self.inner_rules)

    def __getattr__(self, name):
        try: return self.__dict__[name]
        except KeyError: return self._entities.get(name)
