class Model:
    """
    与数据库中的model表对应
    """
    def __init__(self, *args, **kwargs):
        self.model_type = kwargs["modelType"]