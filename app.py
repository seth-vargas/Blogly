"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, default_img_url as default

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def index():
    return redirect("/users")


@app.route('/users')
def list_users():
    return render_template("users.html", users=User.get_all_users())


@app.route('/users/new', methods=["GET"])
def show_new_user_form():
    return render_template("new-user-form.html")


@app.route('/users/new', methods=["POST"])
def post_new_user():
    first_name, last_name, image_url  = request.form["first-name"], request.form["last-name"], default if not request.form["image-url"] else request.form["image-url"]
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.route('/users/<int:user_id>')
def get_user_details(user_id):
    return render_template("user-detail.html", user=User.get(user_id))


@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    return render_template("edit-user.html", user=User.get(user_id))


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def post_user_edit(user_id):
    user = User.get(user_id)

    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["image-url"] if request.form["image-url"] else default

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect("/users")
