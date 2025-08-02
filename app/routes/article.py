# ~/COPIN/app/routes/article.py
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Article, Tag
from datetime import datetime, timezone

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
    article = Article.query.get_or_404(article_id)# レコードを取得、存在しない場合HTTP404エラー
    return jsonify({
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "author": article.author.username,
            "tags": [t.name for t in article.tags],
            "created_at": article.created_at.strftime('%Y-%m-%d')
    })

# 記事の更新
@article_bp.route('/articles/<int:article_id>', methods=['PATCH'])
@login_required
def update_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article.author_id != current_user.id:
        return jsonify({'error': 'You are not authorized to update this article.'}), 403
    data    = request.get_json()
    title   = data.get('title')
    content = data.get('content')
    tags    = data.get('tags', [])

    if title:
        article.title = title
    if content:
        article.content = content
    if tags:
        article.tags.clear()
        for name in tags:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
            article.tags.append(tag)
    article.updated_at = datetime.now(timezone.utc)

    db.session.commit()
    return jsonify({'message': 'Article updated successfully.'}), 200

# 記事の削除
@article_bp.route('/articles/<int:article_id>', methods=['DELETE'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article.author_id != current_user.id:
        return jsonify({'error': 'You are not authorized to delete this article.'}), 403
    db.session.delete(article)
    db.session.commit()
    return jsonify({'message': 'Article deleted successfully.'}), 200
