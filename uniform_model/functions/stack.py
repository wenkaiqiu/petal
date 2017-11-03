import logging

from .utils import render
from uniform_model.functions.base import FunctionNew
from uniform_model.base import Statement, When, Need, Entity

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('uniform_model.functions.stack_new')
logger.setLevel(logging.DEBUG)


class FunctionStack(FunctionNew):
    name = "stack"
    vals = {'domain_id': True, 'member_id': True, 'priority': True, 'stack_port': True}
    # todo: 可不可以检查dict？还是只能写对象？
    entities = {
        'device': Entity('device', ('interface', 'slot_id'), ()),
    }
    inner_rules = (
        Need('a.priority in range(0, 255)'),
    )
    intra_rules = (
        When('type(a) is type(b)',
             When('a.domain_id == b.domain_id',
                  Need('a.port_id != b.port_id'),
                  Statement(True)),
             Statement(True)),

        When('type(a) is type(b)',
             When('a.domain_id == b.domain_id',
                  Need('a.priority != b.priority'),
                  Statement(True)),
             Statement(True)),
    )

    def _infer_value(self, **kwargs):
        # 俩个作用，一是默认值设置，二是推断缺失属性
        new_kwargs=kwargs
        for key in filter(lambda x: x not in new_kwargs, self.vals):
            if key == 'member_id':
                new_kwargs.update({'member_id': kwargs['device'].slot_id[0]})
            elif key == 'priority':
                new_kwargs.update({'priority': 100})
        return new_kwargs

    def __init__(self, *args, **kwargs):
        new_kwargs = self._infer_value(**kwargs)
        super(FunctionStack, self).__init__(*args, **new_kwargs)
        # 参数填写的通用方法已在父类init方法中实现,此处填写特别配置即可
        # self._entities['this']['member_id'] = kwargs['device'].slot_id[0]


def main():
    class A: pass

    a = A()
    a.slot_id = '32'
    a.interface = '32'
    function_stack = FunctionStack(device=a, domain_id=12, priority=123, stack_port={'port_id':'32', 'physical_port':'32'})
    print(function_stack._entities)
    conf = function_stack.generate_conf()
    print(conf)
    print(function_stack.generate_revoke_conf())
    b = A()
    b.slot_id = '33'
    b.interface = '33'
    function_stack_b = FunctionStack(device=b, domain_id=12, priority=123, port_id=32, physical_port=32)
    function_stack.intra_check(function_stack_b)


if __name__ == '__main__':
    main()
