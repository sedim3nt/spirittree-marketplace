#!/usr/bin/env python3
"""
Aesop Design System Restyle for AgentOrchard
Batch-updates all 85 HTML files in the repo.
Replaces CSS custom properties AND hardcoded hex colors.
Preserves all JavaScript/Supabase/Stripe logic untouched.
"""

import os
import re
import glob

REPO = "/tmp/ao-redesign"

# ── 1. CSS variable replacements ──────────────────────────────────────────────
# Map old variable VALUES (in :root blocks) to Aesop values.
# These are safe to do as simple string replacements inside <style> tags.

ROOT_VAR_MAP = {
    # Backgrounds
    "--sand-50:#f6f7f8":       "--sand-50:#F4EFE6",
    "--sand-50: #f6f7f8":      "--sand-50: #F4EFE6",
    "--white:#ffffff":         "--white:#F4EFE6",
    "--white:#fff":            "--white:#F4EFE6",
    "--white: #ffffff":        "--white: #F4EFE6",
    # Text
    "--ink-900:#1a1a2e":       "--ink-900:#3A2E20",
    "--ink-700:#2d2d44":       "--ink-700:#3A2E20",
    "--ink-600:#4a4a5a":       "--ink-600:#7A6A52",
    "--ink-500:#6b6b7a":       "--ink-500:#B8AD98",
    # Accent (tide → amber)
    "--tide-600:#006ca5":      "--tide-600:#8B5E3C",
    "--tide-700:#005a8a":      "--tide-700:#6B4428",
    # Borders
    "--border-subtle:rgba(26,26,46,0.05)":  "--border-subtle:rgba(216,206,188,0.6)",
    "--border-card:rgba(26,26,46,0.1)":     "--border-card:#D8CEBC",
    # Tide light (used for step number bg)
    "--tide-light:rgba(13,148,136,0.1)":    "--tide-light:rgba(139,94,60,0.10)",
    # Shadows
    "--shadow-card:0 1px 3px rgba(26,26,46,0.08)":     "--shadow-card:0 2px 12px rgba(58,46,32,0.06)",
    "--shadow-card-hover:0 4px 16px rgba(26,26,46,0.12)": "--shadow-card-hover:0 4px 20px rgba(58,46,32,0.10)",
}

# ── 2. Hardcoded hex replacements in CSS blocks ───────────────────────────────
HEX_MAP = {
    # Old accent blues → amber
    "#006ca5": "#8B5E3C",
    "#005a8a": "#6B4428",
    "#0369a1": "#8B5E3C",
    "#0284c7": "#6B4428",
    # Old bg whites
    "#ffffff":  "#F4EFE6",
    "#fff":     "#F4EFE6",
    "#f6f7f8":  "#F4EFE6",
    # Old ink darks → umber
    "#1a1a2e":  "#3A2E20",
    "#2d2d44":  "#3A2E20",
    "#4a4a5a":  "#7A6A52",
    "#6b6b7a":  "#B8AD98",
    # Old light blue highlight → amber wash
    "#e0f2fe":  "#FDF6EC",
}

# rgba patterns to replace
RGBA_MAP = [
    (r"rgba\(26,26,46,0\.4\)",   "rgba(58,46,32,0.5)"),
    (r"rgba\(26,26,46,0\.05\)",  "rgba(216,206,188,0.6)"),
    (r"rgba\(26,26,46,0\.1\)",   "#D8CEBC"),
    (r"rgba\(26,26,46,0\.08\)",  "rgba(58,46,32,0.06)"),
    (r"rgba\(26,26,46,0\.12\)",  "rgba(58,46,32,0.10)"),
    (r"rgba\(13,148,136,0\.1\)", "rgba(139,94,60,0.10)"),
]

