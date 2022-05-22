from django.shortcuts import render
from flask import render_template, Blueprint, url_for, redirect
from flask_login import current_user, login_required
from wannaWatch import db
from wannaWatch.posts.forms import GetParticipants, SearchTitle
from .helpers import searchTitle, getMovie
from wannaWatch.models import Post, User


posts = Blueprint("posts", __name__)
KEY = "k_ak08wghi"

@posts.route("/create-post/<movie>", methods=["GET", "POST"])
@login_required
def create_post(movie):
    form = GetParticipants()
    if form.validate_on_submit():
        movie_id = movie
        movie = getMovie(movie)
        post = Post(author=current_user, name=movie["title"], movie_id=movie_id, plot=movie["plot"], genre=movie["genres"], content_ratings=movie["content_rating"], user_ratings=movie["user_rating"], cast=movie["cast"], image=movie["image"], time_immediate=0, time_later=0, time_never=0, time_answers="")
        participants = form.participants.data
        participants = participants.split(",")
        db.session.add(post)
        db.session.commit()
        for i in participants:
            participant = i.strip()
            user = User.query.filter_by(username=participant).first()
            user.posts.append(post)
            db.session.commit()
        current_user.posts.append(post)
        db.session.commit()
        return redirect(url_for("users.dashboard"))
    return render_template("create_post.html", title="Create Post", form=form)


@posts.route("/search/<title>")
@login_required
def pick_title(title):
    movie = searchTitle(title)
    return render_template("movie_options.html", title=f"Results for {title}", movies=movie)
