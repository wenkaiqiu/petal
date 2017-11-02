import abc


class Database(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def set_conf(cls, conf): raise NotImplementedError

    @abc.abstractclassmethod
    def get_models(cls): raise NotImplementedError

    @abc.abstractclassmethod
    def get_all_device_detail(cls): raise NotImplementedError

    @abc.abstractclassmethod
    def get_device_detail(cls, device_id): raise NotImplementedError

    # todo:添加其他需要的接口
