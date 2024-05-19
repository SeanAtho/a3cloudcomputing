from datetime import datetime
from application import db, login_manager
from flask_login import UserMixin
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login user loader callback.
    This function loads a user by their user_id.
    """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    User model representing a user in the application.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(255), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __init__(self, **kwargs):
        """
        Initializes a new User instance.
        Logs the creation of the user.
        """
        super(User, self).__init__(**kwargs)
        logger.info(f"User created: {self.username}")

    def save(self):
        """
        Saves the user to the database.
        Logs the save operation.
        """
        db.session.add(self)
        db.session.commit()
        logger.info(f"User saved: {self.username}")

    def update(self, **kwargs):
        """
        Updates the user's attributes with the given keyword arguments.
        Logs the update operation.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        logger.info(f"User updated: {self.username}")

class Post(db.Model):
    """
    Post model representing a blog post in the application.
    """
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, **kwargs):
        """
        Initializes a new Post instance.
        Logs the creation of the post.
        """
        super(Post, self).__init__(**kwargs)
        logger.info(f"Post created: {self.title} by user_id {self.user_id}")

    def save(self):
        """
        Saves the post to the database.
        Logs the save operation.
        """
        db.session.add(self)
        db.session.commit()
        logger.info(f"Post saved: {self.title}")

    def update(self, **kwargs):
        """
        Updates the post's attributes with the given keyword arguments.
        Logs the update operation.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        logger.info(f"Post updated: {self.title}")
