import logging

from uniform_model.utils import check_necessary, fill_value

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.model')
logger.setLevel(logging.DEBUG)


class Model:
    """
    与数据库中的model表对应
    """
    vals = {
        'model_type': False,
        'name': False,
        'category': True,
        'vendor': False,
        'description': False,
    }
    inner_rules = tuple()

    def __init__(self, **kwargs):
        logger.info(f'<Model> init Model object {kwargs}')
        self._entities = dict()
        # 1.val check
        if not check_necessary(kwargs, self.vals):
            raise Exception(f'lack necessary attribute of {type(self)}')
        # 2.fill vals
        fill_value(self._entities, kwargs, self.vals)
        # 3.inner check
        if not (self._inner_check()): raise Exception('内部检查失败')

    def _inner_check(self):
        logger.info('<Model> inner check')
        # inner check
        return all(rule.apply(self, None) for rule in self.inner_rules)

    def get_entities(self):
        return self._entities

    def __getattr__(self, name):
        try: return self.__dict__[name]
        except KeyError: return self._entities.get(name)