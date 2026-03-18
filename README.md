# PDF generation POC (server-side)

Proof of concept for generating course PDFs on the server, with a structure similar to the frontend `pdf-preview` (cover page, topic header, topic body).

## What’s in this repo

- **`template.html`** — Static HTML that mirrors the PDF layout:
  - **Cover page**: primary-colored hero, course title, description, table of contents (units + topics).
  - **Topic pages**: header bar + body with paragraphs, lists, table, and a button-style block.
- **`styles.css`** — Styling aligned with the React PDF theme (colors, fonts, cover, topic header/body).
- **`main.py`** — Python script that converts the HTML to PDF using [WeasyPrint](https://weasyprint.org/).

## Setup

1. **Python env and install**:

   ```bash
   cd pdf-poc
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Choose a PDF backend**:

   - **Option A — Playwright** (no system deps, recommended for POC):  
     `playwright install chromium`
   - **Option B — WeasyPrint** (needs Cairo/Pango):  
     - macOS: `brew install cairo pango gdk-pixbuf libffi`  
     - Ubuntu/Debian: `sudo apt-get install libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev`

## Generate the PDF

**With Playwright** (works without system libs):

```bash
playwright install chromium
python main_playwright.py
```

**With WeasyPrint** (after installing system deps above):

```bash
python main.py
```

Output is written to `output.pdf` in the same directory.

To use custom paths:

```python
from pathlib import Path
from main import generate_pdf

generate_pdf(
    html_path=Path("template.html"),
    output_path=Path("my-course.pdf"),
)
```

## Next steps (for production)

- Replace the static HTML with a **templating engine** (Jinja2, etc.) and data from your API (content, theme, logo).
- Optionally use **Playwright** (or similar) instead of WeasyPrint if you need to reuse the exact same HTML/JS as the frontend or need more complex layout.
- Add **fonts** (e.g. bundled or from a CDN) and ensure they are available to the PDF renderer (WeasyPrint can use local or `@font-face` URLs).
