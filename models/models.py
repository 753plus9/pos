from sqlalchemy import Column, Integer, String, CHAR, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
import datetime

class Item(Base):
    __tablename__ = "items"

    prd_id = Column(Integer, primary_key=True, autoincrement=True)
    # prd_code = Column(Integer, unique=True, nullable=False)
    prd_code = Column(String(13), unique=True, nullable=False)
    prd_name = Column(String(50), nullable=False)
    prd_price = Column(Integer, nullable=False)

    # 関連: 1対多（items → trade_details）
    trade_details = relationship("TradeDetail", back_populates="item")


class Trade(Base):
    __tablename__ = "trade"

    trd_id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(TIMESTAMP, default=datetime.datetime.now)
    emp_cd = Column(CHAR(10), nullable=False, default="9999999999")
    store_cd = Column(CHAR(5), nullable=False, default="30")
    pos_no = Column(CHAR(3), nullable=False, default="90")
    total_amt = Column(Integer, default=0)
    ttl_amt_ex_tax = Column(Integer, default=0)

    # 関連: 1対多（trade → trade_details）
    trade_details = relationship("TradeDetail", back_populates="trade")


class TradeDetail(Base):
    __tablename__ = "trade_detail"

    dtl_id = Column(Integer, primary_key=True, autoincrement=True)
    trd_id = Column(Integer, ForeignKey("trade.trd_id"), nullable=False)
    prd_id = Column(Integer, ForeignKey("items.prd_id"), nullable=False)

    # prd_code = Column(CHAR(13), nullable=False)
    prd_code = Column(String(13), nullable=False)
    prd_name = Column(String(50), nullable=False)
    prd_price = Column(Integer, nullable=False)
    tax_cd = Column(CHAR(2), nullable=False, default="10")

    # 関連
    trade = relationship("Trade", back_populates="trade_details")
    item = relationship("Item", back_populates="trade_details")
