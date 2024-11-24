from django import template

register = template.Library()

@register.filter(name='default_if_empty')
def default_if_empty(value, default="Not provided"):
    if not value:
        return default
    return value