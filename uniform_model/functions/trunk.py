import logging
from itertools import product

from uniform_model.functions.base import Function
from uniform_model.functions.exceptions import ConflictError
from uniform_model.base import Statement, When, Need, Entity

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.functions.trunk')
logger.setLevel(logging.DEBUG)


class FunctionTrunk(Function):
    name = 'trunk'
    vals = {'number': False, 'mode': False, 'trunk_port': True}

    # entities用于推导参数
    entities = {
        'device': Entity('device', ('interface',), ()),
    }
    inner_rules = (
        When('a.mode', Need('a.mode in ["manual"]'), Statement(True)),  # 检查负载分担模式
        Need('a._check_id_range()'),  # 检查trunk-id取值范围
    )
    intra_rules = (
        When('type(b).name == "stack"',
             When('a._check_conflict_function(b)',
                  Statement(False),
                  Statement(True)),
             Statement(True)),
    )

    def _check_id_range(self):
        return all(int(port['trunk_id']) in range(0, int(self.number)) for port in self.trunk_port)

    def _check_conflict_function(self, b):
        # 返回是协议配置端口否冲突。
        return all(
            bool(set(x['physical_port']).intersection(set(y['physical_port'])))
            for x, y in product(self.trunk_port, b.stack_port))

        # 为实现消除冲突，通过raise ConflictError来指示冲突对象
        # for x, y in product(self.trunk_port, b.stack_port):
        #     if bool(set(x['physical_port']).intersection(set(y['physical_port']))):
        #         raise ConflictError(**{'conflict_function': b})

    def _infer_value(self, **kwargs):
        if not self.number:
            self.number = 64
        return kwargs

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def main():
    class A: pass

    a = A()
    a.slot_id = '32'
    a.interface = '32'
    function_trunk = FunctionTrunk(device=a, number=64, mode='manual',
                                   trunk_port=[{'trunk_id': 32, 'physical_port': '32'}])
    print(function_trunk._entities)
    conf = function_trunk.generate_conf()
    print(conf)
    print(function_trunk.generate_revoke_conf())
    b = A()
    b.slot_id = '33'
    b.interface = '33'
    from uniform_model.functions.stack import FunctionStack
    function_stack_b = FunctionStack(device=b, domain_id=12, priority=123,
                                     stack_port=[{'port_id': 32, 'physical_port': '32'}])
    res = function_trunk.intra_check(function_stack_b)
    print(res)


if __name__ == '__main__':
    main()
