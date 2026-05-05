import re
from core.parser import Parser
from core.requester import Requester
from payloads.xss import payloads


class Scanner:
    def __init__(self, url, scan_type):
        self.url = url
        self.scan_type = scan_type
        self.parser = Parser(url)
        self.requester = Requester()

    # =========================
    # Context Detection Engine
    # =========================
    def detect_context(self, payload, response_text):

        if payload not in response_text:
            return None

        # SCRIPT context
        script_pattern = rf"<script[^>]*>.*{re.escape(payload)}.*</script>"
        if re.search(script_pattern, response_text, re.IGNORECASE | re.DOTALL):
            return "script"

        # ATTRIBUTE context
        attr_pattern = rf"=\s*['\"][^'\"]*{re.escape(payload)}[^'\"]*['\"]"
        if re.search(attr_pattern, response_text):
            return "attribute"

        # HTML context
        return "html"

    # =========================
    # Risk Scoring Engine
    # =========================
    def get_risk_level(self, context):
        if context == "script":
            return "HIGH"
        elif context == "attribute":
            return "MEDIUM"
        elif context == "html":
            return "LOW"
        return "NONE"

    # =========================
    # Form Testing
    # =========================
    def test_form(self, form):
        for input_field in form["inputs"]:
            name = input_field["name"]

            for payload in payloads:
                data = {name: payload}

                if form["method"] == "get":
                    response = self.requester.get(form["action"], params=data)
                else:
                    response = self.requester.session.post(form["action"], data=data)

                if response:
                    context = self.detect_context(payload, response.text)

                    if context:
                        risk = self.get_risk_level(context)
                        print(f"[{risk}] XSS in {name} ({context}) -> {payload}")
                        return

        print("[+] Form not vulnerable")

    # =========================
    # URL Parameter Testing
    # =========================
    def scan_url_params(self, url_data):
        url = url_data["url"]
        params = url_data["params"]

        for param_name in params.keys():
            for payload in payloads:
                test_url = url.replace(str(params[param_name][0]), payload)

                response = self.requester.get(test_url)

                if response:
                    context = self.detect_context(payload, response.text)

                    if context:
                        risk = self.get_risk_level(context)
                        print(f"[{risk}] XSS in {param_name} ({context}) -> {url}")
                        return

        print("[+] URL not vulnerable")

    # =========================
    # Main Engine
    # =========================
    def run(self):
        print("[*] Starting scan...")

        forms = self.parser.get_forms()
        urls = self.parser.get_urls_with_params()

        print(f"[+] Found {len(forms)} forms")
        print(f"[+] Found {len(urls)} URLs with parameters")

        for form in forms:
            self.test_form(form)

        for url_data in urls:
            self.scan_url_params(url_data)