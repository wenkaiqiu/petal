import logging

from uniform_model.devices.space import Space
from uniform_model.devices.status import Status
from uniform_model.utils import check_necessary, fill_value

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.devices.templates.base')
logger.setLevel(logging.DEBUG)


class TemplateType(type):
    def __str__(cls):
        return f'<Template: {cls.__name__}>'

    def __repr__(cls):
        return f'<Template: {cls.__name__}>'


class Template(metaclass=TemplateType):
    """
    模板类的基类，定义了模板生成设备实例时的流程
    """
    name = str()
    device_vals = dict()
    model_vals = dict()
    status_vals = dict()
    inner_rules = tuple()

    @classmethod
    def generate(cls, info):
        # 生成存放属性的属性类实例
        device = cls.generate_device(info['device'])
        model = cls.generate_device(info['model'])
        status = cls.generate_device(info['status']) if 'status' in info else None
        space = cls.generate_device(info['space']) if 'space' in info else None
        # 赋值，由device统一管理信息
        device.model = model
        device.status = status
        device.space = space
        device.parent_id = info['parent_id'] if 'parent_id' in info else None
        device.children_id = info['children_id'] if 'parent_id' in info else []
        # inner check
        if not (cls._inner_check()):
            raise Exception('内部检查失败')
        return device

    @classmethod
    def _inner_check(cls):
        # inner check
        return all(rule.apply(cls, None) for rule in cls.inner_rules)

    @classmethod
    def generate_device(cls, device_info):
        device = Status(**device_info)
        # 1.val check
        if not check_necessary(device_info, cls.device_vals):
            raise Exception(f'lack necessary attribute of model in {type(cls)}')
        # 2.fill vals
        fill_value(device.get_entities(), device_info, cls.device_vals)

    @classmethod
    def generate_model(cls, model_info):
        model = Status(**model_info)
        # 1.val check
        if not check_necessary(model_info, cls.model_vals):
            raise Exception(f'lack necessary attribute of model in {type(cls)}')
        # 2.fill vals
        fill_value(model.get_entities(), model_info, cls.model_vals)

    @classmethod
    def generate_status(cls, status_info):
        status = Status(**status_info)
        # 1.val check
        if not check_necessary(status_info, cls.status_vals):
            raise Exception(f'lack necessary attribute of status in {type(self)}')
        # 2.fill vals
        fill_value(status.get_entities(), status_info, cls.status_vals)

    @classmethod
    def generate_space(cls, space_info):
        return Space(**space_info)

    def __getattr__(self, name):
        try: return self.__dict__[name]
        except KeyError: return self._entities.get(name)
