import logging
from itertools import product

from uniform_model import FunctionStack
from uniform_model.functions.base import FunctionNew
from uniform_model.base import Statement, When, Need, Entity

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.functions.trunk')
logger.setLevel(logging.DEBUG)


# todo: 暂时实现手工负载负担模式
class ConfictError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.conflict_function = kwargs["conflict_function"]


class FunctionTrunk(FunctionNew):
    name = "trunk"
    vals = {'number': False, 'mode': False, 'trunk_port': True}

    # entities用于推导参数
    entities = {
        'device': Entity('device', ('interface',), ()),
    }
    inner_rules = (
        Need('a.mode in ["manual"]'),  # 检查负载分担模式
        Need('a.func()'),  # 检查trunk-id取值范围
    )
    intra_rules = (
        When('type(b).name == "stack"',
             When('a.func2(b)',
                  Statement(False),
                  Statement(True)),
             Statement(True)),
    )

    # todo
    def func(self):
        return all(int(port["trunk_id"]) in range(0, int(self.number)) for port in self.trunk_port)

    def func2(self, b):
        print("---------------------------")
        print(all(
            not bool(set(a["physical_port"]).intersection(set(b["physical_port"])))
            for a,b in product(self.trunk_port, b.stack_port)))
        # return all(
        #     not bool(set(a["physical_port"]).intersection(set(b["physical_port"])))
        #     for a,b in product(self.trunk_port, b.stack_port))
        for x, y in product(self.trunk_port, b.stack_port):
            if bool(set(x["physical_port"]).intersection(set(y["physical_port"]))):
                raise ConfictError(**{'conflict_function': b})

    def _infer_value(self, **kwargs):
        new_kwargs = kwargs
        for key in filter(lambda x: x not in new_kwargs, self.vals):
            if key == 'member_id':
                new_kwargs.update({'member_id': kwargs['device'].slot_id[0]})
        return new_kwargs

    def __init__(self, *args, **kwargs):
        new_kwargs = self._infer_value(**kwargs)
        super(FunctionTrunk, self).__init__(*args, **new_kwargs)
        try:
            for func in new_kwargs["device"].functions_list:
                res = self.intra_check(func)
                print(res)
        except ConfictError as e:
            func = e.conflict_function
            print(func)
            func.tag = True
            print(func.tag)


def main():
    class A: pass

    a = A()
    a.slot_id = '32'
    a.interface = '32'
    function_trunk = FunctionTrunk(device=a, number=64, mode='manual',
                                   trunk_port={'trunk_id': '32', 'physical_port': '32'})
    print(function_trunk._entities)
    conf = function_trunk.generate_conf()
    print(conf)
    print(function_trunk.generate_revoke_conf())
    b = A()
    b.slot_id = '33'
    b.interface = '33'
    function_stack_b = FunctionStack(device=b, domain_id=12, priority=123,
                                     stack_port={'port_id': '32', 'physical_port': '32'})
    res = function_trunk.intra_check(function_stack_b)
    print(res)


if __name__ == '__main__':
    main()
