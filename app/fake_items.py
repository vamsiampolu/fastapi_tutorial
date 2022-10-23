from app.models.item import Item
from app.models.offer import Offer

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

fake_items_db2 = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

keyword_weights = {"foo": 2.3, "bar": 3.4}

logisitics_items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


def create_offer(offer_id: str) -> Offer:
    return Offer(
        id=offer_id,
        name="My Offer",
        description="This is my offer",
        price=122.24,
        items=[
            Item(
                name="my item",
                price=200.125,
                tags={"electronics", "mobile", "accessories"},
            )
        ],
    )
