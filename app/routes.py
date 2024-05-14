from flask import current_app
from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import db, photos
from app.models import User, Post, Comment
from app.forms import RegistrationForm, LoginForm, CommentForm

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts, comment_form=CommentForm())

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

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'photo' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)
    file = request.files['photo']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = photos.save(file)
        url = photos.url(filename)
        new_post = Post(body=request.form['body'], image_url=url, author=current_user)
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Your post has been uploaded successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while uploading your post.', 'error')
            current_app.logger.error(f'Error uploading post: {e}')
    else:
        flash('Invalid file type.', 'error')
    return redirect(url_for('main.index'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
