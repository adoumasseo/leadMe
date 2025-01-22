
from app.controllers.main import bp
from flask import render_template
from app.database.models.post import Post


@bp.route('/')
def index():
    latest_posts = Post.query.order_by(Post.created_at.desc()).limit(3).all()
    return render_template("landing_page.html", posts=latest_posts)

@bp.route('/all-posts')
def all_posts():
    all_post = Post.query.all()
    return render_template("posts.html", posts=all_post)