from flask_sqlalchemy import SQLAlchemy
import time

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

default_img_url = "https://www.kindpng.com/picc/m/24-248253_user-profile-default-image-png-clipart-png-download.png"

##############################################################################################
#                                         User Model                                         #
##############################################################################################

class User(db.Model):
    """ User Model """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(35), nullable=False)
    last_name = db.Column(db.String(35), nullable=False)
    image_url = db.Column(db.String, default=default_img_url)
    posts = db.relationship("Post", cascade="all, delete", backref="users")

    def __repr__(self):
        return f"<User: {self.get_full_name()}>"

    @classmethod
    def get_all_users(cls):
        return cls.query.order_by(cls.first_name, cls.last_name).all()

    @classmethod
    def get(cls, user_id):
        return cls.query.get_or_404(user_id)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

##############################################################################################
#                                   Joining Table: PostTag                                   #
##############################################################################################


class PostTag(db.Model):
    """ Mapping of tags to posts """

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        "posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

    def __repr__(self):
        return f"<PostTag: {self.post_id}, {self.tag_id}"

##############################################################################################
#                                         Post Model                                         #
##############################################################################################

class Post(db.Model):
    """ Post model """

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.Time, nullable=False,
                           default=time.strftime("%Y-%m-%d %H:%M"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User")
    tags = db.relationship("Tag", secondary="posts_tags", backref='posts')

    def __repr__(self):
        return f"<Post: {self.title}>"

    @classmethod
    def get_all(cls):
        return cls.query.order_by(cls.created_at).all()

    @classmethod
    def get_all_by_user(cls, user_id):
        """ Returns a list of all posts a user has """
        return cls.query.filter(cls.user_id == user_id).all()

    @classmethod
    def get(cls, post_id):
        return cls.query.get_or_404(post_id)

##############################################################################################
#                                         Tag Model                                          #
##############################################################################################

class Tag(db.Model):
    """ Tag model """

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Tag: {self.name}>"

    @classmethod
    def get(cls, tag_id):
        return cls.query.get_or_404(tag_id)
