from core.requester import Requester
from payloads.xss import payloads

class ReflectedXSS:
    def __init__(self, url):
        self.url = url
        self.requester = Requester()

    def scan(self):
        print("[*] Starting XSS scan...")

        for payload in payloads:
            test_url = f"{self.url}?q={payload}"
            
            response = self.requester.get(test_url)

            if response and payload in response.text:
                print(f"[VULNERABLE] XSS Found with payload: {payload}")
                return

        print("[+] No XSS found")