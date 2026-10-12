import json
from pathlib import Path
from typing import Dict, Any, List
from playwright.sync_api import sync_playwright

from ..config import DATA_DIR, OUTPUT_DIR
from ..synthesis.cleaner import clean_text, split_sentences

MAX_WORDS = 220
BUFFER_PX = -1

CHECK_JS = """
() => {
  const mm = v => Math.round(v * 25.4 / 96 * 10) / 10;
  const out = [];
  document.querySelectorAll('.page').forEach(pg => {
    const inner = pg.querySelector('.page-inner');
    if (!inner) return;
    const lim = inner.getBoundingClientRect().bottom + 1;
    let worst = 0;
    inner.querySelectorAll('*').forEach(el => {
      const b = el.getBoundingClientRect().bottom;
      if (b > lim) worst = Math.max(worst, b - lim);
    });
    let clipped = 0;
    inner.querySelectorAll('.body, article, .lead-main, .lead-side').forEach(el => {
      const cs = getComputedStyle(el);
      if (cs.overflow === 'visible') return;
      clipped = Math.max(clipped, el.scrollHeight - el.clientHeight, el.scrollWidth - el.clientWidth);
    });
    const total = Math.max(worst, clipped);
    if (total > 1) out.push(pg.id + ':' + mm(total) + 'mm');
  });
  return out;
}
"""

FIT_JS = """
(args) => {
  const [plan, buf] = args;
  const res = {};
  const over = pg => {
    const inner = pg.querySelector('.page-inner');
    if (!inner) return false;
    const lim = inner.getBoundingClientRect().bottom - buf;
    for (const el of inner.querySelectorAll('*')) {
      if (el.getBoundingClientRect().bottom > lim) return true;
    }
    for (const el of inner.querySelectorAll('.body, article, .lead-main, .lead-side')) {
      const cs = getComputedStyle(el);
      if (cs.overflow !== 'visible') {
        if (el.scrollHeight - el.clientHeight > 1 || el.scrollWidth - el.clientWidth > 1) return true;
      }
    }
    return false;
  };
  for (const [pid, cands] of Object.entries(plan)) {
    const pg = document.getElementById(pid);
    if (!pg) continue;
    const bodies = [...pg.querySelectorAll('.body')];
    const k = cands.map(() => 1), done = cands.map(() => false);
    const apply = i => {
      const p = document.createElement('p');
      p.textContent = cands[i].slice(0, k[i]).join(' ');
      if (bodies[i]) bodies[i].replaceChildren(p);
    };
    cands.forEach((_, i) => apply(i));
    let progress = true;
    while (progress) {
      progress = false;
      for (let i = 0; i < cands.length; i++) {
        if (done[i]) continue;
        if (k[i] >= cands[i].length) { done[i] = true; continue; }
        k[i]++; apply(i);
        if (over(pg)) { k[i]--; apply(i); done[i] = true; } else progress = true;
      }
    }
    res[pid] = { k, bad: over(pg) };
  }
  return res;
}
"""

def check_pages_overflow(html_path: Path) -> List[str]:
    """Headless Chromium DOM overflow detector measuring pixel and millimeter clipping per page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file://{html_path.resolve()}", wait_until="networkidle")
        page.wait_for_timeout(1000)
        overflows = page.evaluate(CHECK_JS)
        browser.close()
    return overflows

def get_candidates(art: Dict[str, Any], pool: Dict[str, Any]) -> List[str]:
    """Extract word-bounded sentences for fitting."""
    existing = " ".join(p for p in art.get("body", []) if not p.strip().startswith("(Source:")).strip()
    full = clean_text(pool.get(art["id"], {}).get("text", ""))
    if full and existing[:40] and full.startswith(existing[:40]):
        src = full
    else:
        src = existing
    out = []
    words = 0
    for s in split_sentences(src):
        words += len(s.split())
        if out and words > MAX_WORDS:
            break
        out.append(s)
    return out if out else [src]

def fit_article_summaries(
    html_path: Path,
    articles_path: Path = None,
    pool_path: Path = None
) -> Dict[str, Any]:
    """Iteratively tune article summary sentence counts using headless browser feedback."""
    if articles_path is None:
        articles_path = DATA_DIR / "articles.json"
    if pool_path is None:
        pool_path = DATA_DIR / "pool.json"

    articles = json.loads(articles_path.read_text(encoding="utf-8"))
    pool = json.loads(pool_path.read_text(encoding="utf-8")) if pool_path.exists() else {}

    from ..rendering.engine import compile_magazine_data
    from .planner import build_pages_plan

    mag, arts = compile_magazine_data()
    pages, *_ = build_pages_plan(mag, arts)

    plan = {}
    order = {}
    for p in pages:
        if p["type"] in ("lead", "pair", "trio"):
            pid = f"page-{p['n']}"
            plan[pid] = [get_candidates(a, pool) for a in p["arts"]]
            order[pid] = [a["id"] for a in p["arts"]]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file://{html_path.resolve()}", wait_until="networkidle")
        page.wait_for_timeout(1000)
        fit_results = page.evaluate(FIT_JS, [plan, BUFFER_PX])
        browser.close()

    updated_count = 0
    for pid, res in fit_results.items():
        k_values = res["k"]
        for i, aid in enumerate(order[pid]):
            chosen_sentences = plan[pid][i][:k_values[i]]
            articles[aid]["body"] = [" ".join(chosen_sentences)]
            updated_count += 1

    articles_path.write_text(json.dumps(articles, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"updated_articles": updated_count, "fit_results": fit_results}
