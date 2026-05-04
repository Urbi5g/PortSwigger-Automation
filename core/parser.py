import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

class Parser:
    def __init__(self, url):
        self.url = url

    # =========================
    # FORM PARSER (قديم)
    # =========================
    def get_forms(self):
        try:
            response = requests.get(self.url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            forms = soup.find_all("form")
            form_details = []

            for form in forms:
                action = form.get("action")
                method = form.get("method", "get").lower()

                inputs = []
                for input_tag in form.find_all("input"):
                    input_name = input_tag.get("name")
                    input_type = input_tag.get("type", "text")

                    if input_name:
                        inputs.append({
                            "name": input_name,
                            "type": input_type
                        })

                form_details.append({
                    "action": urljoin(self.url, action),
                    "method": method,
                    "inputs": inputs
                })

            return form_details

        except Exception as e:
            print(f"[PARSER ERROR] {e}")
            return []

    # =========================
    # URL PARAMETER PARSER (جديد 🔥)
    # =========================
    def get_urls_with_params(self):
        try:
            response = requests.get(self.url, timeout=20)
            soup = BeautifulSoup(response.text, "html.parser")

            links = soup.find_all("a")

            params_list = []

            for link in links:
                href = link.get("href")

                if not href:
                    continue

                full_url = urljoin(self.url, href)
                parsed = urlparse(full_url)

                params = parse_qs(parsed.query)

                if params:
                    params_list.append({
                        "url": full_url,
                        "params": params
                    })

            return params_list

        except Exception as e:
            print(f"[PARSER ERROR] {e}")
            return []