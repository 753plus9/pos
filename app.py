from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from crud import crud
from db.database import SessionLocal, engine
from models.models import Base, Item, Trade, TradeDetail
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import datetime

# DB初期化（初回実行時のみ必要）
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS（Next.jsからアクセスするため）
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[
    #     "http://localhost:3000",  # フロントのURLに合わせて変更
    #     "https://localhost:3000",  # ←追加！
    #     "https://192.168.3.13:3000",
    # ],
    allow_origins=["*"],  # ← 本番環境では非推奨
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DBセッション依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- スキーマ定義（Pydantic） ---

class ProductResponse(BaseModel):
    prd_id: int
    prd_code: str
    prd_name: str
    prd_price: int

    class Config:
        orm_mode = True

class PurchaseItem(BaseModel):
    prd_id: int
    prd_code: str
    prd_name: str
    prd_price: int

class PurchaseRequest(BaseModel):
    emp_cd: str
    items: List[PurchaseItem]


# --- APIエンドポイント ---

# 商品コードで商品を検索
@app.get("/products/{prd_code}", response_model=ProductResponse)
def get_product(prd_code: str, db: Session = Depends(get_db)):
    
    print(f"🔍 検索対象のコード: [{prd_code}]")  # デバッグ用
    
    item = crud.get_item_by_code(db, prd_code)
    if not item:
        raise HTTPException(status_code=404, detail="該当の商品がありませんでした")
    return item


# 購入処理（取引＋明細登録）
@app.post("/purchase")
# def register_purchase(request: PurchaseRequest, db: Session = Depends(get_db)):
#     if not request.items:
#         raise HTTPException(status_code=400, detail="商品が入力されていません")
    
#     items = [item.dict() for item in request.items]
#     return crud.create_trade_with_details(db, request.emp_cd, items)

def register_purchase(request: PurchaseRequest, db: Session = Depends(get_db)):
    try:
        if not request.items:
            raise HTTPException(status_code=400, detail="商品が入力されていません")

        items = [item.dict() for item in request.items]
        return crud.create_trade_with_details(db, request.emp_cd, items)
    except Exception as e:
        print(f"❌ 登録エラー: {e}")
        raise HTTPException(status_code=500, detail="購入処理中にエラーが発生しました")