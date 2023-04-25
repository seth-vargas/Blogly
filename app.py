"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)
db.create_all()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

##############################################################################################
#                                      Routes for part 1                                     #
##############################################################################################


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
    """ If method=POST, redirect to '/users', else render 'new-user-form' """
    if request.method == 'POST':
        first_name = request.form["first-name"]
        last_name = request.form["last-name"]
        image_url = request.form["image-url"]

        if request.form["image-url"]:
            new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        else:
            new_user = User(first_name=first_name, last_name=last_name)

        db.session.add(new_user)
        db.session.commit()
        return redirect("/users")
    return render_template("new-user-form.html")


@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """ Shows users details """
    return render_template("user-detail.html", user=User.get(user_id), posts=Post.get_all_by_user(user_id))


@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """ if method=POST, redirects to /users, else render 'edit-user' """
    user = User.get(user_id)
    if request.method == "POST":
        user.first_name = request.form["first-name"]
        user.last_name = request.form["last-name"]
        user.image_url = request.form["image-url"]
        
        if request.form["image-url"]:
            user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        else:
            user = User(first_name=first_name, last_name=last_name)

        db.session.add(user)
        db.session.commit()
        return redirect("/users")
    return render_template("edit-user.html", user=user)


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """ Deletes a user from the DB """
    db.session.delete(User.get(user_id))
    db.session.commit()
    return redirect("/users")

##############################################################################################
#                                      Routes for part 2                                     #
##############################################################################################


@app.route('/posts')
def list_posts():
    return render_template("posts.html", posts=Post.get_all())


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """ Shows post """
    [user_id] = db.session.query(Post.user_id).filter(Post.id == post_id).one()
    return render_template("post-detail.html",  user=User.get(user_id), post=Post.get(post_id))


@app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
def new_post(user_id):
    """ Creates new post """
    if request.method == 'POST':
        title = request.form["title"]
        content = request.form["content"]
        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        tags = request.form.getlist("tags")
        for tag in tags:
            db.session.add(PostTag(post_id=new_post.id, tag_id=int(tag)))

        db.session.commit()

        return redirect(f"/users/{user_id}")
    return render_template("new-post-form.html", user=User.get(user_id), tags=Tag.query.all())


@app.route('/posts/<int:post_id>/edit', methods=["GET", "POST"])
def edit_post(post_id):
    """ Returns form where user can edit a post """
    post = Post.get(post_id)
    user_id = post.user.id
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.add(post)
        db.session.commit()

        tags = request.form.getlist("tags")
        for tag in tags:
            db.session.add(PostTag(post_id=post_id, tag_id=int(tag)))

        db.session.commit()
        return redirect(f"/users/{user_id}")
    return render_template("edit-post.html", user=User.get(user_id), post=post, tags=Tag.query.all())


@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """ Deletes a post from the DB """
    post = Post.get(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

##############################################################################################
#                                      Routes for part 3                                     #
##############################################################################################


@app.route("/tags")
def list_tags():
    """ Lists all tags, with links to the tag detail page. """
    return render_template("list-tags.html", tags=Tag.query.all())


@app.route("/tags/<int:tag_id>")
def show_tag_details(tag_id):
    """ Show detail about a tag. Have links to edit form and to delete. """
    return render_template("tag-details.html", tag=Tag.get(tag_id))


@app.route("/tags/new", methods=["GET", "POST"])
def new_tag():
    """ 
    POST: Process add form, create new Tag object, and redirect to tag list.
    GET: Show form to add a new tag. 
    """

    if request.method == "POST":
        name = request.form["name"]
        new_tag = Tag(name=name)

        db.session.add(new_tag)
        db.session.commit()

        return redirect(f"/tags")

    return render_template("new-tag-form.html")


@app.route("/tags/<int:tag_id>/edit", methods=["GET", "POST"])
def edit_tag(tag_id):
    """
    POST: Process edit form, edit tag, and redirects to the tags list. 
    GET: Show edit form for a tag.
    """
    tag = Tag.get(tag_id)
    if request.method == "POST":
        tag.name = request.form["name"]
        db.session.add(tag)
        db.session.commit()
        return redirect("/tags")
    return render_template("edit-tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/delete")
def delete_tag(tag_id):
    """ Delete a tag. """
    tag = Tag.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")
