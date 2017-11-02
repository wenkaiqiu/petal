from jinja2 import Environment, PackageLoader

import os
project_path = os.path.join(os.getcwd().split("petal")[0], "petal")

env = Environment(
    loader=PackageLoader('uniform_model.functions', 'templates'),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render(name, **kwargs):
    return env.get_template(f'{name}.tmplt').render(**kwargs)
