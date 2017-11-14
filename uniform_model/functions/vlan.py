import logging

from uniform_model.functions.base import Function
from uniform_model.base import Statement, When, Need, Entity

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.functions.vlan')
logger.setLevel(logging.DEBUG)


class FunctionVLAN(Function):
    name = 'vlan'
    vals = {'vlan_id': True, 'vlan_type': True, 'ports': True}

    # entities用于推导参数
    entities = {
        'entity': Entity('device', ('interface',), ()),
    }
    inner_rules = (
        Need('int(a.vlan_id) in range(1, 4094)'),
    )
    intra_rules = ()

    def _infer_value(self, **kwargs):
        return kwargs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def main():
    class A: pass

    a = A()
    a.slot_id = '32'
    a.interface = '32'
    function_vlan = FunctionVLAN(device=a, vlan_id=2, vlan_type='interface', ports=[{'port_id': 1, 'link_type': 'access'}, {'port_id': 2, 'link_type': 'hybrid', 'priority': 1}])
    print(function_vlan._entities)
    print(function_vlan.generate_conf())
    print(function_vlan.generate_revoke_conf())


if __name__ == '__main__':
    main()
