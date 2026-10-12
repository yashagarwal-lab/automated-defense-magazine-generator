import click
from pathlib import Path
from .config import OUTPUT_DIR, DEFAULT_PDF_NAME
from .rendering.engine import render_print_magazine, render_web_reader
from .rendering.pdf_exporter import export_pdf
from .layout.fitter import check_pages_overflow, fit_article_summaries
from .reader.server import run_server

@click.group()
@click.version_option()
def main():
    """Autonomous Multi-Page Defense Publication Compiler & Automated Typesetter."""
    pass

@main.command()
@click.option("--output", "-o", type=click.Path(), default=None, help="Path to output HTML file")
def render(output):
    """Render print-ready A4 HTML magazine using Jinja2."""
    out_path = Path(output) if output else OUTPUT_DIR / "index.html"
    click.echo(f"Rendering print magazine to {out_path}...")
    res = render_print_magazine(out_path)
    click.secho(f"✓ Rendered 50-page print magazine: {res}", fg="green", bold=True)

@main.command()
def fit():
    """Run sentence-by-sentence DOM auto-fitting loop to eliminate text clipping."""
    html_path = OUTPUT_DIR / "index.html"
    if not html_path.exists():
        click.echo("Building base HTML for fitting...")
        render_print_magazine(html_path)
    click.echo("Executing headless browser layout fitting loop...")
    res = fit_article_summaries(html_path)
    click.secho(f"✓ Optimized {res['updated_articles']} article slots across all sections.", fg="green", bold=True)
    # Re-render HTML with updated fitted summaries
    render_print_magazine(html_path)
    click.secho("✓ Updated print HTML with fitted content.", fg="green")

@main.command()
def check():
    """Check all 50 pages for text overflow or clipping via headless browser."""
    html_path = OUTPUT_DIR / "index.html"
    if not html_path.exists():
        click.echo("Building HTML for check...")
        render_print_magazine(html_path)
    click.echo("Auditing pages for overflow...")
    bad = check_pages_overflow(html_path)
    if bad:
        click.secho(f"✗ Found {len(bad)} overflowing page(s): {', '.join(bad)}", fg="red", bold=True)
        raise SystemExit(1)
    else:
        click.secho("✓ All 50 pages pass! Zero overflow or text clipping detected.", fg="green", bold=True)

@main.command()
@click.option("--output", "-o", type=click.Path(), default=None, help="Path to output PDF file")
def pdf(output):
    """Compile publication-grade 50-page print PDF via Playwright Chromium."""
    html_path = OUTPUT_DIR / "index.html"
    if not html_path.exists():
        click.echo("Rendering HTML prior to PDF compilation...")
        render_print_magazine(html_path)
    out_pdf = Path(output) if output else OUTPUT_DIR / DEFAULT_PDF_NAME
    click.echo(f"Compiling print PDF to {out_pdf}...")
    res = export_pdf(html_path, out_pdf)
    size_mb = res.stat().st_size / (1024 * 1024)
    click.secho(f"✓ Compiled PDF: {res} ({size_mb:.2f} MB)", fg="green", bold=True)

@main.command()
@click.option("--output", "-o", type=click.Path(), default=None, help="Path to output HTML file")
def reader(output):
    """Render the interactive digital flipbook web reader."""
    out_path = Path(output) if output else OUTPUT_DIR / "reader.html"
    click.echo(f"Rendering interactive web reader to {out_path}...")
    res = render_web_reader(out_path)
    click.secho(f"✓ Rendered web reader: {res}", fg="green", bold=True)

@main.command()
@click.option("--host", default="127.0.0.1", help="Host address")
@click.option("--port", "-p", default=8000, type=int, help="Port number")
def serve(host, port):
    """Launch interactive web reader preview server."""
    click.secho(f"Starting preview server at http://{host}:{port}/reader ...", fg="cyan", bold=True)
    run_server(host=host, port=port)

@main.command()
def all():
    """Run full end-to-end publishing pipeline: fit -> render -> check -> pdf."""
    click.secho("=== RUNNING FULL END-TO-END PUBLISHING PIPELINE ===", fg="cyan", bold=True)
    html_path = OUTPUT_DIR / "index.html"
    render_print_magazine(html_path)
    click.echo("Stage 1: Running DOM auto-fitter...")
    fit_article_summaries(html_path)
    render_print_magazine(html_path)
    render_web_reader(OUTPUT_DIR / "reader.html")
    click.echo("Stage 2: Auditing for text overflow...")
    bad = check_pages_overflow(html_path)
    if bad:
        click.secho(f"✗ Overflow detected: {bad}", fg="red")
        raise SystemExit(1)
    click.secho("✓ Zero overflow verified!", fg="green")
    click.echo("Stage 3: Compiling print PDF...")
    res_pdf = export_pdf(html_path, OUTPUT_DIR / DEFAULT_PDF_NAME)
    size_mb = res_pdf.stat().st_size / (1024 * 1024)
    click.secho(f"✓ Pipeline Complete! PDF: {res_pdf} ({size_mb:.2f} MB)", fg="green", bold=True)

if __name__ == "__main__":
    main()
