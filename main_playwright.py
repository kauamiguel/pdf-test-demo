#!/usr/bin/env python3
"""
Alternative PDF generator using Playwright (headless Chromium).
Use this if WeasyPrint fails due to missing system libs (Cairo/Pango).
Run once: playwright install chromium
"""

from pathlib import Path

from playwright.sync_api import sync_playwright


def get_base_dir() -> Path:
    return Path(__file__).resolve().parent


def generate_pdf(
    html_path: Path | None = None,
    output_path: Path | None = None,
) -> Path:
    base = get_base_dir()
    html_path = html_path or base / "template.html"
    output_path = output_path or base / "output.pdf"

    if not html_path.exists():
        raise FileNotFoundError(f"HTML template not found: {html_path}")

    # Use file:// so CSS and fonts load correctly
    url = html_path.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        page.pdf(
            path=str(output_path),
            format="A4",
            margin={"top": "20mm", "right": "20mm", "bottom": "20mm", "left": "20mm"},
            print_background=True,
        )
        browser.close()

    return output_path


if __name__ == "__main__":
    out = generate_pdf()
    print(f"PDF generated: {out}")
