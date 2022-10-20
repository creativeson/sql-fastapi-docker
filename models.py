from sqlalchemy import Column, Integer, String, TEXT
from database import Base


class Order(Base):
    __tablename__ = "order"

    order_id = Column(Integer, primary_key=True, index=True, nullable=True)
    customer_name = Column(String)
    customer_id = Column(String)
    purchase_time = Column(TEXT)

class Order_item(Base):
    __tablename__ = "order item"

    order_id = Column(Integer, primary_key=True, index=True, nullable=True)
    product_name = Column(String)
    amount = Column(Integer)
    product_id = Column(String)
    price = Column(Integer)

