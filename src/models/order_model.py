from dataclasses import dataclass

@dataclass
class Order:
    order_item_id: int = None
    order_id: str = None
    product_id: str = None
    product_name: str = None
    product_price: float = None
    quantity: int = None,
    