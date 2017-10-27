import queue


class OperationValidator:
    def validate(self, operations: list):
        while operations:
            operation = operations.pop(0)
            if not operation:
                operations.append(operation)
