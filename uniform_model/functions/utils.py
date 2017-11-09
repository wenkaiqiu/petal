from jinja2 import Environment, PackageLoader

env = Environment(
    loader=PackageLoader('uniform_model.functions', 'templates'),
    trim_blocks=True,
)


def render(name, **kwargs):
    return env.get_template(f'{name}.tmplt').render(**kwargs)
