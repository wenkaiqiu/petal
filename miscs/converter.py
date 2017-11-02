import json

import os

prefix = './devices'


def name_induct(name: str):
    attrs = []
    name = name.lower()
    if name.endswith('id'): attrs.append('primary_key=True')
    if name.endswith('name'): attrs.append('String')
    if name.endswith('number'): attrs.append('Float')
    if name.endswith('tag'): attrs.append('String')
    if name.endswith('version'): attrs.append('String')
    if name.endswith('datetime'): attrs.append('DateTime')
    if name.endswith('no'): attrs.append('Integer')
    return ', '.join(attrs)


def reduction(s: dict, prefix=''):
    result = {}
    for k in s:
        if k.startswith('T_'):
            result.update(**reduction(s[k], k.lstrip('T_')))
        else:
            cur_prefix = prefix+'Entity' if prefix.endswith(k) else (prefix + k)
            if type(s[k]) is dict: result.update(**reduction(s[k], cur_prefix))
            else: result[cur_prefix] = f'Column({name_induct(cur_prefix)})'
    return result


converted_dst = os.path.abspath(os.path.join('.', 'devices_converted.py'))
with open(os.path.abspath(os.path.join(converted_dst)), 'w') as converted_f:
    converted_f.write('from sqlalchemy import Column, Integer, String, Float, DateTime\n')
    converted_f.write('from sqlalchemy.ext.declarative import declarative_base\n\n\n')
    converted_f.write('Base = declarative_base()\n\n\n')
    for child in os.listdir('./devices'):
        print(child)
        with open(os.path.join(prefix, child)) as f:
            table_name = os.path.splitext(os.path.basename(child))[0]
            s = json.loads(f.read())
            # write class definition
            converted_f.write(f'class {table_name.capitalize()}(Base):\n')
            # write table_name
            converted_f.write(' ' * 4 + f'table_name = "{table_name}"\n\n')
            for k, v in reduction(s).items():
                converted_f.write(' ' * 4 + f'{k} = {v}\n')
            converted_f.write('\n\n')
