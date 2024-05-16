from flask import current_app, render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import User, Post, Comment
from app.forms import RegistrationForm, LoginForm, CommentForm

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts, comment_form=CommentForm())

@main.route('/create_post', methods=['POST'])
@login_required
def create_post():
    post_body = request.form.get('post_body')
    if post_body:
        post = Post(body=post_body, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
    else:
        flash('Post content cannot be empty.', 'error')
    return redirect(url_for('main.index'))

@main.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(body=form.body.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added.', 'success')
        return redirect(url_for('main.post', post_id=post_id))
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.desc()).all()
    return render_template('post.html', post=post, comments=comments, form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next') or url_for('main.index')
            return redirect(next_page)
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html', title='Sign In', form=form)

@main.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/upload/<int:post_id>', methods=['POST'])
@login_required
def upload(post_id):
    post = Post.query.get_or_404(post_id)
    if 'file' not in request.files:
        flash('No file part found. Please select a file.', 'error')
        return redirect(url_for('main.post', post_id=post_id))
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        flash('Your file has been uploaded successfully!', 'success')
    else:
        flash('No file selected or invalid file type.', 'error')
    return redirect(url_for('main.post', post_id=post_id))

@main.route('/profile/<username>', methods=['GET'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
