import hmac

def safe_str_cmp(a, b):
    """Perform a constant time string comparison."""
    return hmac.compare_digest(a, b)
