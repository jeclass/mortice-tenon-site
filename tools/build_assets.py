#!/usr/bin/env python3
"""Build the site's binary assets from Mortice & Tenon's own source files.

Run with the build venv (has pillow, fonttools[woff2]/brotli, pymupdf):
    ~/.local/share/mtsite-venv/bin/python tools/build_assets.py

Inputs live OUTSIDE this repo (OneDrive copy + label work folders); outputs go
into docs/assets/. Re-running overwrites the outputs. Every image used on the
site is either an Amazon listing image we own, our own label art, or our logo.
"""
import os
import pathlib
import shutil
import subprocess

import pymupdf
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

HOME = pathlib.Path.home()
REPO = pathlib.Path(__file__).resolve().parent.parent
OUT = REPO / "docs" / "assets"
MT = HOME / "migration-inbox" / "MORTICE&TENON"
PICS = MT / "Amazon Pics"
LABELS = HOME / "mt-data" / "labels"
FONTS = LABELS / "work" / "fonts"

CREAM = (251, 247, 238)  # #fbf7ee brand cream
MAX_BYTES = 200 * 1024

# Amazon main image for each ASIN (matched pixel-for-pixel to the live listing
# main images on 2026-10-27).
PRODUCTS = {
    "zip-10": PICS / "Zip Anchors/Zip Anchor 10 Pack/ZipSelfDrillingAnchor 10 Hero Image - jpg 1500x1500 px.jpg",
    "zip-25": PICS / "Zip Anchors/Zip Anchor 25 Pack/ZipSelfDrillingAnchor 25 Hero Image - jpg 1500x1500 px.jpg",
    "zip-50": PICS / "Zip Anchors/Zip Anchor 50 Pack/ZipSelfDrillingAnchor 50 Hero Image - jpg 1500x1500px.jpg",
    "zip-100": PICS / "Zip Anchors/updated 100 pack hero.jpg",
    "ea-2": PICS / "New Easy Anchor/ChatGPT Image Jul 17, 2026, 12_26_48 PM.png",
    "ea-5": PICS / "New Easy Anchor/01-02-24 (1).jpg",
    "ea-10": PICS / "New Easy Anchor/01-01-27 (1).jpg",
    "ea-20": PICS / "New Easy Anchor/ChatGPT Image Jul 17, 2026, 01_59_33 PM.png",
}

# Step panels on the approved labels, in PDF points (x0, y0, x1, y1).
STEPS = {
    "zip": (LABELS / "FINAL2-2026-10-13/Zip Anchor 100pk.pdf", [
        (25.2, 114.1, 119.7, 174.9), (137.8, 114.1, 233.1, 174.9),
        (24.1, 200.8, 118.4, 261.4), (136.7, 200.8, 230.9, 261.4)]),
    "ea": (LABELS / "EA-RESIZE-2026-10-27/v2/Easy Anchor 20pk.pdf", [
        (9.4, 103.0, 109.7, 152.7), (118.7, 103.0, 214.5, 152.7),
        (9.4, 180.9, 109.7, 230.6), (118.7, 180.9, 214.5, 230.6)]),
}


def save_webp(im, path, quality=80):
    """Save as WebP, stepping quality down until the file is <= 200 KB."""
    path.parent.mkdir(parents=True, exist_ok=True)
    q = quality
    while True:
        im.save(path, "WEBP", quality=q, method=6)
        if path.stat().st_size <= MAX_BYTES or q <= 40:
            break
        q -= 5
    return path.stat().st_size


def flatten(im, bg=(255, 255, 255)):
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        base = Image.new("RGB", im.size, bg)
        base.paste(im, mask=im.split()[3])
        return base
    return im.convert("RGB")


