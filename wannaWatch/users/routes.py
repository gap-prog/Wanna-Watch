from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from wannaWatch import db, bcrypt
from wannaWatch.models import User, Post
from wannaWatch.posts.helpers import getMovie
from wannaWatch.users.forms import RegistrationForm, LoginForm
from wannaWatch.posts.forms import SearchTitle, PickTime
from ..posts.helpers import getMovie


users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.dashboard"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, password=hashed_password, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("users.dashboard"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("users.dashboard"))
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard(movie_id=None):
    user = User.query.filter_by(username=current_user.username).first()
    posts = user.posts
    form = SearchTitle()
    form2_list = []
    for j in posts:
        form2 = PickTime()
        form2.post_id = str(j).split(",")[1]
        form2.submit_name = j
        form2_list.append(form2)
    if form.validate_on_submit():
        return redirect(url_for(f"posts.pick_title", title=form.title.data))
    for k in form2_list:
        if k.validate_on_submit():
            option = k.values.data
            post_id = k.post_id
    movies = {}
    for i in posts:
        i = str(i).split(",")
        movie = i[0]
        movies[movie] = [getMovie(str(movie)), i[1].strip()]
    movie_keys = list(movies.keys())
    return render_template("dashboard.html", title=f"{current_user.username}'s Dashboard", movies=movies, movie_keys=movie_keys, form=form, form2_list=form2_list)
