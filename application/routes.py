from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import boto3
import os
import time

from . import db
from .forms import RegistrationForm, LoginForm, PostForm
from .models import User, Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        image_file = save_picture(request.files['file'])
        post = Post(image_file=image_file, caption=form.caption.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form)

def save_picture(form_picture):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = secure_filename(f"{current_user.username}_{int(time.time())}{f_ext}")
    s3 = boto3.client('s3', region_name=os.getenv('AWS_REGION'), 
                      aws_access_key_id=os.getenv('S3_KEY'), 
                      aws_secret_access_key=os.getenv('S3_SECRET'))
    s3.upload_fileobj(form_picture, os.getenv('S3_BUCKET'), picture_fn)
    return f"{os.getenv('S3_LOCATION')}{picture_fn}"