# ── 3. Typography upgrades in CSS blocks ─────────────────────────────────────
TYPOGRAPHY_MAP = {
    # Hero heading: remove bold weight, add literary style
    "font-weight:800;color:var(--ink-900)": "font-weight:300;color:var(--ink-900)",
    "font-weight:700;color:var(--ink-900)": "font-weight:400;color:var(--ink-900)",
    # Nav brand: keep Cormorant, tweak weight
    "font-family:'Cormorant Infant',Georgia,serif;font-size:2.5rem;font-weight:600": 
        "font-family:'Cormorant Infant',Georgia,serif;font-size:2.5rem;font-weight:400;letter-spacing:-0.01em",
    # Nav links: add letter-spacing, uppercase
    "gap:24px;font-size:0.875rem;font-weight:500;color:var(--ink-700)":
        "gap:24px;font-size:0.75rem;font-weight:400;color:var(--ink-700);text-transform:uppercase;letter-spacing:0.15em",
    "gap:24px;font-size:.875rem;font-weight:500;color:var(--ink-700)":
        "gap:24px;font-size:0.75rem;font-weight:400;color:var(--ink-700);text-transform:uppercase;letter-spacing:0.15em",
    # Nav login button
    "border:1px solid rgba(26,26,46,0.4)":  "border:1px solid rgba(58,46,32,0.4)",
    "border:1px solid rgba(26,26,46,.4)":   "border:1px solid rgba(58,46,32,0.4)",
}

# ── 4. New :root block to INJECT (prepend) ────────────────────────────────────
# These add the Aesop variables alongside the existing ones.
AESOP_ROOT_INJECTION = """
  /* ── Aesop Design System ── */
  --aesop-parchment:#F4EFE6;
  --aesop-ivory:#EEE8DC;
  --aesop-stone:#D8CEBC;
  --aesop-limestone:#B8AD98;
  --aesop-bark:#7A6A52;
  --aesop-umber:#3A2E20;
  --aesop-dark-earth:#1E1810;
  --aesop-amber:#8B5E3C;
  --aesop-amber-deep:#6B4428;
  --aesop-amber-light:#C89060;
  --aesop-amber-wash:rgba(139,94,60,0.08);
  --font-display:'Cormorant Infant',Georgia,'Times New Roman',serif;
  --font-ui:'Inter',system-ui,-apple-system,sans-serif;"""

# ── 5. Footer dark background injection ──────────────────────────────────────
# Add dark earth footer styling
FOOTER_CSS_EXTRA = """
/* Aesop footer dark */
footer{background:#1E1810 !important;border-top:none !important}
footer *,.fi,.footer-inner,.fbot,.footer-bottom,.fc,.footer-col{color:#EEE8DC !important}
footer a,.fc nav a,.footer-col nav a{color:#B8AD98 !important}
footer a:hover,.fc nav a:hover,.footer-col nav a:hover{color:#EEE8DC !important}
.footer-bottom p,.fbot p{color:#7A6A52 !important;border-top-color:rgba(216,206,188,0.15) !important}
.fbot{border-top-color:rgba(216,206,188,0.15) !important}
.footer-bottom{border-top-color:rgba(216,206,188,0.15) !important}
"""

