from flask import render_template, request, redirect
from flask.wrappers import Response
from flaskblog import db
from flask_login import current_user
from flaskblog.posts.forms import CreateComment
from flaskblog.models import Post, Comment, post_likes
from sqlalchemy import asc, desc, func


def like_action(post_id: Post.id) -> Response:
    liked_post = Post.query.get(post_id)
    if current_user not in liked_post.likes:
        liked_post.likes.append(current_user)
    else:
        liked_post.likes.remove(current_user)
    db.session.add(liked_post)
    db.session.commit()
    return redirect(request.referrer)

def post_logic(post: Post) -> Post | Response:
    post_id = request.args.get('like')
    if post_id:
        return like_action(post_id)
    if not hasattr(post, 'cmnt_form'):
        post.cmnt_form = CreateComment()
    if post.cmnt_form.validate_on_submit():
        new_cmnt(post)
        return redirect(request.referrer)
    return post

def new_cmnt(post: Post) -> None:
    post_id = request.form["post_id"]
    content = post.cmnt_form.content.data
    user_id = current_user.id
    comment = Comment(
           post_id = post_id,
           content = content,
           user_id = user_id
           )
    db.session.add(comment)
    db.session.commit()

def add_params(url: str, params: list[list[str, str]]) -> str:
    if not url.find('?'):
        url += '?'
    url += '&'.join('='.join(i) for i in params)
    return url
    
def parse_params(args: dict) -> dict:
    params = {'page': '1', 'sort': 'date', 'order': 'desc'}
    is_val_valid = {
        'page': lambda x: x.isdigit() and int(x) > 0,
        'sort': lambda x: x in ('date', 'likes', 'comments'),
        'order': lambda x: x in ('desc', 'asc')
    }
    for param in params.keys():
        b = args.get(param)
        if b and is_val_valid[param](b):
            params[param] = b
    return params    

def get_posts(strategy, dsc=True):
    is_dsc = (asc, desc)
    if strategy == 'comments':
        posts = db.session.query(Post).outerjoin(Comment).group_by(Post).order_by(is_dsc[dsc](func.count(Post.comments)))
    elif strategy == 'likes':
        posts = db.session.query(Post).outerjoin(post_likes).group_by(Post).order_by(is_dsc[dsc](func.count(post_likes.c.user_id)))
    else:
        posts = Post.query.order_by(is_dsc[dsc](Post.date_posted))
    if dsc:
        posts = posts
    return posts


def render_home_pg() -> Response:
    params = parse_params(request.args)
    cur_page = int(params['page'])
    dsc = params['order'] == 'desc'
    posts = get_posts(params['sort'], dsc=dsc)
    posts = posts.paginate(page=cur_page, per_page=3)
    post_lst = []
    for post in posts:
        post_or_redir = post_logic(post)
        if isinstance(post_or_redir, Response):
            return post_or_redir
        post_lst.append(post_or_redir)
    return render_template("home.html", title="home page", posts=post_lst, page=cur_page, pages=posts.pages, params=params)

