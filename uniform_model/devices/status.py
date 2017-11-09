import logging

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.status')
logger.setLevel(logging.DEBUG)


class Status:
    """
    与数据库中的status表对应
    """
    vals = {
        'State': True,
        'Health': True
    }
    inner_rules = tuple()

    def __init__(self, **kwargs):
        logger.info('<Status> init Status object')
        self._entities = dict(this=dict())
        # 1.val check
        if not all(val in kwargs for val in self.vals if self.vals[val]):
            raise Exception( 'lack necessary attribute of Status')
        # 2.fill vals
        for key in self.vals: self._entities[key] = kwargs[key]
        # 3.inner check
        if not (self._inner_check()): raise Exception('内部检查失败')

    def _inner_check(self):
        logger.info('<Status> inner check')
        # inner check
        return all(rule.apply(self, None) for rule in self.inner_rules)

    def __getattr__(self, name):
        try: return self.__dict__[name]
        except KeyError: return self._entities.get(name)
