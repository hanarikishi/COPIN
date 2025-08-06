# ~/COPIN/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import timedelta
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    load_dotenv() # .envから読み込み

    app = Flask(__name__) # Flaskアプリのインスタンス化

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL") #どのDBと接続するのか
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #オブジェクト追跡機能を無効化することで、パフォーマンスを向上
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") #セッションキーの管理

    app.permanent_session_lifetime = timedelta(minutes=40) # セッションの有効期限を30分に設定

    db.init_app(app) #DBをFlaskアプリに接続
    login_manager.init_app(app) #Flask-Loginの初期化
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    from app.models import User # Userモデルのimport (循環インポート防止のため、ここに記載)
    from app.routes.auth import auth_bp # authルートのインポート
    from app.routes.article import article_bp # articleルートのインポート

    # ルートの登録
    app.register_blueprint(auth_bp)
    app.register_blueprint(article_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) # DBからIDでユーザーを取得
    return app