class Link:
    def __init__(self, **kwargs):
        self.link_type = kwargs['link_type']
        self.link_name = kwargs['link_name']
        self.device_id_a = kwargs['device_id_a']
        self.device_id_b = kwargs['device_id_b']
        self.port_a = kwargs['port_a']
        self.port_b = kwargs['port_b']
        self.protocol = kwargs['protocol']
        self.pro_version = kwargs['pro_version']
        self.width = kwargs['width']
        self.usage = kwargs['usage']