#!/usr/bin/env python3
"""
POC: send the existing pdf-poc HTML + CSS to Gotenberg (Chromium) and save PDF.

Prerequisites:
  docker compose -f gotenberg/docker-compose.yml up -d
  pip install httpx

Usage (from pdf-poc/):
  python gotenberg/convert_to_pdf.py
  GOTENBERG_URL=http://other-host:3000 python gotenberg/convert_to_pdf.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    import httpx
except ImportError:
    print("Install httpx: pip install httpx", file=sys.stderr)
    raise SystemExit(1) from None

# pdf-poc/ (parent of gotenberg/)
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_GOTENBERG = os.environ.get("GOTENBERG_URL", "http://127.0.0.1:3049").rstrip("/")
HEALTH_PATH = "/health"
CONVERT_PATH = "/forms/chromium/convert/html"


def wait_for_gotenberg(client: httpx.Client, base: str, max_attempts: int = 30) -> None:
    for i in range(max_attempts):
        try:
            r = client.get(f"{base}{HEALTH_PATH}")
            if r.status_code == 200:
                return
        except httpx.ConnectError:
            pass
        if i == 0:
            print("Waiting for Gotenberg…", file=sys.stderr)
        import time

        time.sleep(1)
    raise RuntimeError(
        f"Gotenberg not reachable at {base}. Start with:\n"
        "  cd pdf-poc/gotenberg && docker compose up -d"
    )


def convert_html_to_pdf(
    gotenberg_url: str = DEFAULT_GOTENBERG,
    html_path: Path | None = None,
    css_path: Path | None = None,
    output_path: Path | None = None,
) -> Path:
    html_path = html_path or BASE_DIR / "template.html"
    css_path = css_path or BASE_DIR / "styles.css"
    output_path = output_path or BASE_DIR / "output-gotenberg.pdf"

    if not html_path.is_file():
        raise FileNotFoundError(html_path)
    if not css_path.is_file():
        raise FileNotFoundError(css_path)

    # Gotenberg expects the entry document to be named index.html in the multipart upload.
    with (
        httpx.Client(timeout=120.0) as client,
        open(html_path, "rb") as html_f,
        open(css_path, "rb") as css_f,
    ):
        wait_for_gotenberg(client, gotenberg_url)

        files = [
            ("files", ("index.html", html_f, "text/html")),
            ("files", ("styles.css", css_f, "text/css")),
        ]

        # Optional Chromium form fields (inches) — see https://gotenberg.dev/docs/routes#html
        data = {
            "marginTop": "0.4",
            "marginBottom": "0.4",
            "marginLeft": "0.4",
            "marginRight": "0.4",
            "preferCssPageSize": "true",
        }

        url = f"{gotenberg_url}{CONVERT_PATH}"
        response = client.post(url, files=files, data=data)

    if response.status_code != 200:
        raise RuntimeError(
            f"Gotenberg returned {response.status_code}: {response.text[:500]}"
        )

    output_path.write_bytes(response.content)
    return output_path


def main() -> None:
    out = convert_html_to_pdf()
    print(f"PDF written: {out}")


if __name__ == "__main__":
    main()
