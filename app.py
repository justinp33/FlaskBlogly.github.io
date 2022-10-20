"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, USER, Post, Tag, PostTag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  =  False
app.config['SQLALCHEMY_ECHO'] =  True
app.config['SECRET_KEY'] = "mysecretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def list_users():
    """Shows list of all users in db"""
    users = USER.query.all()
    return render_template('list.html', users=users)

@app.route('/add-user-form')
def add_user_form():
    """Show add user form"""

    return render_template('add_user.html')

@app.route('/', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user  = USER(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/{new_user.id}')

@app.route("/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = USER.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id==user.id)
    return render_template("detail.html", user=user, posts=posts)

@app.route("/<int:user_id>/edit-user-form")
def edit_user_form(user_id):
    """Show edit user form"""
    user = USER.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route('/<int:user_id>/edit-user', methods=["POST"])
def edit_user(user_id):
    """Actually edit user info"""
    user = USER.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect(f'/{user.id}')

@app.route('/<int:user_id>/delete-user', methods=["POST"])
def delete_user(user_id):
    """Delete a user"""
    user = USER.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/')

@app.route("/<int:user_id>/posts/new")
def show_post_form(user_id):
    """Show new post form"""
    user = USER.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("new_post.html", user=user, tags=tags)

@app.route("/<int:user_id>/posts/new", methods=["POST"])
def add_new_post(user_id):
    """Add new post"""
    user = USER.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["content"]
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post  = Post(title=title, content=content, user_id=user.id, tags=tags)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/{user.id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show post"""

    post=Post.query.get_or_404(post_id)

    return render_template('show_post.html', post=post)

@app.route("/posts/<int:post_id>/edit-post")
def edit_post_form(post_id):
    """Show edit post form"""
    post = Post.query.get_or_404(post_id)
    tags=Tag.query.all()

    return render_template("edit_post.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit-post", methods=["POST"])
def edit_post(post_id):
    """Edit an existing post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/{post.user.id}')

@app.route("/posts/<int:post_id>/delete-post", methods=["POST"])
def delete_post(post_id):
    """Delete user post"""

    post=Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect('/')

@app.route('/tags')
def get_tags_list():
    """Lists all tags, with links to the tag detail page."""

    tags=Tag.query.all()

    return render_template("tags_list.html", tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show tag detail"""

    tag=Tag.query.get_or_404(tag_id)

    return render_template('show_tag.html', tag=tag)

@app.route("/tags/new")
def show_tag_form():
    """Show new tag form"""
    
    return render_template("new_tag.html")

@app.route("/tags/new", methods=["POST"])
def add_new_tag():
    """Add new post"""

    name = request.form["name"]

    new_tag  = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route("/tags/<int:tag_id>/edit-tag")
def edit_tag_form(tag_id):
    """Show edit tag form"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit-tag", methods=["POST"])
def edit_tag(tag_id):
    """Edit an existing tag"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]

    db.session.add(tag)
    db.session.commit()

    return redirect(f'/tags')

@app.route("/tags/<int:tag_id>/delete-tag", methods=["POST"])
def delete_tag(tag_id):
    """Delete user tag"""

    tag=Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')







