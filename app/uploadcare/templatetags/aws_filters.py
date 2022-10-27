from collections import defaultdict

from django import template


register = template.Library()


@register.filter(name="get_inner_values")
def extract_values_from_list_of_dict(value):
    unique_values = set()
    for _dict in value:
        unique_values.update(_dict.values())

    return list(unique_values)


@register.filter(name="pivot_the_data")
def group_values_by_keys(value):
    by_same_keys = defaultdict(list)
    for _dict in value:
        for _key, _value in _dict.items():
            by_same_keys[_key].append(_value)

    result = []
    for _same_key, _collection in by_same_keys.items():
        result.append("{k}: {v}".format(k=_same_key, v=", ".join(map(str, _collection))))
    return "\n".join(result)