def square(im, bg=(255, 255, 255)):
    """Pad a non-square image onto a white square (the 20pk main is 1402x1122)."""
    w, h = im.size
    if w == h:
        return im
    s = max(w, h)
    canvas = Image.new("RGB", (s, s), bg)
    canvas.paste(im, ((s - w) // 2, (s - h) // 2))
    return canvas


def build_products():
    for key, src in PRODUCTS.items():
        im = square(flatten(Image.open(src)))
        for width in (360, 720):
            out = OUT / "img" / "products" / f"{key}-{width}.webp"
            size = save_webp(im.resize((width, width), Image.LANCZOS), out)
            print(f"{out.relative_to(REPO)}  {size // 1024} KB")


def build_steps():
    for line, (pdf, rects) in STEPS.items():
        page = pymupdf.open(pdf)[0]
        for i, r in enumerate(rects, 1):
            clip = pymupdf.Rect(*r)
            zoom = 640 / clip.width
            pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=clip)
            im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            out = OUT / "img" / "install" / f"{line}-step-{i}.webp"
            size = save_webp(im, out, quality=82)
            print(f"{out.relative_to(REPO)}  {im.size}  {size // 1024} KB")


def logo_paths(skip_white=True, only_mark=False):
    """Turn the vector logo PDF into SVG <path> elements."""
    page = pymupdf.open(MT / "logos" / "logo-pdf 1b.pdf")[0]

    def f(v):
        return ("%.2f" % v).rstrip("0").rstrip(".")

    def pt(q):
        return f"{f(q.x)} {f(q.y)}"

    paths = []
    for i, dr in enumerate(page.get_drawings()):
        fill = dr.get("fill")
        if i == 0 or (skip_white and fill == (1.0, 1.0, 1.0)):
            continue  # background rect / hidden mask fill
        col = "#%02x%02x%02x" % tuple(round(x * 255) for x in fill)
        r = dr["rect"]
        is_mark = r.x0 > 180 and r.y1 < 430 and r.y0 > 150  # the diamond tree
        if only_mark and not is_mark:
            continue
        d, cur = [], None
        for it in dr["items"]:
            k = it[0]
            if k in ("l", "c"):
                a = it[1]
                if cur is None or abs(cur.x - a.x) > 1e-3 or abs(cur.y - a.y) > 1e-3:
                    d.append("M" + pt(a))
                if k == "l":
                    d.append("L" + pt(it[2]))
                    cur = it[2]
                else:
                    d.append("C" + pt(it[2]) + " " + pt(it[3]) + " " + pt(it[4]))
                    cur = it[4]
            elif k == "re":
                q = it[1]
                d.append(f"M{f(q.x0)} {f(q.y0)}H{f(q.x1)}V{f(q.y1)}H{f(q.x0)}Z")
                cur = None
            elif k == "qu":
                q = it[1]
                d.append("M" + pt(q.ul) + "L" + pt(q.ur) + "L" + pt(q.lr) + "L" + pt(q.ll) + "Z")
                cur = None
        rule = ' fill-rule="evenodd"' if dr.get("even_odd") else ""
        paths.append(f'<path fill="{col}"{rule} d="{"".join(d)}"/>')
    return paths


def build_logo():
    full = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="55 52 425 438">'
            + "".join(logo_paths()) + "</svg>\n")
    (OUT / "img" / "logo.svg").write_text(full)
    mark = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="170 140 214 300">'
            + "".join(logo_paths(only_mark=True)) + "</svg>\n")
    (OUT / "img" / "mark.svg").write_text(mark)
    # Favicon SVG: the tree mark on a cream rounded square, readable at 16px.
    fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="142 136 270 300">'
           '<rect x="142" y="136" width="270" height="300" rx="40" fill="#fbf7ee"/>'
           + "".join(logo_paths(only_mark=True)).replace("#769687", "#4f6b5f")
           .replace('d="', 'stroke="#4f6b5f" stroke-width="6" d="')
           + "</svg>\n")
    (REPO / "docs" / "favicon.svg").write_text(fav)
    print("logo.svg", len(full), "mark.svg", len(mark), "favicon.svg", len(fav))


