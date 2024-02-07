from typing import NewType, TypedDict


CartItemDictionary = TypedDict(
    "CartItemDictionary",
    {
        "id": str,
        "name": str,
        "description": str,
        "price": float,
        "image": str,
        "quantity": int,
    },
)
CartItemsDictionary = NewType("CartItemsDictionary", dict[str, CartItemDictionary])
Cart = TypedDict(
    "Cart",
    {
        "items": CartItemsDictionary | dict,
        "total_number_of_items": int,
        "delivery": float,
    },
)
