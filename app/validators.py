import queue


class OperationValidator:
    def validate(self, operations: list):
        while operations:
            # print("------OperationValidator------")
            # print(operations)
            operation = operations.pop(0)
            result = operation()
            # print("------OperationValidator------")
            # print(result)
            if not result:
                operations.append(operation)
