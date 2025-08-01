# ~/COPIN/app/routes/article.py
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Article, Tag
from datetime import datetime

# articleルートのBlueprintを作成
article_bp = Blueprint('article', __name__)

# 記事の作成
@article_bp.route('/articles', methods=['POST'])
@login_required
def create_article():
    data    = request.get_json()
    title   = data.get('title')
    content = data.get('content')
    tag_names    = data.get('tags', [])

    if not title or not content:
        return jsonify({'error': 'Title and content are required.'}), 400

    # 記事の作成
    article = Article(title=title, content=content, author_id=current_user.id)

    # タグの処理
    for name in tag_names:
        tag = Tag.query.filter_by(name=name).first() # タグが存在するか確認
        if not tag: # タグが存在しない場合は新規作成
            tag = Tag(name=name)
        article.tags.append(tag) # タグを記事に追加

    db.session.add(article) # 記事をデータベースに追加
    db.session.commit() # 変更をコミット

    return jsonify({'message': 'Article created successfully.', 'article_id': article.id}), 201

# 記事の一覧取得
@article_bp.route('/articles', methods=['GET'])
def get_articles():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return jsonify([
        {
            "id": a.id,
            "title": a.title,
            "author": a.author.username,
            "tags": [t.name for t in a.tags],
            "created_at": a.created_at.strftime('%Y-%m-%d')
        }
        for a in articles
    ])

# 記事の詳細取得
@article_bp.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    article = Article.query.get_or_404(article_id)
    return jsonify({
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "author": article.author.username,
            "tags": [t.name for t in article.tags],
            "created_at": article.created_at.strftime('%Y-%m-%d')
    })