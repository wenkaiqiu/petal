import collections


class Field:
    def __init__(self, choices=None):
        if isinstance(choices, collections.Iterator):
            choices = list(choices)
        self.choices = choices or []

    def check(self, value):
        """
        自定义数据类型检查流程，在赋值时自动调用
        :return: 检查通过返回真，否则 raise对应错误(推荐) 或者 返回False
        """
        errors = []
        errors.extend(self._check_choices())
        return errors

    def _check_choices(self):
        if self.choices:
            # todo: 类型检查和值格式检查，参考
            # if (isinstance(self.choices, six.string_types) or
            #         not is_iterable(self.choices)):
            #     return [
            #         checks.Error(
            #             "'choices' must be an iterable (e.g., a list or tuple).",
            #             obj=self,
            #             id='fields.E004',
            #         )
            #     ]
            # elif any(isinstance(choice, six.string_types) or
            #          not is_iterable(choice) or len(choice) != 2
            #          for choice in self.choices):
            #     return [
            #         checks.Error(
            #             "'choices' must be an iterable containing "
            #             "(actual value, human readable name) tuples.",
            #             obj=self,
            #             id='fields.E005',
            #         )
            #     ]
            # else:
            #     return []
            return []
        else:
            return []

    def _get_default_value(self):
        pass


class CharField(Field):
    def _get_default_value(self):
        if not self.choices:
            return ""
        else:
            return self.choices[0][1]

    # todo: 重写_validate

    def __init__(self, *args, **kwargs):
        super(CharField, self).__init__(*args, **kwargs)
        self.value = self._get_default_value()

    def set_value(self, value):
        if self.check(value):
            self.value = value
        else:
            raise ValueError()

    def get_value(self):
        return self.value


class IPField(Field):
    def _get_default_value(self):
        return "0.0.0.0"

    def __init__(self, *args, **kwargs):
        super(IPField, self).__init__(*args, **kwargs)
        self.value = self._get_default_value()

    # todo: 重写_validate

    def set_value(self, value):
        if self.check(value):
            self.value = value
        else:
            raise ValueError()

    def get_value(self):
        return self.value
