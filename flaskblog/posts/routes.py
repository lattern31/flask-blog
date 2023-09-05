from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask.wrappers import Response
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment
from flaskblog.posts.forms import CreatePost, CreateComment
from flaskblog.posts.utils import post_logic, parse_params 

posts = Blueprint('posts', __name__)

@posts.route("/new_post", methods=["GET", "POST"])
@login_required
def new_post():
    form = CreatePost()
    if form.validate_on_submit():
        post = Post(
                title=form.title.data, 
                content=form.content.data, 
                author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post Created", "success")
        return redirect(url_for('main.home'))
    return render_template("form_full_page.html", title="Create Post", form=form)

@posts.route("/post/<int:post_id>", methods=["GET", "POST"])
def post_page(post_id):
    post = Post.query.get(post_id)
    post_or_redir = post_logic(post)
    if isinstance(post_or_redir, Response):
        return post_or_redir
    return render_template('post_page.html', title=post.title, post=post_or_redir)

@posts.route("/post/<int:post_id>/comments", methods=["GET", "POST"])
def post_comments_page(post_id):
    page = int(parse_params(request.args)['page'])
    post = Post.query.get(post_id)
    comments = Comment.query.filter_by(post_id=post.id).paginate(page=page, per_page=5)
    return render_template('comments_page.html', comments=comments, page=page, pages=comments.pages, post_id=post_id)

