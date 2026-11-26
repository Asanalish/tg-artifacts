#!/usr/bin/env python3
"""Add (or update) an artifact page in the Mini App site.

Usage:
  python3 add_page.py <slug> <file.html> "<Title>" "<short description>" [--header "#1240e0"]

  slug  latin letters, digits, _ or - (Telegram's startapp limit). It becomes
        the folder name and the link: t.me/<bot>/<app>?startapp=<slug>

The script copies the page to <slug>/index.html, plugs in the Telegram script
and tg.js, and records the page in pages.json (the hub reads it).
Running it again with the same slug replaces the page; the channel link stays.
"""
import json, re, sys, argparse, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
TG = ('<script src="https://telegram.org/js/telegram-web-app.js"></script>\n'
      '<script src="../tg.js"></script>\n')

ap = argparse.ArgumentParser()
ap.add_argument('slug'); ap.add_argument('src'); ap.add_argument('title'); ap.add_argument('desc')
ap.add_argument('--header', help='Telegram top bar colour, e.g. #1240e0')
ap.add_argument('--bg-light', default='#ffffff'); ap.add_argument('--bg-dark', default='#0a0d18')
a = ap.parse_args()

if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', a.slug):
    sys.exit('slug: only A-Z a-z 0-9 _ -')

html = pathlib.Path(a.src).read_text(encoding='utf-8')
html = html.replace(TG, '')  # re-running on an already patched file

# 1. Telegram scripts right after the viewport meta (or <head>)
m = re.search(r'<meta[^>]+name=["\']viewport["\'][^>]*>\s*', html, re.I) or re.search(r'<head[^>]*>\s*', html, re.I)
if not m:
    sys.exit('no <head> in the page')
html = html[:m.end()] + TG + html[m.end():]

# 2. colours for Telegram's chrome, as attributes on <html>
attrs = f' data-tg-bg-light="{a.bg_light}" data-tg-bg-dark="{a.bg_dark}"'
if a.header:
    attrs += f' data-tg-header="{a.header}"'
html = re.sub(r'\s+data-tg-(?:bg-light|bg-dark|header)="[^"]*"', '', html)
html = re.sub(r'<html\b', '<html' + attrs, html, count=1, flags=re.I)

# 3. sticky bars must clear Telegram's buttons in fullscreen mode
html = re.sub(r'<nav\b(?![^>]*data-tg-sticky)', '<nav data-tg-sticky', html, flags=re.I)

out = ROOT / a.slug / 'index.html'
out.parent.mkdir(exist_ok=True)
out.write_text(html, encoding='utf-8')

pj = ROOT / 'pages.json'
pages = json.loads(pj.read_text(encoding='utf-8')) if pj.exists() else []
pages = [p for p in pages if p['slug'] != a.slug]
pages.insert(0, {'slug': a.slug, 'title': a.title, 'desc': a.desc})
pj.write_text(json.dumps(pages, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'ok: {out.relative_to(ROOT)}  ({len(pages)} pages in pages.json)')
