# Mortice & Tenon website

Static site for Mortice & Tenon (self-drilling zip drywall anchors and Easy Anchor toggle anchors). It is plain HTML and CSS, with no framework, no build step and no JavaScript. The only script is a 1-line inline one in `404.html`.

- **Preview:** https://jeclass.github.io/mortice-tenon-site/ (GitHub Pages, `main` branch, `/docs` folder)
- **Future domain:** https://morticeandtenon.us. It still points to Base44. See `SWITCH-PLAN.md` before changing anything.
- **Claims and image sources:** `SOURCES.md`. Every fact on the site must trace to a source listed there.

## Layout

```
docs/                    ← the published site (GitHub Pages serves this folder)
  index.html             Home
  products/index.html    Both lines, 8 pack cards with Amazon links
  install/index.html     Install steps (exact label wording) + how to choose a pack
  wholesale/index.html   Quote request (mailto) + ASIN/UPC tables + line card
  about/ contact/ privacy/
  404.html               Sets <base> with an inline script so it works at any depth
  assets/css/site.css    All styles (colours, fonts, layout)
  assets/fonts/          Arvo Bold + Outfit (OFL; licence files alongside)
  assets/img/            WebP images, logo SVGs, OG card
  downloads/             mortice-and-tenon-line-card.pdf
  robots.txt sitemap.xml favicon.* apple-touch-icon.png .nojekyll
tools/
  build_assets.py        Rebuilds images, logo, favicons, fonts from the source files
  linecard.html          Source of the line-card PDF
  make_linecard.sh       Prints linecard.html to docs/downloads/…pdf
  serve.py               Local server that mimics GitHub Pages (subpath + 404.html)
  screenshots.mjs        Full-page screenshots (1440 + 390 px) of every page → _review/
_review/                 Screenshots (git-ignored)
```

## Editing rules

- **Links are relative** (`../products/`), so the site works both at `/mortice-tenon-site/` and at the domain root. Never use root-absolute paths like `/assets/...`, except in `404.html`, which uses `<base>`.
- **The header and footer are repeated in every page.** To change navigation, edit all 8 HTML files. Use `grep -l 'site-nav' docs -r` to find them.
- **No prices, ratings, review counts or sales numbers.** They change or can't be proved. No trackers, cookies, forms or third-party embeds, because the privacy policy promises none. The one planned exception is a Google Form for quotes: the slot is marked `RFQ FORM SLOT` in `docs/wholesale/index.html`. If you add it, update `privacy/index.html`.
- **Hold ratings and install steps must match the pack labels word for word** (see `SOURCES.md`).
- **Images:** use only our own images, WebP, each ≤ 200 KB. Add them via `tools/build_assets.py` so they can be rebuilt.
- **Absolute URLs** (canonical, og:url, og:image, sitemap, robots) already point at `https://morticeandtenon.us/`.

## Common tasks

```bash
# Preview locally (http://127.0.0.1:8765/mortice-tenon-site/)
python3 tools/serve.py

# Screenshots of every page (needs the local server running; uses Chrome on port 9333)
node tools/screenshots.mjs

# Lighthouse (mobile) on a page
CHROME_PATH=/usr/bin/google-chrome npx -y lighthouse@12 https://jeclass.github.io/mortice-tenon-site/ \
  --chrome-flags="--headless=new" --only-categories=performance,accessibility,best-practices,seo

# Rebuild images/fonts/logo, or the line card (build venv: ~/.local/share/mtsite-venv
# with pillow, fonttools, brotli, pymupdf)
~/.local/share/mtsite-venv/bin/python tools/build_assets.py
tools/make_linecard.sh

# Deploy = commit and push to main; Pages rebuilds in ~1 minute
git add -A && git commit -m "…" && git push
```

## What must never be in this repo

This repo is public. Never commit secrets or credentials, customer data, or legal/tax/loan documents. Never commit prices or cost data.
