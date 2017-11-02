import logging

from uniform_model.functions.base import Function

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('uniform_model.functions.trunk')
logger.setLevel(logging.DEBUG)


class FunctionTrunk(Function):
    @classmethod
    def op(cls, arith_list):
        print(f'op on {arith_list}')