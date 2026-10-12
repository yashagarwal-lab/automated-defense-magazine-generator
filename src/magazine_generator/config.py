from pathlib import Path
import os

PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent.parent

DATA_DIR = Path(os.environ.get("MAG_DATA_DIR", PROJECT_ROOT / "data"))
STATIC_DIR = Path(os.environ.get("MAG_STATIC_DIR", PROJECT_ROOT / "static"))
TEMPLATES_DIR = Path(os.environ.get("MAG_TEMPLATES_DIR", PROJECT_ROOT / "templates"))
OUTPUT_DIR = Path(os.environ.get("MAG_OUTPUT_DIR", PROJECT_ROOT / "output"))

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

WINDOW_START = "2026-09-01"
WINDOW_END = "2026-10-03"
DATE_WINDOW = (WINDOW_START, WINDOW_END)

TARGET_PAGE_COUNT = 50
APPENDIX2_ROWS_PER_PAGE = [23, 25, 26]

SECTIONS = [
    "Security & Strategic Affairs",
    "Regional News & Development",
    "Society & Youth Empowerment",
    "Sports & Achievements"
]

DEFAULT_PDF_NAME = "Securing_the_Northeast_Magazine.pdf"
