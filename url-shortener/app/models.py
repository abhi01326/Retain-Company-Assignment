# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata

import threading
from datetime import datetime

lock = threading.Lock()
url_map = {}
click_counts = {}
timestamps = {}

def save_url(short_code, original_url):
    with lock:
        url_map[short_code] = original_url
        click_counts[short_code] = 0
        timestamps[short_code] = datetime.utcnow()

def get_url(short_code):
    return url_map.get(short_code)

def increment_click(short_code):
    with lock:
        if short_code in click_counts:
            click_counts[short_code] += 1

def get_stats(short_code):
    if short_code in url_map:
        return {
            "url": url_map[short_code],
            "clicks": click_counts[short_code],
            "created_at": timestamps[short_code].isoformat()
        }
    return None
