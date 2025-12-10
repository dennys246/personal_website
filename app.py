from flask import Flask, render_template, Response, url_for
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/story")
def story():
    return render_template("story.html")

@app.route("/experiences")
def experiences():
    return render_template("experiences.html")

@app.route("/achievements")
def achievements():
    return render_template("achievements.html")

@app.route("/papers")
def papers():
    return render_template("papers.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/ramblings")
def ramblings():
    return render_template("ramblings.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/perceptrons")
def perceptrons():
    return render_template("perceptrons.html")


@app.route("/robots.txt")
def robots_txt():
    sitemap_url = url_for("sitemap_xml", _external=True)
    content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            f"Sitemap: {sitemap_url}",
        ]
    )
    return Response(content, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap_xml():
    pages = [
        ("main", "weekly", "1.0"),
        ("story", "monthly", "0.8"),
        ("experiences", "monthly", "0.8"),
        ("achievements", "monthly", "0.8"),
        ("papers", "monthly", "0.8"),
        ("projects", "monthly", "0.8"),
        ("ramblings", "monthly", "0.6"),
        ("contact", "monthly", "0.6"),
        ("perceptrons", "monthly", "0.6"),
    ]

    lastmod = datetime.utcnow().date().isoformat()
    url_entries = []
    for endpoint, changefreq, priority in pages:
        loc = url_for(endpoint, _external=True)
        url_entries.append(
            f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""
        )

    xml_content = "\n".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            *url_entries,
            "</urlset>",
        ]
    )
    return Response(xml_content, mimetype="application/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
