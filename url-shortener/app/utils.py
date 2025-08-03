# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need

import random
import string
import re

def is_valid_url(url):
    """Check if the provided URL is valid."""
    pattern = re.compile(
        r'^(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/\S*)?$'
    )
    return bool(pattern.match(url))
def generate_short_code(length=6):
    """Generate a random short code of specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
