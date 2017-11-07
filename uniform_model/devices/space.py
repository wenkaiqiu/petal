class Space:
    """
    与数据库中的space表对应
    """
    def __init__(self, *args, **kwargs):
        self.space_type = kwargs["space_type"]
        self.name = kwargs["name"]
        self.direction = kwargs["direction"]
        self.serial = kwargs["serial"]
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.z = kwargs["z"]
        self.data_center = kwargs["data_center"]