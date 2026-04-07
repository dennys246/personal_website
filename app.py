from flask import Flask, render_template, Response, url_for, redirect
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

@app.route("/maxim")
def maxim():
    return render_template("maxim-overview.html")

@app.route("/maxim-overview")
def maxim_overview():
    return redirect(url_for("maxim"), code=301)

@app.route("/maxim/memory-systems")
def maxim_memory_systems():
    return render_template("maxim-memory-systems.html")

@app.route("/maxim/proprioception")
def maxim_proprioception():
    return render_template("maxim-proprioception.html")

@app.route("/maxim/attention-salience")
def maxim_attention_salience():
    return render_template("maxim-attention-salience.html")

@app.route("/maxim/agent-architecture")
def maxim_agent_architecture():
    return render_template("maxim-agent-architecture.html")

@app.route("/maxim/technical-deepdive")
def maxim_technical_deepdive():
    return render_template("maxim-technical-deepdive.html")

@app.route("/maxim/operating-modes")
def maxim_operating_modes():
    return render_template("maxim-operating-modes.html")

@app.route("/maxim/usage-guide")
def maxim_usage_guide():
    return render_template("maxim-usage-guide.html")

@app.route("/maxim/communication")
def maxim_communication():
    return render_template("maxim-communication.html")

@app.route("/maxim/math-cognition")
def maxim_math_cognition():
    return render_template("maxim-math-cognition.html")

@app.route("/maxim/semantic-memory")
def maxim_semantic_memory():
    return render_template("maxim-semantic-memory.html")

@app.route("/maxim/tools")
def maxim_tools():
    return render_template("maxim-tools.html")

@app.route("/maxim/simulation")
def maxim_simulation():
    return render_template("maxim-simulation.html")

@app.route("/maxim/benchmarks")
def maxim_benchmarks():
    return render_template("maxim-benchmarks.html")

@app.route("/maxim/embodiment")
def maxim_embodiment():
    return render_template("maxim-embodiment.html")

@app.route("/maxim/networking")
def maxim_networking():
    return render_template("maxim-networking.html")

@app.route("/maxim/roadmap")
def maxim_roadmap():
    return render_template("maxim-roadmap.html")

@app.route("/maxim/privacy-policy")
def maxim_privacy_policy():
    return render_template("maxim-privacy-policy.html")

@app.route("/maxim/terms-and-conditions")
def maxim_terms_and_conditions():
    return render_template("maxim-terms-and-conditions.html")

@app.route("/gan-training-tips")
def gan_training_tips():
    return render_template("gan-training-tips.html")

@app.route("/progressive-growing")
def progressive_growing():
    return render_template("progressive-growing.html")


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
        ("maxim", "weekly", "1.0"),
        ("maxim_agent_architecture", "weekly", "0.9"),
        ("maxim_memory_systems", "weekly", "0.9"),
        ("maxim_attention_salience", "weekly", "0.9"),
        ("maxim_proprioception", "weekly", "0.9"),
        ("maxim_usage_guide", "weekly", "0.9"),
        ("maxim_technical_deepdive", "weekly", "0.9"),
        ("maxim_operating_modes", "weekly", "0.9"),
        ("maxim_communication", "weekly", "0.9"),
        ("maxim_math_cognition", "weekly", "0.9"),
        ("maxim_semantic_memory", "weekly", "0.9"),
        ("maxim_tools", "weekly", "0.9"),
        ("maxim_simulation", "weekly", "0.9"),
        ("maxim_benchmarks", "weekly", "0.9"),
        ("maxim_embodiment", "weekly", "0.9"),
        ("maxim_networking", "weekly", "0.9"),
        ("maxim_roadmap", "monthly", "0.7"),
        ("maxim_privacy_policy", "monthly", "0.5"),
        ("maxim_terms_and_conditions", "monthly", "0.5"),
        ("gan_training_tips", "monthly", "0.6"),
        ("progressive_growing", "monthly", "0.6"),
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
