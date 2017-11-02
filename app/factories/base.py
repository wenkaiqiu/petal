import abc


class Factory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def generate(self, **kwargs): raise NotImplementedError
