from django.template import Library

register = Library()


@register.filter
def get_item_quantity(items, key: int):
    try:
        return items[str(key)]["quantity"]
    except:
        return ""
