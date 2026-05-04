# PortSwigger SQL Injection Automation

## Description
This Python script automates the **SQL Injection (Login Bypass)** vulnerability found in PortSwigger's Web Security Academy. It demonstrates how to programmatically bypass authentication by injecting a payload into the username field.

## Features
* **CSRF Token Handling:** Automatically extracts the CSRF token from the login page to maintain session integrity.
* **Session Management:** Uses `requests.Session()` to handle cookies and redirects.
* **Command-line Arguments:** Accepts any Lab URL as an input, making it reusable.

## How it Works
1. Fetches the `/login` page.
2. Parses the HTML to find the hidden `csrf` input value.
3. Sends a POST request with the payload `administrator'--`.
4. Validates success by checking for the "Log out" string in the response.

## Usage
```bash
python sqli_login_bypass.py "<LAB_URL>"