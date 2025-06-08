from sqlalchemy.orm import Session
from sqlalchemy import func
from models.models import Item, Trade, TradeDetail
from typing import List
import datetime

# 商品コードで商品を取得
# def get_item_by_code(db: Session, prd_code: str):
#     return db.query(Item).filter(Item.prd_code == prd_code).first()


def get_item_by_code(db: Session, prd_code: str):
    return db.query(Item).filter(func.trim(Item.prd_code) == prd_code.strip()).first()


# 取引登録＋取引明細登録（purchase処理）
def create_trade_with_details(db: Session, emp_cd: str, items: List[dict]):
    # 合計計算
    total_ex_tax = sum(item["prd_price"] for item in items)
    tax = int(total_ex_tax * 0.1)
    total = total_ex_tax + tax

    # 取引登録
    trade = Trade(
        emp_cd=emp_cd or "9999999999",
        store_cd="30",
        pos_no="90",
        total_amt=total,
        ttl_amt_ex_tax=total_ex_tax
    )
    db.add(trade)
    db.commit()
    db.refresh(trade)

    # 明細登録
    for item in items:
        detail = TradeDetail(
            trd_id=trade.trd_id,
            prd_id=item["prd_id"],
            prd_code=str(item["prd_code"]),
            prd_name=item["prd_name"],
            prd_price=item["prd_price"],
            tax_cd="10"
        )
        db.add(detail)

    db.commit()

    return {
        "success": True,
        "total_ex_tax": total_ex_tax,
        "tax": tax,
        "total": total
    }
