import logging
from itertools import product

from models.base import ModelGroup, OperableTrait

logging.basicConfig(format='%(asctime)s <%(name)s> %(message)s')
logger = logging.getLogger('actions')
logger.setLevel(logging.DEBUG)


def link(model_a, model_b, protocol):
    logger.info(f'linking {model_a} and {model_b} with {protocol}')


def op(protocol: OperableTrait, *arith_list) -> None:
    lst = [arith.group if isinstance(arith, ModelGroup) else [arith] for arith in arith_list]
    for p in product(*lst): logger.info(f'operate {protocol} on {p}')


def group(*models):
    return ModelGroup(*models)
