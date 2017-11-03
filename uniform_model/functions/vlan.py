import logging

from uniform_model.functions.base_old import Function
from uniform_model.functions.base import FunctionNew
from uniform_model.base import Statement, When, Need, Entity

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('uniform_model.functions.vlan')
logger.setLevel(logging.DEBUG)


class FunctionVLAN(FunctionNew):
    name = "vlan"
    vals = {"vlan_id": True, "port_id": True}

    # entities用于推导参数
    entities = {
        'entity': Entity('device', ('interface',), ()),
    }
    inner_rules = (
        Need('a.vlan_id in range(1, 4094)'),
    )
    intra_rules = (
        # When('type(a) is type(b)',
        #      When('a.domain_id == b.domain_id',
        #           Need('a.port_id != b.port_id'),
        #           Statement(True)),
        #      Statement(True)),
    )

    def _infer_value(self, **kwargs):
        new_kwargs=kwargs
        for key in filter(lambda x: x not in new_kwargs, self.vals):
            if key == 'member_id':
                new_kwargs.update({'member_id': kwargs['device'].slot_id[0]})
        return new_kwargs

    def __init__(self, *args, **kwargs):
        new_kwargs = self._infer_value(**kwargs)
        super(FunctionVLAN, self).__init__(*args, **new_kwargs)
