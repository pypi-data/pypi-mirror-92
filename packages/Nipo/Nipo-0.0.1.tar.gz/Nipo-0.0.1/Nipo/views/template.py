from jinja2 import Template
from .SendBack import SendBack

def render(template,context):
    return SendBack(Template(template).render(**context))