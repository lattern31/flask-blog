from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import login_manager
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateUser)
from flaskblog.users.utils import save_picture
from flaskblog.posts.utils import post_logic
from flask.wrappers import Response


users = Blueprint('users', __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
                )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('form_full_page.html', title="Register", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_pw(form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('unsuccessful login', 'danger')
    return render_template('form_full_page.html', title="Auth", form=form)

@users.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('main.home'))
        
@users.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = UpdateUser()
    if form.validate_on_submit():
        if form.picture.data:
            picture_name = save_picture(form.picture.data)
            current_user.avatar = picture_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.description = form.description.data
        db.session.commit()
        flash('your account has been updated!', 'success')
        return redirect('/user/' + current_user.username)
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.description.data = current_user.description  
    posts = Post.query.filter_by(user_id=current_user.id)
    image_file = url_for('static', filename='profile_pics/' + current_user.avatar)
    return render_template("user_edit_page.html", title="Edit profile", posts=posts, image_file=image_file, form=form)

@users.route("/user/<username>", methods=["GET", "POST"])
def user_page(username):
    user = User.query.filter_by(username=username).first() 
    image_file = url_for('static', filename='profile_pics/' + user.avatar)
    posts = user.posts
    post_lst = []
    for post in posts:
        post_or_redir = post_logic(post)
        if isinstance(post_or_redir, Response):
            return post_or_redir
        post_lst.append(post_or_redir)
    return render_template(
                "user_page.html",
                title=username, 
                user=user, 
                posts=post_lst,
                image_file=image_file, 
                is_loged=current_user.is_authenticated
                )
