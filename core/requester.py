import requests

class Requester:
    def __init__(self):
        self.session = requests.Session()

    def get(self, url, params=None):
        try:
            response = self.session.get(url, params=params, timeout=15)
            return response
        except Exception as e:
            print(f"[ERROR] {e}")
            return None