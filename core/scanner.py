from core.parser import Parser
from core.requester import Requester
from payloads.xss import payloads

class Scanner:
    def __init__(self, url, scan_type):
        self.url = url
        self.scan_type = scan_type
        self.parser = Parser(url)
        self.requester = Requester()

    def run(self):
        print("[*] Parsing target...")

        forms = self.parser.get_forms()

        if not forms:
            print("[!] No forms found, fallback to URL injection")
            self.scan_url(self.url)
            return

        print(f"[+] Found {len(forms)} forms")

        for form in forms:
            self.test_form(form)

        url_params = self.parser.get_urls_with_params()

        print(f"[+] Found {len(url_params)} URLs with parameters")

    def test_form(self, form):
        for input_field in form["inputs"]:
            name = input_field["name"]

            for payload in payloads:
                data = {name: payload}

                if form["method"] == "get":
                    response = self.requester.get(form["action"], params=data)
                else:
                    response = self.requester.session.post(form["action"], data=data)

                if response and payload in response.text:
                    print(f"[VULNERABLE] XSS in {name}")
                    return

        print("[+] Form not vulnerable")

    def scan_url_params(self, url_data):
        url = url_data["url"]
        params = url_data["params"]

        for url_data in url_params:
            self.scan_url_params(url_data)

        for param_name in params.keys():
            for payload in payloads:
                test_url = url.replace(str(params[param_name][0]), payload)

                response = self.requester.get(test_url)

                if response and payload in response.text:
                    print(f"[VULNERABLE] XSS in {param_name} -> {url}")
                    return