from models.actions import op
from . import rules as model
from models import protocols


def model_generator(model_dict):
    type = model_dict.pop('type')
    obj = getattr(model, type)(**model_dict)
    return {obj.logical_id: obj}


def operation_generator(operation_dict):
    type = operation_dict.get('type')
    return lambda: op(getattr(protocols, type), *operation_dict.get('device'), params=operation_dict.get('params'))


def output_generator(device):
    return {}