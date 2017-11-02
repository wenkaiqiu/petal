from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('.', 'templates'),
)


def render(name, **kwargs):
    return env.get_template(f'{name}.tmplt').render(**kwargs).split('\n')
