import click
import json
from pathlib import Path
from typing import Optional

from .config import OUTPUT_DIR, DEFAULT_PDF_NAME, DATA_DIR
from .rendering.engine import render_print_magazine, render_web_reader, compile_magazine_data
from .rendering.pdf_exporter import export_pdf
from .layout.fitter import check_pages_overflow, fit_article_summaries
from .layout.planner import build_pages_plan
from .layout.budgeter import auto_budget_magazine
from .curation.allocator import allocate_articles_to_sections
from .ingestion.factory import ingest_from_source
from .reader.server import run_server

@click.group()
@click.version_option()
def main():
    """Autonomous Multi-Page Defense Publication Compiler & Automated Typesetter."""
    pass

@main.command()
@click.option("--output", "-o", type=click.Path(), default=None, help="Path to output HTML file")
@click.option("--config", "-c", type=click.Path(), default=None, help="Path to YAML or JSON config")
@click.option("--theme", "-t", default=None, help="Theme: army_gold, navy_blue, airforce_slate, editorial_mono")
@click.option("--pages", "-p", default=None, type=int, help="Target page count")
def render(output, config, theme, pages):
    """Render print-ready A4 HTML magazine using Jinja2."""
    out_path = Path(output) if output else OUTPUT_DIR / "index.html"
    cfg_path = Path(config) if config else None
    click.echo(f"Rendering print magazine to {out_path}...")
    res = render_print_magazine(out_path, config_path=cfg_path, theme=theme, target_pages=pages)
    click.secho(f"✓ Rendered print magazine: {res}", fg="green", bold=True)

@main.command()
@click.option("--output", "-o", type=click.Path(), default=None, help="Path to output HTML file")
@click.option("--config", "-c", type=click.Path(), default=None, help="Path to YAML or JSON config")
@click.option("--theme", "-t", default=None, help="Theme: army_gold, navy_blue, airforce_slate, editorial_mono")
@click.option("--pages", "-p", default=None, type=int, help="Target page count")
def reader(output, config, theme, pages):
    """Render the interactive digital flipbook web reader."""
    out_path = Path(output) if output else OUTPUT_DIR / "reader.html"
    cfg_path = Path(config) if config else None
    click.echo(f"Rendering interactive web reader to {out_path}...")
    res = render_web_reader(out_path, config_path=cfg_path, theme=theme, target_pages=pages)
    click.secho(f"✓ Rendered web reader: {res}", fg="green", bold=True)

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
    """Check all pages for text overflow or clipping via headless browser."""
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
        click.secho("✓ All pages pass! Zero overflow or text clipping detected.", fg="green", bold=True)

@main.command()
@click.option("--output", "-o", type=click.Path(), default=None, help="Path to output PDF file")
@click.option("--config", "-c", type=click.Path(), default=None, help="Path to YAML or JSON config")
@click.option("--theme", "-t", default=None, help="Theme name")
def pdf(output, config, theme):
    """Compile publication-grade print PDF via Playwright Chromium."""
    html_path = OUTPUT_DIR / "index.html"
    cfg_path = Path(config) if config else None
    click.echo("Rendering HTML prior to PDF compilation...")
    render_print_magazine(html_path, config_path=cfg_path, theme=theme)
    out_pdf = Path(output) if output else OUTPUT_DIR / DEFAULT_PDF_NAME
    click.echo(f"Compiling print PDF to {out_pdf}...")
    res = export_pdf(html_path, out_pdf)
    size_mb = res.stat().st_size / (1024 * 1024)
    click.secho(f"✓ Compiled PDF: {res} ({size_mb:.2f} MB)", fg="green", bold=True)

@main.command()
@click.option("--host", default="127.0.0.1", help="Host address")
@click.option("--port", "-p", default=8000, type=int, help="Port number")
def serve(host, port):
    """Launch interactive web reader preview server."""
    click.secho(f"Starting preview server at http://{host}:{port}/reader ...", fg="cyan", bold=True)
    run_server(host=host, port=port)

