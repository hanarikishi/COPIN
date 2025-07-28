from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


db = SQLAlchemy()

def create_app():
    load_dotenv() # .envから読み込み

    app = Flask(__name__) # Flaskアプリのインスタンス化

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL") #どのDBと接続するのか
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #オブジェクト追跡機能を無効化することで、パフォーマンスを向上

    db.init_app(app) #DBをFlaskアプリに接続

    return app