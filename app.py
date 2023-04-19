"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, default_img_url as default, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    """ Currently redirects to /users """
    return redirect("/users")


@app.route('/users')
def list_users():
    """ Lists all users present in DB as a UL """
    return render_template("users.html", users=User.get_all_users())


@app.route('/users/new', methods=["GET", "POST"])
def new_user():
    """ Redirects to /users if method=POST, otherwise renders the needed form """
    if request.method == 'POST':
        first_name, last_name, image_url = request.form["first-name"], request.form[
            "last-name"], default if not request.form["image-url"] else request.form["image-url"]
        new_user = User(first_name=first_name,
                        last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/users")
    return render_template("new-user-form.html")


@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """ Shows users details """
    return render_template("user-detail.html", user=User.get(user_id), posts=Post.get_posts_by_user(user_id))


@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """ Redirects to /users if method=POST, else renders required form """
    if request.method == "POST":
        user = User.get(user_id)
        user.first_name = request.form["first-name"]
        user.last_name = request.form["last-name"]
        user.image_url = request.form["image-url"] if request.form["image-url"] else default
        db.session.add(user)
        db.session.commit()
        return redirect("/users")
    return render_template("edit-user.html", user=User.get(user_id))


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """ Deletes a user from the DB """
    user = User.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


@app.route('/posts')
def list_posts():
    return render_template("posts.html", posts=Post.get_all_posts())


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """ Shows post """
    [user_id] = db.session.query(Post.user_id).filter(Post.id == post_id).one()
    return render_template("post-detail.html",  user=User.get(user_id), post=Post.query.get_or_404(post_id))


@app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
def new_post(user_id):
    """ Creates new post """
    if request.method == 'POST':
        title = request.form["title"]
        content = request.form["content"]
        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(f"/users/{user_id}")
    return render_template("new-post-form.html", user=User.get(user_id))


@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """ Returns form where user can edit a post """
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.add(post)
        db.session.commit()
        return redirect(f"/users/{user_id}")
    return render_template("edit-post.html", user=User.get(user_id), post=post)


@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """ Deletes a post from the DB """
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")
