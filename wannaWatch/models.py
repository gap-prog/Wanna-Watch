from datetime import datetime
from flask_login import UserMixin
from wannaWatch import db, login_manager


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


association = db.Table("association",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"))
)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    created = db.relationship("Post", backref="author", lazy=True)
    posts = db.relationship("Post", secondary=association)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.created}', '{self.posts}')"


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    time_answers = db.Column(db.String(length=1000), nullable=False)
    name = db.Column(db.String(length=50), nullable=False)
    movie_id = db.Column(db.String(length=50), nullable=False)
    plot = db.Column(db.String(length=500), nullable=False)
    genre = db.Column(db.String(length=20), nullable=False)
    content_ratings = db.Column(db.String(length=20))
    user_ratings = db.Column(db.String(length=20))
    cast = db.Column(db.String(length=70), nullable=False)
    image = db.Column(db.String(length=500), nullable=False)
    time_immediate = db.Column(db.Integer)
    time_later = db.Column(db.Integer)
    time_never = db.Column(db.Integer)

    def getAuthor(self):
        return self.user_id
    
    def __repr__(self):
        return f"{self.movie_id},{self.id}"
