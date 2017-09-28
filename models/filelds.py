class Field:
    def _validate(self, value):
        """
        自定义数据类型检查流程，在赋值时自动调用
        :return: 检查通过返回真，否则 raise对应错误(推荐) 或者 返回False
        """
        return True

    def _get_default_value(self):
        pass


class CharField(Field):
    def _get_default_value(self):
        return ""

    # todo: 重写_validate

    def __init__(self):
        self.value = self._get_default_value()

    def set_value(self, value):
        if self._validate(value):
            self.value = value
        else:
            raise ValueError()

    def get_value(self):
        return self.value


class IPField(Field):
    def _get_default_value(self):
        return "0.0.0.0"

    def __init__(self):
        self.value = self._get_default_value()

    # todo: 重写_validate

    def set_value(self, value):
        if self._validate(value):
            self.value = value
        else:
            raise ValueError()

    def get_value(self):
        return self.value