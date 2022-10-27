from django import template

register = template.Library()


@register.filter(name='orientation_as_string')
def convert_orientation_to_string_representation(value):
    try:
        int_value = int(value)
        return ["portrait", "landscape"][int_value % 2]
    except (TypeError, ValueError):
        return "-"
