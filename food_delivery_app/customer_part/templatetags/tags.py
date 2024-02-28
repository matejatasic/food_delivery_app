from django.template import Library
from django.utils.html import format_html
from json import dumps

register = Library()


@register.filter
def get_item_quantity(items, key: int):
    try:
        return items[str(key)]["quantity"]
    except:
        return ""

@register.filter
def restaurant_coordinates_json_script(coordinates: list[tuple[float, float]], order_id: str):
    template = '<script id="{}" type="application/json">{}</script>'

    return format_html(template, f"restaurant_coordinates_{order_id}", dumps(coordinates))