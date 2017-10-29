from functools import reduce


class ConfigurationGenerator:
    def __init__(self):
        pass

    def _check_circle(self, function_list, device):
        in_degrees = []
        for func in function_list:
            in_degrees.append(len(getattr(device, func).dependencies))
        if 0 in in_degrees:
            return False
        else:
            return True

    def generate(self, devices):
        output = []  # 存放全部设备的配置信息
        for device in devices:
            loc_output = []  # 存放单个设备的配置信息
            function_list = getattr(device, "support_functions", None)
            if function_list is not None:
                temp_list = function_list.copy()  # 作为队列使用
                if self._check_circle(function_list, device):
                    raise ValueError(f"exit circle in function dependencies of model <{device.model_type}>'")
                while temp_list:
                    func = temp_list.pop(0)
                    func_instance = getattr(device, func)
                    dependencies = func_instance.dependencies
                    # 检验依赖关系
                    if dependencies:
                        if not loc_output:  # 无已配置项时，显然依赖不满足
                            temp_list.append(func)
                        else:   # 有已配置项，检查依赖项是否都满足
                            tag = True  # 作为依赖是否满足的标记
                            for dependency in dependencies:
                                # 依赖项未在已配置内容中，则将标记置为False
                                if not list(filter(lambda key: dependency == key, reduce(lambda a, b: list(a)+list(b), map(lambda item: item.keys(), loc_output)))):
                                    tag = False
                            if not tag:
                                temp_list.append(func)
                            else:
                                loc_output.append({func: func_instance.generate_conf()})
                    else:
                        loc_output.append({func: func_instance.generate_conf()})
            output.append({device.name: loc_output})
        return output
