from flask import render_template, Blueprint
from flaskblog.posts.utils import render_home_pg

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
def home():
    return render_home_pg()

@main.route("/about")
def about():
    return render_template("about.html")
