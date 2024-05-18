import hmac
from werkzeug.security import generate_password_hash, check_password_hash

def safe_str_cmp(a, b):
    """Perform a constant time string comparison."""
    return hmac.compare_digest(a, b)

def hash_password(password):
    """Hash a password for storing."""
    return generate_password_hash(password)

def check_password(hashed_password, password):
    """Verify a stored password against one provided by user."""
    return check_password_hash(hashed_password, password)
