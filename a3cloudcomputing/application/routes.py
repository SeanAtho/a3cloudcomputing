from flask import render_template, url_for, flash, redirect, request
from application import app, db
from application.forms import RegistrationForm, LoginForm, PostForm, UpdateAccountForm, ResetPasswordForm
from application.models import User, Post
from application.utils import hash_password, verify_password, save_picture
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
import markdown
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    for post in posts:
        post.content = markdown.markdown(post.content)
    logger.info('Home page accessed')
    return render_template('home.html', posts=posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = hash_password(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created!', 'success')
            logger.info('New user registered: %s', user.username)
            return redirect(url_for('login'))
        except IntegrityError as e:
            db.session.rollback()
            if 'users.username' in str(e.orig):
                flash('Username already exists. Please choose a different one.', 'danger')
            elif 'users.email' in str(e.orig):
                flash('Email already registered. Please use a different one.', 'danger')
            logger.error('Error registering user: %s', str(e))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and verify_password(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            logger.info('User logged in: %s', user.username)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            logger.warning('Failed login attempt for user: %s', form.email.data)
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logger.info('User logged out: %s', current_user.username)
    logout_user()
    return redirect(url_for('home'))

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        logger.info('New post created by user: %s', current_user.username)
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        logger.info('Account updated for user: %s', current_user.username)
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