def chrome_png(svg_path, png_path, size, bg="00000000"):
    subprocess.run([
        "google-chrome", "--headless=new", "--disable-gpu", "--hide-scrollbars",
        f"--default-background-color={bg}", f"--window-size={size},{size}",
        f"--screenshot={png_path}", f"data:text/html,<html><body style='margin:0'>"
        f"<img src='file://{svg_path}' style='width:{size}px;height:{size}px;object-fit:contain'>"
        f"</body></html>"], check=True, capture_output=True)


def build_icons():
    tmp = pathlib.Path("/tmp/mtsite-icons")
    tmp.mkdir(exist_ok=True)
    fav = REPO / "docs" / "favicon.svg"
    # Chrome blocks file:// images inside data: URLs, so render via a temp HTML file.
    for size in (180, 512, 48, 32):
        html = tmp / f"icon{size}.html"
        html.write_text(f"<html><body style='margin:0;background:#fbf7ee'><img src='{fav}' "
                        f"style='display:block;width:{size}px;height:{size}px'></body></html>")
        subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--window-size={size},{size}", f"--screenshot={tmp}/icon{size}.png",
                        f"file://{html}"], check=True, capture_output=True)
    Image.open(tmp / "icon180.png").convert("RGB").save(REPO / "docs" / "apple-touch-icon.png", optimize=True)
    Image.open(tmp / "icon512.png").convert("RGB").save(OUT / "img" / "icon-512.png", optimize=True)
    ico = Image.open(tmp / "icon48.png").convert("RGBA")
    ico.save(REPO / "docs" / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("icons done")


def build_fonts():
    # Whole-font WOFF2 wrappers (no subsetting), so the fonts stay unmodified
    # under the SIL Open Font License.
    for src, dst in (("Arvo-Bold.ttf", "arvo-bold.woff2"), ("Outfit[wght].ttf", "outfit-var.woff2")):
        f = TTFont(FONTS / src)
        f.flavor = "woff2"
        f.save(OUT / "fonts" / dst)
        print(dst, (OUT / "fonts" / dst).stat().st_size // 1024, "KB")


def build_og():
    """1200x630 social card: cream, logo, line names, two product mains."""
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(im)
    d.rectangle([0, H - 120, W, H], fill=(87, 117, 102))  # sage-deep band
    tmp = pathlib.Path("/tmp/mtsite-icons")
    html = tmp / "logo.html"
    html.write_text(f"<html><body style='margin:0;background:#fbf7ee'><img src='{OUT / 'img' / 'logo.svg'}' "
                    "style='display:block;width:300px;height:309px'></body></html>")
    subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--window-size=300,309", f"--screenshot={tmp}/logo.png", f"file://{html}"],
                   check=True, capture_output=True)
    logo = Image.open(tmp / "logo.png").convert("RGB")
    im.paste(logo, (70, 60))
    for i, key in enumerate(("zip-50", "ea-10")):
        p = square(flatten(Image.open(PRODUCTS[key]))).resize((340, 340), Image.LANCZOS)
        card = Image.new("RGB", (360, 360), (255, 255, 255))
        card.paste(p, (10, 10))
        im.paste(card, (440 + i * 375, 70))
    arvo = ImageFont.truetype(str(FONTS / "Arvo-Bold.ttf"), 40)
    d.text((70, H - 88), "Self-drilling zip & toggle drywall anchors", font=arvo, fill=CREAM)
    out = OUT / "img" / "og-card.jpg"
    im.save(out, "JPEG", quality=82, optimize=True, progressive=True)
    print("og-card.jpg", out.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    for sub in ("img/products", "img/install", "fonts"):
        (OUT / sub).mkdir(parents=True, exist_ok=True)
    build_fonts()
    build_logo()
    build_icons()
    build_products()
    build_steps()
    build_og()
