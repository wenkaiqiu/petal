import json
import re
import os


def convert(k):
    s1 = re.sub(r'IP', 'Ip', k)
    s2 = re.sub(r'(?P<value>[A-Z][a-z]+)', lambda v: '_'+v.group('value').lower(), s1)
    s3 = re.sub(r'^_', "", s2)
    s = re.sub(r'(?P<value>[A-Z])', lambda v: v.group('value').lower(), s3)
    print(s)
    return s


def reduction(s: dict):
    result = {}
    for k in s:
        if k.startswith('T_'):
            result[k.lstrip('T_').lower()] = {}
            result[k.lstrip('T_').lower()].update(**reduction(s[k]))
        else:
            if type(s[k]) is dict:
                result.update(**reduction(s[k]))
            else:
                result[convert(k)] = k
    return result


prefix = './devices'

converted_dst = os.path.abspath(os.path.join('.', 'map.py'))
with open(os.path.abspath(os.path.join(converted_dst)), 'w') as converted_f:
    for child in os.listdir('./devices'):
        print(child)
        with open(os.path.join(prefix, child)) as f:
            map_name = os.path.splitext(os.path.basename(child))[0]
            s = json.load(f)
            # write dict definition
            converted_f.write(f'{map_name}_map = ' + '{\n')
            for k, v in reduction(s).items():
                converted_f.write(' ' * 4 + f"'{k}': " + "{\n")
                for k2, v2 in v.items():
                    converted_f.write(' ' * 8 + f"'{k2}': '{v2}',\n")
                converted_f.write(' ' * 4 + '},\n')
            converted_f.write('}\n\n')
