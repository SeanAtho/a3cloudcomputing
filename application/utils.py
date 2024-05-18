import hashlib
import hmac
import os

def safe_str_cmp(a, b):
    """Perform a constant time string comparison."""
    return hmac.compare_digest(a, b)

def hash_password(password):
    """Hash a password for storing."""
    salt = os.urandom(16)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + pwdhash

def check_password(stored_password, provided_password):
    """Verify a stored password against one provided by user."""
    salt = stored_password[:16]
    stored_pwdhash = stored_password[16:]
    pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return hmac.compare_digest(stored_pwdhash, pwdhash)
