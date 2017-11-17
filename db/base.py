import abc


class Database(metaclass=abc.ABCMeta):
    """
    数据库类的抽象基类，用于定义所有数据库类应有的接口
    信息类型及操作如下
    - device_info: get, update
    - model: get
    - link: add, get, update
    - space: get, set
    - part: get, add, update
    - configuration: get, add, update
    - status: get
    - manager: get
    - **device_all_info**: get, update
        - 必须有device_id
        - 包括device_info, model, link, space, part, status, configeration
    """

    @abc.abstractclassmethod
    def set_conf(cls, conf):
        """
        配置该类型访问数据库所需的信息，
        :param conf:配置参数
        :return:None
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_device_all_info(cls, device_id):
        """
        获取设备所有信息，包括基本信息，型号信息，连接信息，状态信息，位置信息，组成信息，管理者信息，配置信息
        :param device_id:
        :return:
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def update_device_all_info(cls, device_id, params):
        """
        更新设备所有信息，包括基本信息，连接信息，位置信息，组成信息，配置信息。
        目前，型号信息，状态信息，管理者信息在我们的设计中无更改能力和需求，故不进行更新。
        连接信息和配置信息单独更新。
        :param device_id: 设备ID
        :param params: 要更新的信息，包括基本信息，位置信息，组成信息
        :return: None
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_device_info(cls, device_id):
        """
        获取设备基本信息，详见返回值
        :param device_id: 设备id
        :return: dict('id', 'uuid', 'name', 'model_type', 'description', 'properties')
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def update_device_info(cls, device_id, params):
        """
        更新设备基本信息
        :param device_id: 设备id
        :param params: dict('id', 'uuid', 'name', 'model_type', 'description', 'properties')
        return None
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_model(cls, model_type):
        """
        获取型号信息
        :param model_type: 设备型号名
        :return: dict('model_type', 'name', 'catogery', 'vendor', 'description', 'properties')
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_links(cls):
        """
        用于配置初始化时，获取全部连接信息
        :return: dict('id', 'name', 'device_id_a', 'device_id_b', 'port_a', 'port_b', 'link_type', 'usage', 'bandwidth',
                        'unit', 'length')[]
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def add_link(cls, params):
        """
        添加设备的连接信息
        :param params: 要添加的连接信息
                        dict('id', 'name', 'device_id_a', 'device_id_b', 'port_a', 'port_b', 'link_type', 'usage',
                         'bandwidth', 'unit', 'length')
        :return: None
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def update_link(cls, link_id, params):
        """
        更新设备的连接信息
        :param link_id: 设备ID
        :param params: 要添加的连接信息
                        dict('id', 'name', 'device_id_a', 'device_id_b', 'port_a', 'port_b', 'link_type', 'usage',
                         'bandwidth', 'unit', 'length')
        :return: None
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_status(cls, device_id):
        """
        获取设备的状态信息
        :param device_id: 设备ID
        :return: array[tuple('id', 'status_type', 'status_value')]
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_space(cls, device_id):
        """
        获取设备的位置信息
        :param device_id: 设备ID
        :return: dict('space_type', 'name', 'direction', 'serial', 'x', 'y', 'z' 'data_center')
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def add_space(cls, device_id, params):
        """
        添加设备的位置信息
        :param device_id: 设备ID
        :param params: dict('space_type', 'name', 'direction', 'serial', 'x', 'y', 'z' 'data_center')
        :return: None
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def update_space(cls, space_id, params):
        """
        更新设备的位置信息
        :param space_id:
        :param params: dict('space_type', 'name', 'direction', 'serial', 'x', 'y', 'z' 'data_center')
        :return: None
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_parent(cls, device_id):
        """
        获取父设备ID
        :param device_id:
        :return: 父设备ID
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def add_parent(cls, device_id, parent_id):
        """
        获取父设备ID
        :param device_id: 设备ID
        :param parent_id: 父设备ID
        :return: None
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def update_parent(cls, device_id, parent_id):
        """
        更新父设备ID
        :param device_id: 设备ID
        :param parent_id: 父设备ID
        :return: None
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_manager(cls, device_id):
        """
        获取管理员用户ID
        :param device_id: 设备ID
        :return: user_id: 管理员用户ID
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_device_configurations(cls, device_id):
        """
        获取设备的所有配置
        :param device_id: 设备ID
        :return: dict('conf_id', 'device_id', 'type', 'params')[]
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def add_configuration(cls, params):
        """
        添加设备的所有配置
        :param params: dict('device_id', 'type', 'params')
        :return: None
        """
        raise NotImplementedError

    @abc.abstractclassmethod
    def update_configuration(cls, conf_id, parmas):
        """
        更新设备的所有配置
        :param conf_id: 配置ID
        :param parmas: dict('device_id', 'type', 'params')
        :return: None
        """
        raise NotImplementedError
