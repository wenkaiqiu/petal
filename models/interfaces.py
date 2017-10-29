import logging

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('interfaces')
logger.setLevel(logging.DEBUG)


class InterfaceType(type):
    def __str__(cls): return f'<Interface: {cls.__name__}>'

    def __repr__(cls): return f'<Interface: {cls.__name__}>'


class Interface(metaclass=InterfaceType):
    def __repr__(self):
        return f'{self.name.replace("GE", "GE ")}'

    def __init__(self, *args, **kwargs):
        # logger.info(f"init {self.__class__}")
        # logger.info(f"interface info: <{kwargs}>")
        self.count = kwargs['count']
        self.type = kwargs['type']
        self.interface_type = kwargs['interface_type']
        self.speed = kwargs['speed']
        self.subcard_number = kwargs['subcard_number']
        self.port_number = kwargs['port_number']
        self.slot_id = kwargs['slot_id']
        self.name = kwargs["name"]+ self.slot_id + "/" + str(self.subcard_number) + "/" + str(self.port_number)  # 10GE1/0/47
        self.attrs = {}

    def set_attr(self, attr_name, value):
        if attr_name not in self.attrs:
            self.attrs.update({attr_name: value})
        else:
            self.attrs[attr_name] = value


class PhysicalInterface(Interface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class EternetInterface(PhysicalInterface):
    pass


class FCInterface(PhysicalInterface):
    pass


class FunctionInterface(Interface):
    pass


class InterfaceManager:
    # 注册已有接口模型
    __global_register = {
        "Ethernet": EternetInterface,
        "FC": FCInterface
    }

    @classmethod
    def _check_interface_info(cls, interface_info):
        lack = []
        for item in cls.conf:
            if item not in interface_info:
                lack.append(item)
        return lack

    @classmethod
    def _get_interface_type(cls, type):
        return cls.__global_register.get(type, None)

    @classmethod
    def set_conf(cls, conf):
        cls.conf = list(filter(lambda x: conf[x], conf))
        logger.info("<InterfaceManager> set_conf")

    @classmethod
    def register_interface_to_device(cls, interface_info, device):
        lack = cls._check_interface_info(interface_info)
        if lack:
            raise AttributeError(f"<register_interface_to_device> lack attr {lack} in interface_info")
        # init device
        if not hasattr(device, "interfaces"):
            setattr(device, "interfaces", {})
        device_interfaces = getattr(device, "interfaces")
        logger.info(f"register {interface_info['type']} interface to {type(device)}")
        interface_info.update({"slot_id": device.slot_id[0]})
        interfaces = cls.generate_interface(interface_info)
        for interface in interfaces:
            device_interfaces.update({interface.name: interface})
        # for item in device_interfaces:
        #     print({item: device_interfaces[item].__dict__})

    @classmethod
    def generate_interface(cls, interface_info):
        i_type = interface_info["type"]
        model = cls._get_interface_type(i_type)
        # FC端口（MX）无子板号
        # len_subcard = len(interface_info["subcard_number"])
        # len_port = len(interface_info["port_number"])
        # if interface_info["count"] != len_port*len_subcard:
        #     raise ValueError("Error value in interface_info[\"count\"]")

        interfaces = []
        new_info = interface_info.copy()
        for i in interface_info["subcard_number"]:
            for j in interface_info["port_number"]:
                new_info.update({"subcard_number": i, "port_number": j})
                interfaces.append(model(**new_info))
        return interfaces

    @classmethod
    def list_all_registered_in_device(cls, device):
        return device.interfaces

    @classmethod
    def get_interface_in_device(cls, interface_name, device):
        interface = filter(lambda x: x.name == interface_name, device.interfaces)
        return interface.__next__
