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
    """
    Renders the home page with a list of posts.
    
    Converts Markdown content to HTML.
    Logs the access to the home page.
    """
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    for post in posts:
        post.content = markdown.markdown(post.content)  # Convert Markdown to HTML
    logger.info('Home page accessed')
    return render_template('home.html', posts=posts)

@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Handles user registration.
    
    If the user is already authenticated, redirects to the home page.
    Validates the registration form and creates a new user if valid.
    Logs the registration process and any errors.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = hash_password(form.password.data)  # Hash the user's password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created!', 'success')
            logger.info('New user registered: %s', user.username)
            return redirect(url_for('login'))
        except IntegrityError as e:
            db.session.rollback()  # Rollback the session in case of an error
            if 'users.username' in str(e.orig):
                flash('Username already exists. Please choose a different one.', 'danger')
            elif 'users.email' in str(e.orig):
                flash('Email already registered. Please use a different one.', 'danger')
            logger.error('Error registering user: %s', str(e))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Handles user login.
    
    If the user is already authenticated, redirects to the home page.
    Validates the login form and logs in the user if valid.
    Logs the login attempts and any failures.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and verify_password(user.password, form.password.data):
            login_user(user, remember=form.remember.data)  # Log the user in
            logger.info('User logged in: %s', user.username)
            next_page = request.args.get('next')  # Redirect to the next page if available
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            logger.warning('Failed login attempt for user: %s', form.email.data)
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    """
    Logs out the current user.
    
    Logs the logout action.
    """
    logger.info('User logged out: %s', current_user.username)
    logout_user()
    return redirect(url_for('home'))

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """
    Handles the creation of a new post.
    
    Validates the post form and saves the post if valid.
    Logs the creation of the post.
    """
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
    """
    Handles the user's account update.
    
    Validates the update account form and updates the user's information if valid.
    Logs the account update.
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)  # Save the uploaded picture
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
