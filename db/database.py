from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# .env読み込み
load_dotenv()

# # 環境変数から取得
# DB_HOST = os.getenv("hostname")
# DB_PORT = os.getenv("port", "3306")
# DB_USER = os.getenv("DB_user")
# DB_PASS = os.getenv("password")
# DB_NAME = "pos_kj"  # あなたが作成したDB名

# DATABASE_URL = (
#     f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# )

# # DBエンジン作成
# # ここで明示的に ssl={"ssl": True} を渡す（Azure用）
# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"ssl": {"ssl": True}}  # ← これがポイント
# )

# 環境変数からデータベース接続情報を取得
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '3306')  # ポートはデフォルト3306
DB_NAME = os.getenv('DB_NAME')

# SSL証明書のパス
# ssl_cert = str(base_path / 'DigiCertGlobalRootCA.crt.pem')

# MySQL接続URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl=true"

# SQLAlchemyエンジン作成（SSLオプションは削除）
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)

# セッション作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Baseクラス
Base = declarative_base()
