from flask import Flask, render_template, Response, url_for, redirect, abort
import os

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

# --- Maxim ---------------------------------------------------------------------
# /maxim is the design-essay side of Maxim (the "why"). Reference docs, install,
# CLI, and the evidence ledger are canonical on https://pymaxim.bio; reference
# pages that used to live here 301 there (see RETIRED_MAXIM_PAGES below).
#
# Wiring a new essay: route here, an entry in `pages` in sitemap_xml, a card on
# the /maxim hub, and a row in `maxim_pages` in templates/_maxim_related.html.

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

@app.route("/maxim/math-cognition")
def maxim_math_cognition():
    return render_template("maxim-math-cognition.html")

@app.route("/maxim/embodiment")
def maxim_embodiment():
    return render_template("maxim-embodiment.html")

@app.route("/maxim/sound-orientation")
def maxim_sound_orientation():
    return render_template("maxim-sound-orientation.html")

@app.route("/maxim/imagination")
def maxim_imagination():
    return render_template("maxim-imagination.html")

@app.route("/maxim/hivemind")
def maxim_hivemind():
    return render_template("maxim-hivemind.html")

@app.route("/maxim/substrate-primary")
def maxim_substrate_primary():
    return render_template("maxim-substrate-primary.html")

@app.route("/maxim/deliberation")
def maxim_deliberation():
    return render_template("maxim-deliberation.html")

@app.route("/maxim/release-1-0")
def maxim_release_1_0():
    return render_template("maxim-1-0-release.html")

@app.route("/maxim/privacy-policy")
def maxim_privacy_policy():
    return render_template("maxim-privacy-policy.html")

@app.route("/maxim/terms-and-conditions")
def maxim_terms_and_conditions():
    return render_template("maxim-terms-and-conditions.html")

# --- Maxim redirects -------------------------------------------------------------
PYMAXIM_DOCS = "https://pymaxim.bio"
MAXIM_GITHUB = "https://github.com/dennys246/Maxim"

# Reference pages retired from this site on 2026-08-26 in favour of their
# pymaxim.bio counterpart. Keep these forever: the old URLs are in search
# results, the pymaxim README, and pymaxim.bio's own markdown.
RETIRED_MAXIM_PAGES = {
    "usage-guide": PYMAXIM_DOCS + "/installation/",
    "tools": PYMAXIM_DOCS + "/reference/tools/",
    "simulation": PYMAXIM_DOCS + "/guides/simulation/",
    "networking": PYMAXIM_DOCS + "/guides/networking/",
    "agent-mesh": PYMAXIM_DOCS + "/guides/networking/",
    "operating-modes": PYMAXIM_DOCS + "/concepts/operating-modes/",
    "communication": PYMAXIM_DOCS + "/concepts/communication/",
    "technical-deepdive": PYMAXIM_DOCS + "/concepts/architecture/",
    "experiments": PYMAXIM_DOCS + "/research/experiments/",
    "roadmap": MAXIM_GITHUB + "/tree/main/docs/plans",
    # Retired once pymaxim.bio gained pages for them (maxim-web #10).
    "dm-campaigns": PYMAXIM_DOCS + "/guides/dm-campaigns/",
    "benchmarks": PYMAXIM_DOCS + "/guides/benchmarks/",
    "prompt-system": PYMAXIM_DOCS + "/concepts/prompt-system/",
    "concept-decomposition": PYMAXIM_DOCS + "/systems/concept-decomposition/",
    "component-library": PYMAXIM_DOCS + "/reference/components/",
}

# Essays folded into another essay (2026-08-26). Fragment survives the 301.
MOVED_MAXIM_PAGES = {
    "semantic-memory": "/maxim/memory-systems#semantic",
}

# Essays still served here. Used to normalise `/maxim/<slug>.html` and
# `/maxim/<slug>/` variants back onto the canonical URL.
MAXIM_ESSAY_SLUGS = (
    "release-1-0", "sound-orientation", "substrate-primary", "hivemind",
    "agent-architecture", "math-cognition", "memory-systems", "embodiment",
    "imagination", "proprioception", "attention-salience", "deliberation",
    "privacy-policy", "terms-and-conditions",
)

