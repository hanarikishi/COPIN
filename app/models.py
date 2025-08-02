# ~/COPIN/app/models.py
from app import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Userモデル定義
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)                # ユーザID
    email         = db.Column(db.String(120), unique=True, nullable=False) # Eメールアドレス
    username      = db.Column(db.String(80), unique=True, nullable=False)  # ユーザ名
    password_hash = db.Column(db.String(256), nullable=False)              # pasuwordハッシュ
    profile       = db.Column(db.Text, nullable=True)                      # プロフィール
    profile_image = db.Column(db.String(120), nullable=True)               # プロフィール画像のURL
    sns_url       = db.Column(db.String(120), nullable=True)               # SNSのURL
    created_at    = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc)) # 作成日
    is_active     = db.Column(db.Boolean, default=True)                    # 論理削除用

    # パスワードをハッシュ化して保存
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 中間モデル：記事とタグのリレーション
article_tags = db.Table('article_tags',
                        db.Column('article_id',db.Integer, db.ForeignKey('articles.id'), primary_key=True),
                        db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
                        )
# タグモデル定義
class Tag(db.Model):
    __tablename__ = 'tags'

    id   = db.Column(db.Integer, primary_key=True)               # ID
    name = db.Column(db.String(50), unique=True, nullable=False) # タグ名

# 記事モデル定義
class Article(db.Model):
    __tablename__ = 'articles'

    id          = db.Column(db.Integer, primary_key=True)   # ID
    title       = db.Column(db.String(100), nullable=False) # タイトル
    content     = db.Column(db.Text, nullable=False)        # 本文
    created_at  = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc)) # 作成日時
    updated_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), onupdate=lambda:datetime.now(timezone.utc)) # 更新日時
    author_id   = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False) # 作成者のユーザID

    author = db.relationship('User', backref=db.backref('articles', lazy='dynamic')) # ユーザとのリレーション
    tags = db.relationship('Tag', secondary=article_tags, backref=db.backref('articles', lazy='dynamic')) # タグとのリレーション