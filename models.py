"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# User Model
default_img_url = "https://www.kindpng.com/picc/m/24-248253_user-profile-default-image-png-clipart-png-download.png"

class User(db.Model):
    """ 
    id, an autoincrementing integer number that is the primary key
    first_name and last_name 
    image_url for profile images 
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(35), nullable=False)
    last_name = db.Column(db.String(35), nullable=False)
    image_url = db.Column(db.String, default=default_img_url)

    @classmethod
    def get_all_users(cls):
        return cls.query.order_by(cls.first_name, cls.last_name).all()

    @classmethod
    def get(cls, user_id):
        return cls.query.get_or_404(user_id)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", backref="posts")

    def __repr__(self):
        return f"<Post>\n    id={self.id}, title={self.title}, user={self.user.get_full_name()}, created_at={self.created_at}\n</Post>"

    @classmethod 
    def get_posts_by_user(cls, user_id):
        return cls.query.filter(cls.user_id == user_id).all()

    @classmethod
    def get_all_posts(cls):
        return cls.query.order_by(cls.created_at).all()