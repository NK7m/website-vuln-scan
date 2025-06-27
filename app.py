from flask import Flask, render_template, request
from scanner import scanner

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    if request.method == "POST":
        target_url = request.form["url"]
        crawled_urls = scanner.crawl(target_url)
        for url in crawled_urls:
            results.extend(scanner.scan_xss(url))
            results.extend(scanner.scan_sqli(url))
        html = "<html><body></body></html>"
        if scanner.scan_csrf(html):
            results.append(("CSRF token detected", target_url))
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
