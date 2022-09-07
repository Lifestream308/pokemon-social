from lib2to3.pgen2 import token
from turtle import title
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from capstone import app, db, bcrypt
from capstone.forms import RegistrationForm, AccountForm, LoginForm, PostForm
from capstone.models import User, Post, users_schema, posts_schema, post_schema
from flask_login import login_user, current_user, logout_user, login_required
from helpers import token_required

# Token API PROTECTED ROUTES
# Create
@app.route('/create_post', methods = ['POST'])
@token_required
def create_post(current_user_token):
    title = request.json['title']
    content = request.json['content']
    author = User.query.filter_by(token=current_user_token.token).first()
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    post = Post(title, content, author, user_token)

    db.session.add(post)
    db.session.commit()

    response = post_schema.dump(post)
    return jsonify(response)

# Retrieve all
@app.route("/apigetposts", methods=['GET'])
@token_required
def apigetposts(current_user_token): 
    getposts = Post.query.all()

    print(f'BIG TESTER: {current_user_token.token}')

    result = posts_schema.dump(getposts)
    return jsonify(result)

# Retrieve one
@app.route("/apigetposts/<id>", methods=['GET'])
@token_required
def apigetpost(current_user_token, id): 
    getpost = Post.query.get(id)
    return post_schema.jsonify(getpost)

# Update
@app.route('/updatepost/<id>', methods = ['PUT'])
@token_required
def updatepost(current_user_token, id):

    post = Post.query.get(id)

    title = request.json['title']
    content = request.json['content']

    post.title = title
    post.content = content

    print(f'BIG TESTER: {current_user_token.token}')

    db.session.commit()

    return post_schema.jsonify(post)

# Delete
@app.route("/delete/<id>", methods=['Delete'])
@token_required
def apidelete(current_user_token, id): 
    getpost = Post.query.get(id)

    db.session.delete(getpost)
    db.session.commit()

    return post_schema.jsonify(getpost)

# Start of UNPROTECTED API Routes
@app.route("/getusers", methods=['GET'])
def getusers(): 
    getusers = User.query.all()
    result = users_schema.dump(getusers)
    return jsonify(result)

@app.route("/getposts", methods=['GET'])
def getposts(): 
    getposts = Post.query.all()
    result = posts_schema.dump(getposts)
    return jsonify(result)
# End API Routes

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/pokedex")
def pokedex():
    return render_template('pokedex.html')

@app.route("/trainers")
def trainers():
    return render_template('trainers.html', trainers=User.query.all())

@app.route("/blog")
def blog():
    return render_template('blog.html', blog=Post.query.order_by(Post.id.desc()).all())

@app.route("/userposts")
@login_required
def userposts():
    return render_template('userposts.html', userposts=Post.query.filter_by(author=current_user).order_by(Post.id.desc()).all())

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, picture=form.picture.data, pokemon=form.pokemon.data, tagline=form.tagline.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password')
    return render_template('login.html', form=form)

@app.route("/guest")
def guest():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.query.filter_by(email='guest@guest.com').first()
    login_user(user)
    return render_template('home.html')

@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html')

# Create, Read, Update, Delete
@app.route("/new_post", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user, user_token=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!')
        return redirect(url_for('blog'))
    return render_template('new_post.html', form=form, legend="New Post")

@app.route("/update_account", methods=['GET', 'POST'])
@login_required
def update_account():
    user = User.query.filter_by(email=current_user.email).first()
    if user != current_user:
        abort(403)
    form = AccountForm()
    if form.validate_on_submit():
        user.picture = form.picture.data
        user.pokemon = form.pokemon.data
        user.tagline = form.tagline.data
        db.session.commit()
        flash('Your account has been updated!')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.picture.data = user.picture
        form.pokemon.data = user.pokemon
        form.tagline.data = user.tagline
    return render_template('update_account.html', form=form, legend='Update Account', user=user)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!')
        return redirect(url_for('userposts'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('new_post.html', form=form, legend='Update Post', post=post, delete="Delete")


@app.route("/post/<int:post_id>/delete", methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    return render_template('delete_post.html', post=post)

@app.route("/post/<int:post_id>/deleted", methods=['GET','POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!')
    return redirect(url_for('userposts'))