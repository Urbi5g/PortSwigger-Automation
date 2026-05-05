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

            if response:

    content = response.text

    # الحالة 1: encoded (آمن)
    encoded = payload.replace("<", "&lt;").replace(">", "&gt;")

    if encoded in content:
        print(f"[SAFE] Payload encoded (no XSS): {payload}")
        continue

    # الحالة 2: reflected
    if payload in content:
        print(f"[REFLECTED] Payload reflected: {payload}")
        continue

    # الحالة 3: غير موجود
    print(f"[OK] Not reflected: {payload}")
                return

        print("[+] No XSS found")
