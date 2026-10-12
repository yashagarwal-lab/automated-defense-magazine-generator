import os
from pathlib import Path
from playwright.sync_api import sync_playwright

from ..config import OUTPUT_DIR, DEFAULT_PDF_NAME

def export_pdf(
    html_path: Path,
    pdf_path: Path = None
) -> Path:
    """Export high-resolution 50-page print PDF via Playwright Chromium."""
    if pdf_path is None:
        pdf_path = OUTPUT_DIR / DEFAULT_PDF_NAME

    file_url = f"file://{html_path.resolve()}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(1000)
        page.pdf(
            path=str(pdf_path.resolve()),
            print_background=True,
            format="A4",
            display_header_footer=False
        )
        browser.close()

    if not pdf_path.exists():
        raise RuntimeError(f"Failed to compile PDF at {pdf_path}")

    return pdf_path
