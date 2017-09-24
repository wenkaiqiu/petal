import logging

from models.base import ModelGroup
from models.protocols import ProtocolType

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('actions')
logger.setLevel(logging.DEBUG)


def link(model_a, model_b, protocol):
    logger.info(f'linking {model_a} and {model_b} with {protocol}')
    pass


def op(protocol: ProtocolType, *arith_list):
    logger.info(f'operate {protocol} on {arith_list}')


def group(*models):
    return ModelGroup(*models)