# ── 6. Body/nav/card global Aesop CSS to inject ───────────────────────────────
GLOBAL_CSS_EXTRA = """
/* Aesop Global Overrides */
body{background:#F4EFE6;color:#3A2E20;font-family:'Inter',system-ui,-apple-system,sans-serif;line-height:1.8}
h1,h2,h3,h4,h5,h6{font-family:'Cormorant Infant',Georgia,serif;font-weight:400;color:#3A2E20;text-transform:lowercase;letter-spacing:-0.01em;line-height:1.2}
header{background:rgba(244,239,230,0.97) !important;border-bottom:1px solid #D8CEBC !important;backdrop-filter:blur(8px)}
.mobile-menu,.mm{background:#F4EFE6 !important}
.card,.pc{background:#EEE8DC !important;border:1px solid #D8CEBC !important}
.card:hover{background:#EEE8DC !important;box-shadow:0 4px 20px rgba(58,46,32,0.10) !important}
.card-tag{background:rgba(244,239,230,0.8) !important;border-color:#D8CEBC !important;color:#7A6A52 !important}
.btn-primary,.card-btn,.pbtn,.nl-btn{background:#8B5E3C !important;color:#F4EFE6 !important;border-radius:4px !important;letter-spacing:0.05em}
.btn-primary:hover,.card-btn:hover,.pbtn:hover,.nl-btn:hover{background:#6B4428 !important}
.btn-outline{border:1px solid #D8CEBC !important;color:#3A2E20 !important;border-radius:4px !important}
.btn-outline:hover{background:#EEE8DC !important;border-color:#B8AD98 !important}
.nav-login,.nli{background:#8B5E3C !important;color:#F4EFE6 !important;border:none !important;border-radius:4px !important}
.nav-login:hover,.nli:hover{background:#6B4428 !important}
.nl-input{background:#F4EFE6 !important;border-color:#D8CEBC !important;color:#3A2E20 !important}
.nl-input:focus{border-color:#8B5E3C !important;outline:none}
.step-num{background:rgba(139,94,60,0.10) !important;color:#8B5E3C !important}
.products,.how,.stats{background:#F4EFE6 !important}
.hero,.newsletter{background:#F4EFE6 !important}
.cat,.card-cat,.pm .cat,.bl{color:#8B5E3C !important}
.stat h2{color:#3A2E20 !important}
.hero h1,.section-head h2,.how h2,.newsletter h2,.pm h1,.step h3,.stat h2{font-family:'Cormorant Infant',Georgia,serif !important;font-weight:300 !important;text-transform:lowercase !important}
.nav-brand,.nb{font-family:'Cormorant Infant',Georgia,serif !important;font-weight:400 !important;color:#3A2E20 !important;letter-spacing:-0.01em}
select,input,textarea{background:#F4EFE6 !important;border-color:#D8CEBC !important;color:#3A2E20 !important}
select:focus,input:focus,textarea:focus{border-color:#8B5E3C !important;outline:none}
"""

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    original = content

    # ── Step A: Replace :root variable values ──
    for old, new in ROOT_VAR_MAP.items():
        content = content.replace(old, new)

    # ── Step B: Replace hardcoded hex colors (only in <style> blocks) ──
    def replace_in_style(match):
        style_block = match.group(0)
        for old_hex, new_hex in HEX_MAP.items():
            # Case-insensitive hex replace
            style_block = re.sub(re.escape(old_hex), new_hex, style_block, flags=re.IGNORECASE)
        for pattern, replacement in RGBA_MAP:
            style_block = re.sub(pattern, replacement, style_block)
        for old_t, new_t in TYPOGRAPHY_MAP.items():
            style_block = style_block.replace(old_t, new_t)
        return style_block

    content = re.sub(r'<style[^>]*>.*?</style>', replace_in_style, content, flags=re.DOTALL)

    # ── Step C: Inject Aesop vars into :root block ──
    # Find the first :root { and inject after the opening brace
    def inject_root_vars(match):
        root_block = match.group(0)
        if '--aesop-parchment' not in root_block:
            root_block = root_block.replace(':root{', ':root{' + AESOP_ROOT_INJECTION, 1)
            root_block = root_block.replace(':root {\n', ':root {\n' + AESOP_ROOT_INJECTION + '\n', 1)
        return root_block

    content = re.sub(r':root\s*\{[^}]*\}', inject_root_vars, content, flags=re.DOTALL)

    # ── Step D: Inject global CSS + footer CSS before </style> ──
    def inject_global_css(match):
        style_block = match.group(0)
        if 'Aesop Global Overrides' not in style_block:
            style_block = style_block.replace('</style>', GLOBAL_CSS_EXTRA + FOOTER_CSS_EXTRA + '</style>', 1)
        return style_block

    content = re.sub(r'<style[^>]*>.*?</style>', inject_global_css, content, flags=re.DOTALL)

    # ── Step E: Fix hardcoded background:#ffffff on header (inline) ──
    content = re.sub(r'background:#ffffff(?=")', 'background:#F4EFE6', content)
    content = re.sub(r"background:#ffffff(?=')", 'background:#F4EFE6', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    html_files = glob.glob(os.path.join(REPO, "**/*.html"), recursive=True)
    html_files += glob.glob(os.path.join(REPO, "*.html"))
    # Dedupe
    html_files = list(set(html_files))
    html_files.sort()

    changed = 0
    skipped = 0
    for fp in html_files:
        result = process_file(fp)
        if result:
            changed += 1
            print(f"  ✓ {fp.replace(REPO + '/', '')}")
        else:
            skipped += 1
            print(f"  - {fp.replace(REPO + '/', '')} (no changes)")

    print(f"\n✅ Done. {changed} files updated, {skipped} unchanged.")


if __name__ == "__main__":
    main()
