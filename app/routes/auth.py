# ~/COPIN/app/routes/auth.py
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() # JSONリクエストを取得

    # emailとパスワードを取得
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first() # emailと一致するユーザーを取得

    if user and user.check_password(password): # パスワードが一致するか確認
        login_user(user, remember=False) # ログイン処理
        return jsonify({'message': 'login successful', 'user_id': user.id}), 200
    else:
        # セキュリティのため、同じメッセージを返す
        return jsonify({'message': 'Invalid email or password'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required # ログインユーザーのみアクセス可能(未ログイン時は401エラー)
def logout():
    logout_user() # ログアウト処理(セッション破棄)
    return jsonify({"message": "logout successful"}), 200

@auth_bp.route('/me', methods=['GET'])
@login_required
def current_user_info():
    if current_user.is_authenticated:
        user_info = {
            'id': current_user.id,
            'email': current_user.email,
            'username': current_user.username,
        }
        return jsonify(user_info), 200
    else:
        return jsonify({'message': 'User not authenticated'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not username or not password:
        return jsonify({'message': 'Email, username and password are required'}), 400
    # 8~16文字のパスワード制限、大文字をいれること
    if len(password) < 8 or len(password) > 16 or not any(c.isupper() for c in password):
        return jsonify({'message': 'Password must be 8-16 characters long and contain at least one uppercase letter'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 409
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 409

    user = User(email = email, username = username) # ユーザインスタンスを作成
    user.set_password(password) # ハッシュ化
    db.session.add(user) # DBに追加
    db.session.commit() # 変更をコミット
    login_user(user, remember=False) # 登録後にログイン状態にする
    return jsonify({'message': 'User registered successfully'}), 200