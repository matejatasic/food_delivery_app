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

OrderItemDto = TypedDict("OrderItemDto", {"name": str, "quantity": int})

MostLikedRestaurantDict = TypedDict(
    "MostLikedRestaurantDict",
    {"id": int, "name": str, "image": str, "number_of_likes": int},
)
MostOrderedRestaurantItemsDict = TypedDict(
    "MostOrderedRestaurantItemsDict",
    {"image": str, "quantity": int, "restaurant_id": int},
)
