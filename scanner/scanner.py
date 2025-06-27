import requests
from bs4 import BeautifulSoup
import re

XSS_PAYLOADS = ["<script>alert(1)</script>", "'><img src=x onerror=alert(1)>"]
SQLI_PAYLOADS = ["' OR '1'='1", "'; DROP TABLE users; --"]
CSRF_TOKENS = ["csrf", "token", "authenticity_token"]

def crawl(url):
    urls = set()
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        for tag in soup.find_all("a", href=True):
            link = tag["href"]
            if link.startswith("/"):
                link = url + link
            if url in link:
                urls.add(link)
    except:
        pass
    return urls

def scan_xss(url):
    found = []
    for payload in XSS_PAYLOADS:
        res = requests.get(url, params={"q": payload})
        if payload in res.text:
            found.append((url, payload))
    return found

def scan_sqli(url):
    found = []
    for payload in SQLI_PAYLOADS:
        res = requests.get(url, params={"q": payload})
        if "sql" in res.text.lower() or "error" in res.text.lower():
            found.append((url, payload))
    return found

def scan_csrf(html):
    for token in CSRF_TOKENS:
        if token in html.lower():
            return True
    return False
