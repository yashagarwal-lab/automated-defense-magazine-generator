import json
import yaml
import os
import shutil
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
from jinja2 import Environment, FileSystemLoader

from ..config import DATA_DIR, TEMPLATES_DIR, OUTPUT_DIR, STATIC_DIR, TARGET_PAGE_COUNT
from ..layout.planner import build_pages_plan

def load_config_file(config_path: Path) -> Dict[str, Any]:
    """Parse YAML or JSON magazine configuration file."""
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    raw = config_path.read_text(encoding="utf-8")
    if config_path.suffix.lower() in (".yaml", ".yml"):
        return yaml.safe_load(raw) or {}
    return json.loads(raw)

def compile_magazine_data(
    config_path: Path = None,
    articles_path: Path = None,
    target_pages: int = None,
    theme: str = None
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Load, merge, and validate magazine structure and curated articles."""
    if config_path is None:
        yaml_cand = Path("configs/securing_the_northeast_50p.yaml")
        if yaml_cand.exists():
            mag = load_config_file(yaml_cand)
        else:
            mag_file = DATA_DIR / "magazine.json"
            if not mag_file.exists():
                raise FileNotFoundError(f"Missing magazine.json in {DATA_DIR}")
            mag = json.loads(mag_file.read_text(encoding="utf-8"))
    else:
        mag = load_config_file(config_path)

    if articles_path is None:
        arts_file = DATA_DIR / "articles.json"
        if not arts_file.exists():
            raise FileNotFoundError(f"Missing articles.json in {DATA_DIR}")
        arts = json.loads(arts_file.read_text(encoding="utf-8"))
    else:
        arts = load_config_file(articles_path)

    if theme:
        mag["theme"] = theme
    if target_pages:
        mag["target_pages"] = target_pages

    return mag, arts

def setup_output_assets():
    """Ensure output directory has necessary CSS, images, and fonts available."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_img = OUTPUT_DIR / "images"
    if not out_img.exists():
        try:
            out_img.symlink_to(STATIC_DIR / "images", target_is_directory=True)
        except Exception:
            shutil.copytree(STATIC_DIR / "images", out_img, dirs_exist_ok=True)

    out_css = OUTPUT_DIR / "css"
    if not out_css.exists():
        try:
            out_css.symlink_to(STATIC_DIR / "css", target_is_directory=True)
        except Exception:
            shutil.copytree(STATIC_DIR / "css", out_css, dirs_exist_ok=True)

    out_js = OUTPUT_DIR / "js"
    if not out_js.exists():
        try:
            out_js.symlink_to(STATIC_DIR / "js", target_is_directory=True)
        except Exception:
            shutil.copytree(STATIC_DIR / "js", out_js, dirs_exist_ok=True)

    # Link root styles.css and layouts.css in output/ for print index.html
    for css_name in ["styles.css", "layouts.css", "web_reader.css"]:
        src_css = STATIC_DIR / "css" / css_name
        dst_css = OUTPUT_DIR / css_name
        if src_css.exists() and not dst_css.exists():
            try:
                dst_css.symlink_to(src_css)
            except Exception:
                shutil.copyfile(src_css, dst_css)

def render_print_magazine(
    output_path: Path = None,
    config_path: Path = None,
    articles_path: Path = None,
    target_pages: int = None,
    theme: str = None
) -> Path:
    """Render the print-ready A4 HTML magazine using Jinja2."""
    if output_path is None:
        output_path = OUTPUT_DIR / "index.html"

    setup_output_assets()
    mag, arts = compile_magazine_data(
        config_path=config_path,
        articles_path=articles_path,
        target_pages=target_pages,
        theme=theme
    )
    pages, toc, stats, used = build_pages_plan(mag, arts)

    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=True
    )
    template = env.get_template("print/magazine.html.j2")
    html_content = template.render(
        mag=mag,
        pages=pages,
        toc=toc,
        stats=stats
    )

    output_path.write_text(html_content, encoding="utf-8")
    return output_path

def render_web_reader(
    output_path: Path = None,
    config_path: Path = None,
    articles_path: Path = None,
    target_pages: int = None,
    theme: str = None
) -> Path:
    """Render the interactive dual-spread flipbook web reader."""
    if output_path is None:
        output_path = OUTPUT_DIR / "reader.html"

    setup_output_assets()
    mag, arts = compile_magazine_data(
        config_path=config_path,
        articles_path=articles_path,
        target_pages=target_pages,
        theme=theme
    )
    pages, toc, stats, used = build_pages_plan(mag, arts)

    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=True
    )
    template = env.get_template("reader/web_reader.html.j2")
    html_content = template.render(
        mag=mag,
        pages=pages,
        toc=toc,
        stats=stats
    )

    output_path.write_text(html_content, encoding="utf-8")
    return output_path
