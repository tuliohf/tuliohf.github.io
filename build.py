#!/usr/bin/env python3
"""Build the website into _site/.

    pip install jinja2 pyyaml
    python build.py            # build
    python build.py --serve    # build and serve on http://localhost:8000

Content lives in _data/*.yml; page layouts in templates/*.html.
"""
import re
import shutil
import sys
from collections import OrderedDict
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

ROOT = Path(__file__).parent
OUT = ROOT / "_site"
PAGES = {
    "index.html": "Home",
    "research.html": "Research",
    "publications.html": "Publications",
    "team.html": "Team",
    "code.html": "Code & Data",
    "service.html": "Service",
    "cv.html": "CV",
    "contact.html": "Contact",
}
NAV = ["research.html", "publications.html", "team.html", "code.html", "service.html", "cv.html", "contact.html"]


def load(name):
    return yaml.safe_load((ROOT / "_data" / f"{name}.yml").read_text(encoding="utf-8")) or []


def fmt_authors(s):
    """Bold the site owner, turn trainee markers (#, *, **, ***) into superscripts."""
    out = []
    for a in [x.strip() for x in s.split(";") if x.strip()]:
        m = re.match(r"^(.*?)([#*]+)$", a.replace("*.", "*"))
        name, mark = (m.group(1).strip(), m.group(2)) if m else (a, "")
        h = escape(name)
        if re.match(r"Hon[oó]rio", name):
            h = Markup(f'<span class="me">{h}</span>')
        if mark:
            h = Markup(f'{h}<sup class="mark" title="{MARKS.get(mark, "")}">{escape(mark)}</sup>')
        out.append(str(h))
    return Markup("; ".join(out))


MARKS = {"#": "Postdoc", "*": "PhD student", "**": "Master student", "***": "Undergraduate student"}


def main():
    site = load("site")
    pubs = load("publications")
    for p in pubs:
        p.setdefault("status", "published")
    by_id = {p["id"]: p for p in pubs}
    projects = load("projects")
    for pr in projects:
        pr["paper_objs"] = [by_id[i] for i in pr.get("papers", []) if i in by_id]
    pos = {"Å": 0, "nm": 10, "µm": 40, "mm": 70, "m": 100}  # log10 position, 1e-10 m → 1 m
    for pr in projects:
        a, b = [x.strip() for x in pr.get("scale", "nm → nm").split("→")]
        pr["span"] = (pos.get(a, 0), pos.get(b, 0))
    team = load("team")
    cv = load("cv")
    code = load("code")
    for c in code:
        c["paper_objs"] = [by_id[i] for i in c.get("papers", []) if i in by_id]

    journal = [p for p in pubs if p["type"] == "journal"]
    published = [p for p in journal if p["status"] in ("published", "in press")]
    pending = [p for p in journal if p["status"] in ("under review", "under revision")]
    years = OrderedDict()
    for p in sorted(published, key=lambda p: (-(p.get("year") or 0), -int(p["id"][1:]))):
        years.setdefault(p["year"], []).append(p)

    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=select_autoescape(["html"]))
    env.filters["authors"] = fmt_authors
    ctx = dict(
        site=site, pubs=pubs, projects=projects, team=team, cv=cv, code=code,
        recent=sorted(published, key=lambda p: -int(p["id"][1:]))[:5],
        selected=[p for p in journal if p.get("selected")],
        years=years, pending=pending,
        chapters=[p for p in pubs if p["type"] == "chapter"],
        theses=[p for p in pubs if p["type"] == "thesis"],
        n_journal=len(published), marks=MARKS,
        nav=[(f, PAGES[f]) for f in NAV],
    )

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for page, title in PAGES.items():
        html = env.get_template(page).render(page=page, title=title, **ctx)
        (OUT / page).write_text(html, encoding="utf-8")
    shutil.copytree(ROOT / "assets", OUT / "assets")
    for f in (ROOT / "files").iterdir():  # CV PDFs etc., served from the site root
        shutil.copy(f, OUT / f.name)
    (OUT / ".nojekyll").write_text("")
    print(f"Built {len(PAGES)} pages into {OUT}")


if __name__ == "__main__":
    main()
    if "--serve" in sys.argv:
        import functools, http.server
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        print("Serving on http://localhost:8000")
        http.server.ThreadingHTTPServer(("", 8000), handler).serve_forever()
