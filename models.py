"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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