@main.command()
@click.option("--pages", "-p", default=50, type=int, help="Target publication pages (e.g. 24, 32, 50)")
@click.option("--config", "-c", type=click.Path(), default=None, help="Path to publication config")
def plan(pages, config):
    """Inspect mathematical page budget breakdown and layout allocation."""
    cfg_path = Path(config) if config else None
    mag, arts = compile_magazine_data(config_path=cfg_path)
    curated_pool = allocate_articles_to_sections(arts)
    budget = auto_budget_magazine(pages, curated_pool, sections_meta=mag.get("sections", []))

    click.secho(f"\n=== PUBLICATION PAGE BUDGET BREAKDOWN (Target: {pages} Pages) ===", fg="cyan", bold=True)
    click.echo(f"• Front Matter:  Cover (1) + Contents (1) + Editor Note (1)" + (" + Primer (1)" if budget['include_overview'] else ""))
    click.echo(f"• Content Sections ({len(budget['sections'])}):")
    total_sec_pages = 0
    for s in budget['sections']:
        s_pages = len(s.get("pages", [])) + 1  # 1 opener + content
        total_sec_pages += s_pages
        click.echo(f"   - {s['name'][:35]:<35} : 1 Opener + {len(s.get('pages', []))} Content Pages ({len(s.get('pages', []))*2} arts)")
    click.echo(f"• Back Matter:   Appendix 1 Sources (1) + Appendix 2 Reasoning ({budget['appendix2_pages']}) + Back Cover (1)")
    click.echo(f"• Appendix 2 Chunks: {budget['appendix2_chunks']} (Total: {sum(budget['appendix2_chunks'])} rows)")
    total_computed = (4 if budget['include_overview'] else 3) + total_sec_pages + 1 + budget['appendix2_pages'] + 1
    click.secho(f"\n✓ Total Planned Pages: {total_computed} / {pages} (Match: {total_computed == pages})\n", fg="green", bold=True)

@main.command()
@click.option("--source", "-s", required=True, type=click.Path(), help="Source file or feed URL")
@click.option("--type", "-t", default=None, help="Source type: json, markdown, rss")
@click.option("--output", "-o", default=None, type=click.Path(), help="Output path for ingested JSON")
def ingest(source, type, output):
    """Ingest articles from raw source (JSON, Markdown, or RSS feed)."""
    click.echo(f"Ingesting content from {source}...")
    articles = ingest_from_source(source, source_type=type)
    click.secho(f"✓ Ingested {len(articles)} articles.", fg="green", bold=True)
    if output:
        out_path = Path(output)
        out_path.write_text(json.dumps(articles, indent=2, ensure_ascii=False), encoding="utf-8")
        click.secho(f"✓ Saved to {out_path}", fg="green")

@main.command()
@click.option("--config", "-c", type=click.Path(), default=None, help="Path to YAML or JSON config")
@click.option("--theme", "-t", default=None, help="Theme name")
@click.option("--pages", "-p", default=None, type=int, help="Target pages")
def all(config, theme, pages):
    """Run full end-to-end publishing pipeline: fit -> render -> check -> pdf."""
    click.secho("=== RUNNING FULL END-TO-END PUBLISHING PIPELINE ===", fg="cyan", bold=True)
    html_path = OUTPUT_DIR / "index.html"
    cfg_path = Path(config) if config else None

    render_print_magazine(html_path, config_path=cfg_path, theme=theme, target_pages=pages)
    click.echo("Stage 1: Running DOM auto-fitter...")
    fit_article_summaries(html_path)
    render_print_magazine(html_path, config_path=cfg_path, theme=theme, target_pages=pages)
    render_web_reader(OUTPUT_DIR / "reader.html", config_path=cfg_path, theme=theme, target_pages=pages)
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
