# tuliohf.github.io

Personal academic website of Tulio Honorio, published at https://tuliohf.github.io.

## How to update the content

Everything you normally change is in `_data/`. You can edit these files directly on GitHub; the site rebuilds by itself within a minute or two after each commit.

| File | What it holds |
|---|---|
| `_data/site.yml` | Name, bio, email, profile links, key numbers, news |
| `_data/projects.yml` | Ongoing projects (home cards + Research page) |
| `_data/publications.yml` | All publications. `selected: true` puts a paper in "Selected" |
| `_data/team.yml` | Advisees. Fill `now:` with where former members went |
| `_data/cv.yml` | Positions, funding, talks, awards, teaching, committees, reviewing |
| `_data/code.yml` | Repositories and datasets |

**Project figures.** Put an image in `assets/img/projects/` (e.g. `asr.jpg`, about 1600×1000 px) and set `image: assets/img/projects/asr.jpg` in `projects.yml`. While `image` is empty, a placeholder is shown.

**CV.** Upload the new PDF to `files/` and update `cv_pdf:` in `site.yml`.

**Add a paper.** Copy an entry at the top of `publications.yml` and change the fields. Use `status: under review`, `under revision`, `in press` or `published`.

## Build locally (optional)

```bash
pip install jinja2 pyyaml
python build.py --serve   # then open http://localhost:8000
```

## One-time setup on GitHub

Settings → Pages → Build and deployment → Source: **GitHub Actions**.

Layout: `templates/` (page layouts), `assets/css/style.css` (design), `build.py` (builder), `.github/workflows/pages.yml` (deployment).
