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
    
    This function loads a user by their user_id. It is used by Flask-Login to manage
    user sessions.
    
    Args:
        user_id (int): The ID of the user to load.
    
    Returns:
        User: The user object corresponding to the given user ID.
    """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    User model representing a user in the application.
    
    Attributes:
        id (int): The primary key for the user.
        username (str): The username of the user, unique and not nullable.
        email (str): The email of the user, unique and not nullable.
        image_file (str): The filename of the user's profile image, with a default value.
        password (str): The hashed password of the user.
        posts (list): A list of posts authored by the user.
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
        
        Args:
            kwargs: The keyword arguments to initialize the user attributes.
        
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
        
        Args:
            kwargs: The keyword arguments to update the user attributes.
        
        Logs the update operation.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        logger.info(f"User updated: {self.username}")

class Post(db.Model):
    """
    Post model representing a blog post in the application.
    
    Attributes:
        id (int): The primary key for the post.
        title (str): The title of the post, not nullable.
        date_posted (datetime): The date and time the post was created, with a default value.
        content (str): The content of the post, not nullable.
        user_id (int): The ID of the user who authored the post, foreign key to the User model.
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
        
        Args:
            kwargs: The keyword arguments to initialize the post attributes.
        
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
        
        Args:
            kwargs: The keyword arguments to update the post attributes.
        
        Logs the update operation.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        logger.info(f"Post updated: {self.title}")
