"""Crawl the sitemap with Flask's test client and fail on anything broken.

Run from the repo root inside a venv that has requirements.txt installed:

    ./venv/bin/python check_site.py

Checks: every sitemap URL renders 200, every internal href resolves (and its
#fragment exists on the target page), every JSON-LD block parses, and the
Maxim redirect variants land where they should.
"""
import json
import re
import sys

from app import app

c = app.test_client()
sitemap = c.get("/sitemap.xml").get_data(as_text=True)
locs = re.findall(r"<loc>http://localhost(/[^<]*)</loc>", sitemap)

pages = {}
problems = []
for p in locs:
    r = c.get(p)
    if r.status_code != 200:
        problems.append((p, "sitemap page", r.status_code))
        continue
    pages[p] = r.get_data(as_text=True)
    for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>', pages[p], re.S):
        try:
            json.loads(blob)
        except ValueError as e:
            problems.append((p, "json-ld", str(e)))

ids = {p: set(re.findall(r'id="([^"]+)"', h)) for p, h in pages.items()}
for p, h in pages.items():
    for href in set(re.findall(r'href="([^"]+)"', h)):
        if href.startswith(("http", "mailto:", "tel:")):
            continue
        path, _, frag = href.partition("#")
        if path.startswith("/static/"):
            continue
        target = path or p
        if target not in pages:
            if c.get(target).status_code != 200:
                problems.append((p, href, "broken link"))
        elif frag and frag not in ids[target]:
            problems.append((p, href, "missing id"))

REDIRECTS = {
    "/maxim/maxim-overview": "/maxim",
    "/maxim/maxim-overview.html": "/maxim",
    "/maxim/memory-systems/": "/maxim/memory-systems",
    "/maxim/semantic-memory": "/maxim/memory-systems#semantic",
    "/maxim/usage-guide": "https://pymaxim.bio/installation/",
}
for src, dst in REDIRECTS.items():
    r = c.get(src)
    if r.status_code != 301 or r.headers.get("Location") != dst:
        problems.append((src, "redirect", f"{r.status_code} {r.headers.get('Location')}"))
if c.get("/maxim/does-not-exist").status_code != 404:
    problems.append(("/maxim/does-not-exist", "redirect", "expected 404"))

print(f"{len(pages)} pages, {len(REDIRECTS)} redirects checked")
if problems:
    for item in problems:
        print("  PROBLEM:", *item)
    sys.exit(1)
print("OK")
