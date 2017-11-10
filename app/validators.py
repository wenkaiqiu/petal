import logging

logging.basicConfig(format='%(asctime)s <%(name)s> [%(levelname)s]: %(message)s')
logger = logging.getLogger('uniform_model.actions.validators')
logger.setLevel(logging.DEBUG)


class OperationValidator:
    @staticmethod
    def validate(operations: list):
        # todo: 完善处理规则
        logger.info('start validator')
        while operations:
            operation = operations.pop(0)
            result = operation()
            if not result:
                operations.append(operation)
        logger.info('end validator')
