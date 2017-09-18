import logging

logging.basicConfig(format='%(asctime)s %(filename)-10s %(message)s')
logger = logging.getLogger('actions')
logger.setLevel(logging.DEBUG)


class ModelGroup:
    def __init__(self, *args):
        self.group = list(args)

    def __str__(self):
        return f'{type(self).__name__}<{", ".join(map(str, self.group))}>'


def link(model_a, model_b, protocol):
    logger.info(f'linking {model_a} and {model_b} with {protocol}')
    pass


def group(*models):
    return ModelGroup(*models)
