import logging
from itertools import chain

from uniform_model.templates.other import OtherTemplate
from uniform_model.templates.processor import ProcessorTemplate
from uniform_model.templates.storage import StorageTemplate
from .chassis import ChassisTemplate
from .switch import SwitchTemplate

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('uniform_model.templates.template_manager')
logger.setLevel(logging.DEBUG)

# 注册已有设备模型
__global_register = {
    'chasis': ChassisTemplate,
    'switch': SwitchTemplate,
    'processor': ProcessorTemplate,
    'other': OtherTemplate,
    'storage': StorageTemplate
}


# 获取设备模型，若不存在，返回None
def _get_model_type(model_type):
    global __global_register
    return __global_register.get(model_type, None)


class TemplateManager:
    """
    负责Model的实例化，并管理已注册的模型实例
    """
    __registered_models = {}

    @classmethod
    def _check_info(cls, model_info):
        if "model_type" not in model_info:
            raise NameError("<model_type> is needed in model_info")
        model_type = model_info["model_type"]
        # for item in chain(cls.conf["base"], cls.conf[model_type]):
        #     if item not in model_info:
        #         raise NameError(f"<{item}> is needed in model_info")

    @classmethod
    def set_conf(cls, conf):
        logger.info("<ModelManager> set_conf")
        cls.conf = {"base": filter(lambda x: conf[x], conf)}
        for item in filter(lambda x: x.startswith("other"), conf):
            cls.conf.update({item.split("_")[1]: filter(lambda x: conf[item][x], conf[item])})

    @classmethod
    def register_model(cls, model_info):
        try:
            cls._check_info(model_info)
            logger.info(f"model <{model_info['name']}> checked success")
        except NameError as e:
            print(e)

        model_type = model_info["model_type"]
        model = _get_model_type(model_type)(**model_info)
        # 检查该类型Model是否重复注册
        if cls.get_model(model.name) is not None:
            raise ValueError(f'model <{model.name}> already registered.')
        cls.__registered_models.update({model.name: model})
        logger.info(f'register model <{model.name}> success')

    @classmethod
    def list_all_registered(cls):
        return cls.__registered_models

    @classmethod
    def get_model(cls, model_name):
        return cls.__registered_models.get(model_name, None)
