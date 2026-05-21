import uuid
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate


def generate_order_number() -> str:
    return f"ORD-{uuid.uuid4().hex[:12].upper()}"


def create_order(db: Session, payload: OrderCreate) -> Order:
    order = Order(
        customer_id=payload.customer_id,
        order_number=generate_order_number(),
        status="pending",
        shipping_address=payload.shipping_address,
        notes=payload.notes,
        total_amount=Decimal("0"),
    )
    db.add(order)
    db.flush()

    total = Decimal("0")
    for item_data in payload.items:
        product = db.get(Product, item_data.product_id)
        if not product or not product.is_active:
            raise ValueError(f"Product {item_data.product_id} not available")
        if product.stock_quantity < item_data.quantity:
            raise ValueError(
                f"Insufficient stock for product {product.name}. "
                f"Available: {product.stock_quantity}"
            )

        unit_price = product.discount_price or product.price
        subtotal = unit_price * item_data.quantity
        total += subtotal

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item_data.quantity,
            unit_price=unit_price,
            subtotal=subtotal,
        )
        db.add(order_item)
        product.stock_quantity -= item_data.quantity

    order.total_amount = total
    db.commit()
    db.refresh(order)
    return order