# The pymaxim 1.0.9 README (immutable on PyPI) and the repo's docs/index.md link
# to /maxim/maxim-<slug> URLs that never existed here. Each one lands on the best
# current home: the essay if it's still served, the pymaxim.bio page if it isn't.
LEGACY_MAXIM_REDIRECTS = {
    "maxim-overview": "/maxim",
    "maxim-1-0-release": "/maxim/release-1-0",
}
for _slug in MAXIM_ESSAY_SLUGS:
    LEGACY_MAXIM_REDIRECTS.setdefault("maxim-" + _slug, "/maxim/" + _slug)
for _slug, _target in {**RETIRED_MAXIM_PAGES, **MOVED_MAXIM_PAGES}.items():
    LEGACY_MAXIM_REDIRECTS["maxim-" + _slug] = _target


def _maxim_redirect_target(slug):
    """Resolve any non-canonical /maxim/<slug> variant, or None to 404."""
    key = slug.strip("/")
    if key.endswith(".html"):
        key = key[:-5]
    if key in RETIRED_MAXIM_PAGES:
        return RETIRED_MAXIM_PAGES[key]
    if key in MOVED_MAXIM_PAGES:
        return MOVED_MAXIM_PAGES[key]
    if key in MAXIM_ESSAY_SLUGS:
        return "/maxim/" + key
    return LEGACY_MAXIM_REDIRECTS.get(key)


@app.route("/maxim/<path:slug>", strict_slashes=False)
def maxim_legacy_redirect(slug):
    # Exact essay routes above win over this rule, so only variants land here:
    # retired slugs, legacy maxim-* slugs, and .html / trailing-slash forms.
    target = _maxim_redirect_target(slug)
    if target is None:
        abort(404)
    return redirect(target, code=301)

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
    # (endpoint, changefreq, priority, lastmod). Bump lastmod when you edit a page;
    # it used to be stamped "today" on every crawl, which told crawlers nothing.
    pages = [
        ("main", "weekly", "1.0", "2026-07-16"),
        ("story", "monthly", "0.8", "2026-09-02"),
        ("experiences", "monthly", "0.8", "2026-09-02"),
        ("achievements", "monthly", "0.8", "2026-01-06"),
        ("papers", "monthly", "0.8", "2026-09-02"),
        ("projects", "monthly", "0.8", "2026-07-16"),
        ("ramblings", "monthly", "0.7", "2026-08-26"),
        ("contact", "monthly", "0.6", "2025-11-29"),
        ("perceptrons", "monthly", "0.6", "2025-11-22"),
        # Maxim — design essays (docs and evidence are on pymaxim.bio)
        ("maxim", "monthly", "0.9", "2026-08-26"),
        ("maxim_release_1_0", "monthly", "0.8", "2026-08-26"),
        ("maxim_sound_orientation", "monthly", "0.8", "2026-08-26"),
        ("maxim_substrate_primary", "monthly", "0.8", "2026-08-26"),
        ("maxim_hivemind", "monthly", "0.8", "2026-08-26"),
        ("maxim_agent_architecture", "monthly", "0.8", "2026-08-26"),
        ("maxim_math_cognition", "monthly", "0.8", "2026-08-26"),
        ("maxim_memory_systems", "monthly", "0.8", "2026-08-26"),
        ("maxim_embodiment", "monthly", "0.8", "2026-08-26"),
        ("maxim_imagination", "monthly", "0.7", "2026-08-26"),
        ("maxim_proprioception", "monthly", "0.7", "2026-08-26"),
        ("maxim_attention_salience", "monthly", "0.7", "2026-08-26"),
        ("maxim_deliberation", "monthly", "0.7", "2026-08-26"),
        ("maxim_privacy_policy", "yearly", "0.3", "2026-06-03"),
        ("maxim_terms_and_conditions", "yearly", "0.3", "2026-06-03"),
        ("gan_training_tips", "monthly", "0.6", "2026-02-08"),
        ("progressive_growing", "monthly", "0.6", "2026-02-08"),
    ]

    url_entries = []
    for endpoint, changefreq, priority, lastmod in pages:
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
