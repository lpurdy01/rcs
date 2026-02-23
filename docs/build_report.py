#!/usr/bin/env python3
"""
build_report.py  —  Convert docs/report_composition.md into docs/report.html

Run from anywhere inside the repo:
    python3 docs/build_report.py

The script injects converted HTML between the comment markers:
    <!-- REPORT_CONTENT_START -->  and  <!-- REPORT_CONTENT_END -->
inside docs/report.html, leaving all surrounding template HTML untouched.
Subsequent runs replace whatever was injected previously — safe to re-run.

Requirements:
    pip3 install markdown --break-system-packages

What this handles:
  • Standard markdown  (headers, paragraphs, lists, blockquotes, bold, italic, hr)
  • GFM tables
  • Fenced code blocks  (``` and ~~~)
  • Mermaid diagrams    (```mermaid → <pre class="mermaid"> for Mermaid.js)
  • Display math        (non-standard [ ... ] block → $$ ... $$ for MathJax)
  • Image + italic caption on next line → <figure><figcaption>
  • *SUG: ...* editorial notes → <div class="editorial-note">
"""

import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit(
        "Missing dependency — run: pip3 install markdown --break-system-packages"
    )

DOCS  = Path(__file__).parent.resolve()
SRC   = DOCS / "report_composition.md"
DEST  = DOCS / "report.html"

START = "<!-- REPORT_CONTENT_START -->"
END   = "<!-- REPORT_CONTENT_END -->"


# ── 1. Pre-process markdown ───────────────────────────────────────────────────

def preprocess(text: str) -> str:
    """Fix non-standard constructs before the markdown parser sees the text."""

    # Display math written as a standalone bracket block:
    #   [
    #   \equation here
    #   ]
    # → standard MathJax display math:  $$\equation here$$
    text = re.sub(
        r"^\[$\n(.*)\n^\]$",
        lambda m: "$$\n" + m.group(1) + "\n$$",
        text,
        flags=re.MULTILINE,
    )

    return text


# ── 2. Convert markdown → HTML ────────────────────────────────────────────────

_MD_EXTENSIONS = ["tables", "fenced_code", "toc", "sane_lists"]


def convert(text: str) -> str:
    md = markdown.Markdown(extensions=_MD_EXTENSIONS)
    return md.convert(text)


# ── 3. Post-process HTML ──────────────────────────────────────────────────────

def postprocess(html: str) -> str:

    # — Mermaid diagrams ——————————————————————————————————————————————————————
    # fenced_code produces: <pre><code class="language-mermaid">…</code></pre>
    # Mermaid.js expects:   <pre class="mermaid">…</pre>
    html = re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        r'<pre class="mermaid">\1</pre>',
        html,
        flags=re.DOTALL,
    )

    # — Strip SUG editorial notes (image-adjacent) ————————————————————————————
    # Pattern: <p><img ...>\n<em>SUG: ...</em></p>  → keep only the figure
    html = re.sub(
        r"<p>(<img[^>]+>)\n<em>SUG:.*?</em></p>",
        r"<figure>\1</figure>",
        html,
        flags=re.DOTALL,
    )

    # — Image + regular italic caption on next line → <figure><figcaption> ———
    # Pattern: <p><img ...>\n<em>caption</em></p>
    html = re.sub(
        r"<p>(<img[^>]+>)\n(<em>.*?</em>)</p>",
        r"<figure>\1<figcaption>\2</figcaption></figure>",
        html,
        flags=re.DOTALL,
    )

    # — Standalone images (no caption) → <figure> ————————————————————————————
    html = re.sub(
        r"<p>(<img[^>]+>)</p>",
        r"<figure>\1</figure>",
        html,
    )

    # — Wrap tech tree figure in horizontal scroll container ——————————————————
    def _wrap_tech_tree(m):
        inner = m.group(1)
        if '<figcaption>' in inner:
            inner = inner.replace(
                '</figcaption>',
                ' <a href="rcs_tech_tree.svg" target="_blank">View full size ↗</a></figcaption>',
            )
        else:
            inner = inner.replace(
                '</figure>',
                '<figcaption><a href="rcs_tech_tree.svg" target="_blank">View full size ↗</a>'
                '</figcaption></figure>',
            )
        return '<div class="figure-scroll">\n' + inner + '\n</div>'

    html = re.sub(
        r'(<figure><img[^>]+rcs_tech_tree\.svg[^>]*>(?:<figcaption>.*?</figcaption>)?</figure>)',
        _wrap_tech_tree,
        html,
        flags=re.DOTALL,
    )

    # — Strip standalone SUG notes entirely ————————————————————————————————————
    # Pattern: <p><em>SUG: ...</em></p>
    html = re.sub(
        r"<p><em>SUG:.*?</em></p>",
        "",
        html,
        flags=re.DOTALL,
    )

    return html


# ── 4. Inject into report.html ────────────────────────────────────────────────

def inject(content_html: str, template: str) -> str:
    if START not in template:
        sys.exit(f"Error: marker '{START}' not found in {DEST}")
    if END not in template:
        sys.exit(f"Error: marker '{END}' not found in {DEST}")

    before = template[: template.index(START) + len(START)]
    after  = template[template.index(END) :]
    return before + "\n" + content_html + "\n      " + after


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    if not SRC.exists():
        sys.exit(f"Source not found: {SRC}")
    if not DEST.exists():
        sys.exit(f"Template not found: {DEST}")

    print(f"  source   : {SRC.relative_to(DOCS.parent)}")

    raw      = SRC.read_text(encoding="utf-8")
    pre      = preprocess(raw)
    html     = convert(pre)
    out      = postprocess(html)
    template = DEST.read_text(encoding="utf-8")
    result   = inject(out, template)
    DEST.write_text(result, encoding="utf-8")

    print(f"  output   : {DEST.relative_to(DOCS.parent)}")
    print("  done.")


if __name__ == "__main__":
    main()
