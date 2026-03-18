#!/usr/bin/env python3
"""
Server-side PDF generation POC.
Renders the static HTML template (similar to pdf-preview structure) to PDF using WeasyPrint.
"""

from pathlib import Path

from weasyprint import HTML, CSS


def get_base_dir() -> Path:
    return Path(__file__).resolve().parent


def generate_pdf(
    html_path: Path | None = None,
    css_path: Path | None = None,
    output_path: Path | None = None,
) -> Path:
    base = get_base_dir()
    html_path = html_path or base / "template.html"
    css_path = css_path or base / "styles.css"
    output_path = output_path or base / "output.pdf"

    if not html_path.exists():
        raise FileNotFoundError(f"HTML template not found: {html_path}")

    # Load HTML (relative to template so CSS href works)
    html = HTML(filename=str(html_path), base_url=str(html_path.parent))

    # Optional: add print-specific CSS for page size and margins
    print_css = CSS(
        string="""
        @page {
            size: A4;
            margin: 20mm;
        }
        """
    )

    # Render to PDF
    html.write_pdf(
        output_path,
        stylesheets=[
            CSS(filename=str(css_path)),
            print_css,
        ],
    )

    return output_path


if __name__ == "__main__":
    out = generate_pdf()
    print(f"PDF generated: {out}")
