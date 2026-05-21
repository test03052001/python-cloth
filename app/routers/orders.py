from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.logging_config import get_logger
from app.models.customer import Customer
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import create_order

router = APIRouter(prefix="/orders", tags=["Orders"])
logger = get_logger()


@router.get("", response_model=list[OrderResponse])
def list_orders(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return (
        db.query(Order)
        .options(joinedload(Order.items))
        .order_by(Order.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def place_order(payload: OrderCreate, db: Session = Depends(get_db)):
    if not db.get(Customer, payload.customer_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer not found")
    try:
        order = create_order(db, payload)
    except ValueError as exc:
        logger.warning("Order validation failed: %s", exc)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    logger.info("Created order id=%s number=%s total=%s", order.id, order.order_number, order.total_amount)
    return order


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, status_value: str, db: Session = Depends(get_db)):
    allowed = {"pending", "confirmed", "shipped", "delivered", "cancelled"}
    if status_value not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status must be one of: {', '.join(sorted(allowed))}",
        )
    order = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    order.status = status_value
    db.commit()
    db.refresh(order)
    logger.info("Order id=%s status updated to %s", order_id, status_value)
    return order
