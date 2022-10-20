from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# 總表格
class Order(BaseModel):
    # order_id: str = Field(min_length=1)
    customer_name: str = Field(min_length=1, max_length=100)
    customer_id: str = Field(min_length=1, max_length=100)
    purchase_time: datetime


@app.get("/order")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Order).all()


@app.post("/order/add")
def create_order(order: Order, db: Session = Depends(get_db)):

    order_model = models.Order()

    order_model.customer_name = order.customer_name
    order_model.customer_id = order.customer_id
    order_model.purchase_time = order.purchase_time

    db.add(order_model)
    db.commit()
    return order

# @app.put("/{order_id}")
@app.put("/order/modify")
def update_order(order_id: int, order: Order, db: Session = Depends(get_db)):

    order_model = db.query(models.Order).filter(models.Order.order_id == order_id).first()

    if order_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {order_id} : Does not exist"
        )

    order_model.customer_name = order.customer_name
    order_model.customer_id = order.customer_id
    order_model.purchase_time = order.purchase_time

    db.add(order_model)
    db.commit()

    return order

@app.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order_model = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {order_id} : Does not exist"
        )
    db.query(models.Order).filter(models.Order.order_id == order_id).delete()
    db.commit()

# item表格

class Order_item(BaseModel):

    product_name: str = Field(min_length=1, max_length=100)
    amount: int = Field(gt=0)
    price: int = Field(gt=0)
    product_id: str = Field(min_length=1, max_length=100)

@app.get("/order_item")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Order_item).all()

@app.post("/order_item/add")
def create_order_item(order_item: Order_item, db: Session = Depends(get_db)):

    order_model = models.Order_item()

    order_model.product_name = order_item.product_name
    order_model.product_id = order_item.product_id
    order_model.amount = order_item.amount
    order_model.price = order_item.price

    db.add(order_model)
    db.commit()

    return order_item


# @app.put("/{order_id}")
@app.put("/order_item/modify")
def update_order_item(order_id: int, order_item: Order_item, db: Session = Depends(get_db)):

    order_model = db.query(models.Order_item).filter(models.Order_item.order_id == order_id).first()

    if order_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {order_id} : Does not exist"
        )
    #order_model.order_id = order.order_id
    order_model.product_name = order_item.product_name
    order_model.product_id = order_item.product_id
    order_model.amount = order_item.amount
    order_model.price = order_item.price

    db.add(order_model)
    db.commit()

    return order_item

# @app.delete("/{order_id}")

@app.delete("/{order_id}/item")
def delete_order_item(order_id: int, db: Session = Depends(get_db)):
    order_model = db.query(models.Order).filter(models.Order.id == order_id).first()

    if order_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {order_id} : Does not exist"
        )
    db.query(models.Order_item).filter(models.Order_item.order_id == order_id).delete()
    db.commit()