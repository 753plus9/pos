from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# .env読み込み
load_dotenv()

# 環境変数から取得
DB_HOST = os.getenv("hostname")
DB_PORT = os.getenv("port", "3306")
DB_USER = os.getenv("username")
DB_PASS = os.getenv("password")
DB_NAME = "pos_kj"  # あなたが作成したDB名

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# DBエンジン作成
# ここで明示的に ssl={"ssl": True} を渡す（Azure用）
engine = create_engine(
    DATABASE_URL,
    connect_args={"ssl": {"ssl": True}}  # ← これがポイント
)

# セッション作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Baseクラス
Base = declarative_base()
