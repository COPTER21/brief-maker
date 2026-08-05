#!/usr/bin/env python3
"""
render_pdf.py — render a self-contained HTML (from build_html.py) to A4 PDF.

Uses Playwright/Chromium for best Thai shaping & full CSS support.
@page rules in base.css control size (A4) and margins, so we render with
prefer_css_page_size and print_background on.

Usage:
  python render_pdf.py DOC.html -o DOC.pdf
"""
import argparse, pathlib, sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("-o", "--out", required=True)
    args = ap.parse_args()

    src = pathlib.Path(args.html).resolve()
    if not src.exists():
        sys.exit(f"[render_pdf] not found: {src}")
    out = pathlib.Path(args.out).resolve()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("[render_pdf] playwright not installed. pip install playwright && playwright install chromium")

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(src.as_uri(), wait_until="networkidle")
        page.emulate_media(media="print")
        page.pdf(
            path=str(out),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
        )
        browser.close()
    print(f"[render_pdf] wrote {out} ({out.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
