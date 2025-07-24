import threading
from datetime import datetime

class URLStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.data = {}  # short_code: {url, created_at, clicks}

    def add(self, short_code, url):
        with self.lock:
            self.data[short_code] = {
                "url": url,
                "created_at": datetime.utcnow().isoformat(),
                "clicks": 0
            }

    def get(self, short_code):
        with self.lock:
            return self.data.get(short_code)

    def increment_clicks(self, short_code):
        with self.lock:
            if short_code in self.data:
                self.data[short_code]["clicks"] += 1
                return True
            return False

# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata