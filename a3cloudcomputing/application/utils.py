from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from PIL import Image
from flask import current_app
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def hash_password(password):
    """
    Hash the password using Werkzeug's security module.
    
    Args:
        password (str): The plain text password to hash.
    
    Returns:
        str: The hashed password.
    """
    hashed = generate_password_hash(password)
    logger.info("Password hashed")
    return hashed

def verify_password(stored_password, provided_password):
    """
    Verify the provided password against the stored hashed password.
    
    Args:
        stored_password (str): The hashed password stored in the database.
        provided_password (str): The plain text password provided by the user.
    
    Returns:
        bool: True if the password matches, False otherwise.
    """
    result = check_password_hash(stored_password, provided_password)
    if result:
        logger.info("Password verified successfully")
    else:
        logger.warning("Password verification failed")
    return result

def save_picture(form_picture):
    """
    Save the uploaded picture, resize it to 125x125 pixels, and return the filename.
    
    Args:
        form_picture (FileStorage): The uploaded picture file.
    
    Returns:
        str: The filename of the saved picture.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    # Resize the image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    logger.info(f"Picture saved: {picture_fn}")

    return picture_fn
