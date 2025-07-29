from app import db
from datetime import datetime

# Userモデル定義
class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)                 # ユーザID
    email         = db.Column(db.String(120), unique=True, nullable=False)  # Eメールアドレス
    password_hash = db.Column(db.String(120), nullable=False)               # pasuwordハッシュ
    username      = db.Column(db.String(80), unique=True, nullable=False)   # ユーザ名
    profile       = db.Column(db.Text, nullable=True)                       # プロフィール
    profile_image = db.Column(db.String(120), nullable=True)                # プロフィール画像のURL
    sns_url       = db.Column(db.String(120), nullable=True)                # SNSのURL
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)         # 作成日
    is_active     = db.Column(db.Boolean, default=True)                     # 論理削除用