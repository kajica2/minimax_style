#!/usr/bin/env python3
"""Generate 5 alternate MiniMax style guides as style-1.html .. style-5.html.

Each variant keeps the same 14-section structure (intro/voice/color/type/space/radius/
shadow/buttons/badges/cards/inputs/icons/hero/footer/dodont) and the same content as
the original index.html. Only the visual system changes: tokens, typefaces, layout
density, radii, shadows.

Run: python3 build_styles.py
Outputs: ./style-1.html ... ./style-5.html
"""
import os, re, html

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---- shared content (lifted from the original index.html, kept in one place) ----
ICON_SVG = """<svg viewBox='0 0 24 24'><path d='M4 6h16M4 12h16M4 18h10'/></svg>"""
ICONS = [
    "<svg viewBox='0 0 24 24'><path d='M4 6h16M4 12h16M4 18h10'/></svg>",
    "<svg viewBox='0 0 24 24'><circle cx='11' cy='11' r='7'/><path d='M21 21l-4.3-4.3'/></svg>",
    "<svg viewBox='0 0 24 24'><path d='M12 2l2.4 5 5.6.8-4 3.9 1 5.6L12 14.8 6.9 17.3l1-5.6-4-3.9 5.6-.8z'/></svg>",
    "<svg viewBox='0 0 24 24'><path d='M20 6L9 17l-5-5'/></svg>",
    "<svg viewBox='0 0 24 24'><path d='M5 12h14M12 5l7 7-7 7'/></svg>",
    "<svg viewBox='0 0 24 24'><rect x='3' y='3' width='18' height='18' rx='3'/><path d='M3 9h18M9 21V9'/></svg>",
    "<svg viewBox='0 0 24 24'><path d='M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z'/></svg>",
    "<svg viewBox='0 0 24 24'><circle cx='12' cy='12' r='9'/><path d='M12 7v5l3 2'/></svg>",
    "<svg viewBox='0 0 24 24'><path d='M4 19h16M4 5h16M9 12h6'/></svg>",
    "<svg viewBox='0 0 24 24'><path d='M12 2v20M2 12h20'/></svg>",
    "<svg viewBox='0 0 24 24'><path d='M3 12a9 9 0 1018 0 9 9 0 00-18 0z'/><path d='M9 12l2 2 4-4'/></svg>",
    "<svg viewBox='0 0 24 24'><path d='M6 6l12 12M18 6L6 18'/></svg>",
    "<svg viewBox='0 0 24 24'><path d='M3 7l9-4 9 4-9 4-9-4z'/><path d='M3 12l9 4 9-4M3 17l9 4 9-4'/></svg>",
    "<svg viewBox='0 0 24 24'><path d='M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z'/><circle cx='12' cy='12' r='3'/></svg>",
    "<svg viewBox='0 0 24 24'><path d='M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5'/></svg>",
    "<svg viewBox='0 0 24 24'><rect x='4' y='4' width='16' height='16' rx='2'/><path d='M9 9h6v6H9z'/></svg>",
]
ICON_GRID = "\n".join(f"<div class='icon-tile'>{s}</div>" for s in ICONS)


# ---- 5 style systems ----

def style_noir():
    """1 · Noir — pure B/W, sharp corners, mono display."""
    return {
        "slug": "noir",
        "name": "Noir",
        "tag": "Monochrome · sharp · terminal-zine",
        "fonts": "IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap",
        "css": r"""
:root{
  --canvas:#ffffff;--surface:#fafafa;--surface-soft:#f2f2f2;
  --ink:#000000;--ink-2:#0a0a0a;--charcoal:#1a1a1a;--slate:#3a3a3a;--steel:#6a6a6a;--stone:#8a8a8a;--muted:#b0b0b0;
  --hairline:#000000;--hairline-soft:#cccccc;
  --accent:#000000;--accent-2:#ff0033;--accent-3:#0033ff;
  --shadow-card:0 0 0 1px #000;--shadow-glow:none;
  --r-xs:0;--r-sm:0;--r-md:0;--r-lg:0;--r-xl:0;--r-pill:0;
  --font-display:'IBM Plex Mono',monospace;--font-body:'IBM Plex Sans',sans-serif;--font-mono:'IBM Plex Mono',monospace;
}
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{font-family:var(--font-body);background:var(--canvas);color:var(--ink);line-height:1.55;-webkit-font-smoothing:antialiased}
code,pre,.mono{font-family:var(--font-mono)}
.shell{display:grid;grid-template-columns:240px 1fr;min-height:100vh}
nav.side{position:sticky;top:0;align-self:start;height:100vh;overflow:auto;border-right:2px solid var(--ink);background:var(--canvas);padding:24px 18px}
nav.side .brand{display:flex;align-items:center;gap:10px;margin-bottom:24px;padding-bottom:18px;border-bottom:2px solid var(--ink)}
nav.side .logo{width:30px;height:30px;background:#000;color:#fff;display:grid;place-items:center;font-weight:700;font-family:var(--font-display);font-size:14px}
nav.side .brand-name{font-family:var(--font-display);font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:0.04em}
nav.side .brand-sub{font-size:10.5px;color:var(--slate);margin-top:2px;font-family:var(--font-mono)}
nav.side .group{font-size:10px;text-transform:uppercase;letter-spacing:0.16em;color:#000;margin:18px 0 8px;font-weight:700;border-bottom:1px solid #000;padding-bottom:4px}
nav.side a{display:block;padding:6px 8px;color:var(--ink);text-decoration:none;font-size:12.5px;font-family:var(--font-mono);border-left:2px solid transparent}
nav.side a:hover{background:#000;color:#fff}
nav.side a.active{background:#000;color:#fff;border-left:2px solid var(--accent-2)}
main{padding:48px 56px 100px;max-width:1080px}
section{margin-bottom:80px;scroll-margin-top:24px}
h1.doc-title{font-family:var(--font-display);font-size:56px;font-weight:700;letter-spacing:-0.03em;line-height:1;margin:0 0 14px;text-transform:uppercase}
.doc-kicker{font-size:11px;text-transform:uppercase;letter-spacing:0.18em;color:#000;margin-bottom:8px;font-family:var(--font-mono);font-weight:600;border:1px solid #000;padding:3px 8px;display:inline-block}
.doc-lead{color:var(--charcoal);font-size:15px;max-width:700px;margin:0 0 40px;line-height:1.6}
h2.section{font-family:var(--font-display);font-size:26px;font-weight:700;letter-spacing:-0.01em;margin:0 0 6px;text-transform:uppercase;border-bottom:3px double #000;padding-bottom:8px;display:flex;align-items:baseline;gap:14px}
h2.section .num{font-family:var(--font-mono);font-size:12px;color:#000;font-weight:700;background:#000;color:#fff;padding:2px 6px}
.section-blurb{color:var(--slate);font-size:14px;margin:12px 0 24px;max-width:640px;line-height:1.55}
h3{font-family:var(--font-display);font-size:15px;font-weight:700;margin:28px 0 12px;text-transform:uppercase;letter-spacing:0.04em;border-bottom:1px solid #000;padding-bottom:4px}
hr.rule{border:0;border-top:2px solid #000;margin:36px 0}
.swatches{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px}
.swatch{border:1px solid #000;background:#fff;overflow:hidden}
.swatch .chip{height:88px;border-bottom:1px solid #000}
.swatch .meta{padding:10px 12px}
.swatch .name{font-weight:700;font-size:12.5px;font-family:var(--font-display);text-transform:uppercase}
.swatch .hex{font-family:var(--font-mono);font-size:11px;color:var(--slate);margin-top:2px}
.swatch .role{font-size:11px;color:var(--steel);margin-top:5px}
.type-row{display:grid;grid-template-columns:200px 1fr;gap:24px;align-items:baseline;padding:18px 0;border-bottom:1px dashed #000}
.type-row:last-child{border-bottom:0}
.type-meta .name{font-weight:700;font-size:12px;font-family:var(--font-display);text-transform:uppercase}
.type-meta .token{font-family:var(--font-mono);font-size:11px;color:var(--slate);margin-top:2px}
.type-meta .use{font-size:11px;color:var(--steel);margin-top:5px}
.specimen-display{font-family:var(--font-display);font-weight:700;font-size:60px;line-height:1;letter-spacing:-0.03em;text-transform:uppercase}
.specimen-h1{font-family:var(--font-display);font-weight:700;font-size:42px;line-height:1.05;letter-spacing:-0.02em;text-transform:uppercase}
.specimen-h2{font-family:var(--font-display);font-weight:700;font-size:26px;line-height:1.1;letter-spacing:-0.01em;text-transform:uppercase}
.specimen-h3{font-family:var(--font-body);font-weight:700;font-size:18px;line-height:1.3}
.specimen-body{font-family:var(--font-body);font-weight:400;font-size:15px;line-height:1.65}
.specimen-medium{font-family:var(--font-body);font-weight:600;font-size:15px}
.specimen-small{font-family:var(--font-body);font-weight:400;font-size:13px;color:var(--slate)}
.specimen-caption{font-family:var(--font-body);font-weight:400;font-size:12px;color:var(--steel)}
.specimen-mono{font-family:var(--font-mono);font-size:12px;color:var(--ink)}
.space-rows{display:flex;flex-direction:column;gap:2px}
.space-row{display:grid;grid-template-columns:90px 1fr 60px;align-items:center;gap:16px;padding:6px 0;border-bottom:1px dashed #ccc}
.space-row .lbl{font-family:var(--font-mono);font-size:11.5px;color:var(--ink);font-weight:600}
.space-row .bar{background:#000;height:8px}
.space-row .val{font-family:var(--font-mono);font-size:11px;color:var(--ink);text-align:right;font-weight:600}
.radius-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:14px}
.radius-tile{text-align:left;border:1px solid #000;padding:10px}
.radius-tile .box{width:100%;aspect-ratio:1.2;background:#000;margin-bottom:8px}
.radius-tile .lbl{font-weight:700;font-size:11.5px;font-family:var(--font-display);text-transform:uppercase}
.radius-tile .tok{font-family:var(--font-mono);font-size:11px;color:var(--slate)}
.shadow-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:20px}
.shadow-tile{background:#fff;padding:24px;border:1px solid #000}
.shadow-tile .lbl{font-weight:700;font-size:12.5px;margin-top:14px;font-family:var(--font-display);text-transform:uppercase}
.shadow-tile .tok{font-family:var(--font-mono);font-size:11px;color:var(--slate)}
.shadow-card-tile{box-shadow:6px 6px 0 #000}
.shadow-glow-tile{box-shadow:-6px 6px 0 var(--accent-2)}
.shadow-glow2-tile{box-shadow:6px -6px 0 var(--accent-3)}
.btn-row{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:14px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 18px;font-family:var(--font-mono);font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:0.04em;border:1px solid #000;cursor:pointer;text-decoration:none;background:#fff;color:#000;transition:none}
.btn:hover{background:#000;color:#fff}
.btn-primary{background:#000;color:#fff}
.btn-primary:hover{background:#fff;color:#000}
.btn-secondary{background:#fff;color:#000}
.btn-coral{background:var(--accent-2);color:#fff;border-color:#000}
.btn-coral:hover{background:#fff;color:var(--accent-2)}
.btn-magenta{background:#ff00aa;color:#fff;border-color:#000}
.btn-blue{background:var(--accent-3);color:#fff;border-color:#000}
.btn-purple{background:#6600ff;color:#fff;border-color:#000}
.btn-square{border-radius:0}
.btn-lg{padding:14px 22px;font-size:14px}
.btn-sm{padding:7px 12px;font-size:11.5px}
.btn-block{display:flex;width:100%;justify-content:center}
.pill{display:inline-flex;align-items:center;gap:6px;padding:4px 10px;font-size:11px;font-weight:600;background:#fff;color:#000;border:1px solid #000;font-family:var(--font-mono);text-transform:uppercase;letter-spacing:0.04em}
.pill .dot{width:6px;height:6px;background:#000}
.pill.coral{background:var(--accent-2);color:#fff;border-color:#000}.pill.coral .dot{background:#fff}
.pill.magenta{background:#ff00aa;color:#fff;border-color:#000}.pill.magenta .dot{background:#fff}
.pill.blue{background:var(--accent-3);color:#fff;border-color:#000}.pill.blue .dot{background:#fff}
.pill.purple{background:#6600ff;color:#fff;border-color:#000}.pill.purple .dot{background:#fff}
.pill.success{background:#000;color:#00ff66;border-color:#000}.pill.success .dot{background:#00ff66}
.card-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.card{border:1px solid #000;background:#fff;padding:18px}
.card .card-kicker{font-size:10.5px;text-transform:uppercase;letter-spacing:0.14em;color:#000;font-weight:700;font-family:var(--font-mono);background:#000;color:#fff;padding:2px 6px;display:inline-block}
.card .card-title{font-family:var(--font-display);font-weight:700;font-size:19px;margin:8px 0 6px;text-transform:uppercase;letter-spacing:-0.01em}
.card .card-body{font-size:13px;color:var(--slate);line-height:1.5}
.product-card{border:1px solid #000;padding:24px;color:#fff;min-height:170px;display:flex;flex-direction:column;justify-content:space-between;background:#000}
.product-card .model{font-family:var(--font-display);font-weight:700;font-size:24px;letter-spacing:-0.01em;text-transform:uppercase}
.product-card .sub{font-size:12px;opacity:0.9;margin-top:4px;font-family:var(--font-mono);text-transform:uppercase;letter-spacing:0.05em}
.pc-coral{background:var(--accent-2)}.pc-magenta{background:#ff00aa}.pc-blue{background:var(--accent-3)}.pc-purple{background:#6600ff;color:#fff}
.field{display:flex;flex-direction:column;gap:5px;max-width:340px}
.field label{font-size:11px;color:#000;font-weight:700;font-family:var(--font-mono);text-transform:uppercase;letter-spacing:0.06em}
.input{padding:9px 12px;border:1px solid #000;background:#fff;font-size:13.5px;color:#000;font-family:var(--font-mono);outline:none}
.input:focus{border-color:#000;box-shadow:4px 4px 0 #000}
.input.square{border-radius:0}
.icon-grid{display:grid;grid-template-columns:repeat(8,1fr);gap:6px}
.icon-tile{aspect-ratio:1;display:grid;place-items:center;background:#fff;border:1px solid #000}
.icon-tile svg{width:22px;height:22px;stroke:#000;fill:none;stroke-width:1.8}
.dodont{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.dodont .item{padding:16px;border:1px solid #000;background:#fff}
.dodont .do{border-left:4px solid #000}
.dodont .dont{border-left:4px solid var(--accent-2)}
.dodont .head{font-weight:700;font-size:11.5px;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;font-family:var(--font-mono)}
.dodont .do .head{color:#000}.dodont .dont .head{color:var(--accent-2)}
.dodont .item p{margin:0;font-size:13px;color:var(--ink);line-height:1.5}
table.tokens{width:100%;border-collapse:collapse;font-size:12.5px;border:1px solid #000}
table.tokens th,table.tokens td{text-align:left;padding:9px 11px;border-bottom:1px solid #000}
table.tokens th{font-size:10.5px;text-transform:uppercase;letter-spacing:0.1em;color:#fff;font-weight:700;background:#000}
table.tokens td.mono{font-family:var(--font-mono);font-size:11.5px}
table.tokens td .swatch-mini{display:inline-block;width:12px;height:12px;vertical-align:middle;margin-right:6px;border:1px solid #000}
.hero-band{background:#000;color:#fff;border:1px solid #000;padding:60px 50px;margin-bottom:32px;position:relative;overflow:hidden}
.hero-band::before{content:"";position:absolute;left:-2px;top:0;bottom:0;width:6px;background:var(--accent-2)}
.hero-band::after{content:"";position:absolute;right:24px;top:24px;font-family:var(--font-mono);font-size:11px;color:var(--accent-2);content:"// 2026";opacity:0}
.hero-band h1{font-family:var(--font-display);font-size:72px;font-weight:700;letter-spacing:-0.03em;line-height:0.95;margin:0;position:relative;z-index:1;text-transform:uppercase}
.hero-band p{font-size:15px;color:#aaa;max-width:520px;margin:18px 0 26px;position:relative;z-index:1;line-height:1.5}
.hero-band .cta-row{display:flex;gap:10px;position:relative;z-index:1}
.hero-band .btn-primary{background:#fff;color:#000;border-color:#fff}
.hero-band .btn-secondary{background:transparent;color:#fff;border-color:#fff}
.tag{display:inline-block;font-size:10.5px;padding:2px 8px;background:#000;color:#fff;font-family:var(--font-mono);text-transform:uppercase;letter-spacing:0.06em;font-weight:600}
.footer-block{background:#000;color:#fff;border:1px solid #000;padding:48px;margin-top:32px}
.footer-block h3{color:#fff;font-family:var(--font-display);font-size:20px;margin:0 0 18px;text-transform:uppercase;letter-spacing:-0.01em}
.footer-block .links{display:grid;grid-template-columns:repeat(4,1fr);gap:28px}
.footer-block .col h4{font-size:10.5px;text-transform:uppercase;letter-spacing:0.14em;color:#999;margin:0 0 12px;font-weight:700;font-family:var(--font-mono)}
.footer-block .col a{display:block;color:#ccc;text-decoration:none;font-size:13px;padding:4px 0}
.footer-block .col a:hover{color:#fff;background:#222;padding-left:6px}
@media (max-width:860px){.shell{grid-template-columns:1fr}nav.side{position:relative;height:auto;border-right:0;border-bottom:2px solid #000}main{padding:32px 20px 80px}.hero-band h1{font-size:42px}}
        """,
        "nav_active": "01",  # brand voice
        "swatches": {
            "surface": [
                ("Canvas", "#ffffff", "Page bg, card surfaces", "#ffffff"),
                ("Surface", "#fafafa", "Section bg", "#fafafa"),
                ("Surface Soft", "#f2f2f2", "Quieter sections", "#f2f2f2"),
                ("Footer", "#000000", "Dark footer, dense", "#000000"),
                ("Surface Deep", "#000000", "Hero bands, inverse UI", "#000000"),
            ],
            "ink": [
                ("Ink", "#000000", "Headlines, CTAs", "#000000"),
                ("Ink 2", "#0a0a0a", "Primary text", "#0a0a0a"),
                ("Charcoal", "#1a1a1a", "Body text", "#1a1a1a"),
                ("Slate", "#3a3a3a", "Secondary text", "#3a3a3a"),
                ("Steel", "#6a6a6a", "Tertiary", "#6a6a6a"),
                ("Stone", "#8a8a8a", "Muted captions", "#8a8a8a"),
                ("Muted", "#b0b0b0", "Footer links", "#b0b0b0"),
            ],
            "hairline": [
                ("Hairline", "#000000", "Borders", "#000000"),
                ("Hairline Soft", "#cccccc", "Quiet dividers", "#cccccc"),
            ],
            "brand": [
                ("Accent", "#000000", "Default accent", "#000000"),
                ("Accent 2", "#ff0033", "Warning / dont", "#ff0033"),
                ("Accent 3", "#0033ff", "Info / link", "#0033ff"),
                ("Brand Magenta", "#ff00aa", "Music 2.6 identity", "#ff00aa"),
                ("Brand Purple", "#6600ff", "Speech 2.8 identity", "#6600ff"),
            ],
            "semantic": [
                ("Success", "#00ff66", "Inline success", "#00ff66"),
                ("Success BG", "#000000", "Badge bg (on dark)", "#000000"),
                ("Error", "#ff0033", "Destructive, error", "#ff0033"),
            ],
        },
    }


def style_aurora():
    """2 · Aurora — pastel gradients, 28px radii, glass blur."""
    return {
        "slug": "aurora",
        "name": "Aurora",
        "tag": "Pastel · glass · friendly",
        "fonts": "Nunito:wght@400;500;600;700;800&family=Quicksand:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap",
        "css": r"""
:root{
  --canvas:#fdfcff;--surface:#f5f1ff;--surface-soft:#ece6ff;
  --surface-deep:#3a2f5e;
  --ink:#2d2454;--ink-2:#3a2f5e;--charcoal:#4a3f70;--slate:#6b5f95;--steel:#8a7eb5;--stone:#a89cc8;--muted:#c4b8e0;
  --hairline:#d8c8f5;--hairline-soft:#e6daf8;
  --brand-coral:#ff9eb5;--brand-magenta:#d8a8ff;--brand-blue:#a8c8ff;--brand-cyan:#9ee5f5;--brand-purple:#c5a8ff;
  --shadow-card:0 8px 24px -8px rgba(140,100,200,0.18), 0 2px 4px rgba(140,100,200,0.08);
  --shadow-glow:0 12px 36px -10px rgba(168,140,255,0.45);
  --shadow-glow2:0 18px 48px -16px rgba(255,158,181,0.5);
  --r-xs:8px;--r-sm:14px;--r-md:22px;--r-lg:28px;--r-xl:36px;--r-pill:9999px;
  --font-display:'Quicksand',sans-serif;--font-body:'Nunito',sans-serif;--font-mono:'JetBrains Mono',monospace;
}
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{font-family:var(--font-body);background:linear-gradient(135deg,#fdfcff 0%,#f5f1ff 60%,#fce8f3 100%);background-attachment:fixed;color:var(--ink);line-height:1.6;-webkit-font-smoothing:antialiased}
code,pre,.mono{font-family:var(--font-mono)}
.shell{display:grid;grid-template-columns:260px 1fr;min-height:100vh}
nav.side{position:sticky;top:0;align-self:start;height:100vh;overflow:auto;background:rgba(255,255,255,0.65);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border-right:1px solid var(--hairline);padding:26px 20px}
nav.side .brand{display:flex;align-items:center;gap:11px;margin-bottom:26px;padding-bottom:20px;border-bottom:1px solid var(--hairline)}
nav.side .logo{width:36px;height:36px;border-radius:14px;background:linear-gradient(135deg,var(--brand-magenta),var(--brand-blue));display:grid;place-items:center;color:#fff;font-weight:800;font-size:15px;font-family:var(--font-display);box-shadow:var(--shadow-glow)}
nav.side .brand-name{font-family:var(--font-display);font-weight:700;font-size:16px;letter-spacing:-0.01em;color:var(--ink)}
nav.side .brand-sub{font-size:11.5px;color:var(--slate);margin-top:2px}
nav.side .group{font-size:10.5px;text-transform:uppercase;letter-spacing:0.1em;color:var(--stone);margin:18px 8px 8px;font-weight:700}
nav.side a{display:block;padding:8px 12px;border-radius:14px;color:var(--charcoal);text-decoration:none;font-size:13.5px;transition:all 0.2s ease}
nav.side a:hover{background:var(--surface-soft);color:var(--ink)}
nav.side a.active{background:linear-gradient(135deg,var(--brand-magenta),var(--brand-blue));color:#fff;font-weight:600;box-shadow:var(--shadow-glow)}
main{padding:54px 62px 110px;max-width:1100px}
section{margin-bottom:90px;scroll-margin-top:24px}
h1.doc-title{font-family:var(--font-display);font-size:58px;font-weight:700;letter-spacing:-0.025em;line-height:1.05;margin:0 0 12px;color:var(--ink)}
.doc-kicker{font-size:11.5px;text-transform:uppercase;letter-spacing:0.14em;color:var(--brand-purple);margin-bottom:8px;font-weight:700}
.doc-lead{color:var(--charcoal);font-size:16px;max-width:720px;margin:0 0 44px;line-height:1.6}
h2.section{font-family:var(--font-display);font-size:30px;font-weight:700;letter-spacing:-0.018em;margin:0 0 8px;color:var(--ink);display:flex;align-items:baseline;gap:14px}
h2.section .num{font-family:var(--font-mono);font-size:12px;color:var(--brand-purple);font-weight:700;background:var(--surface-soft);padding:4px 10px;border-radius:var(--r-pill)}
.section-blurb{color:var(--slate);font-size:14.5px;margin:0 0 26px;max-width:640px;line-height:1.6}
h3{font-family:var(--font-display);font-size:17px;font-weight:700;margin:30px 0 14px;color:var(--ink)}
hr.rule{border:0;border-top:1px solid var(--hairline);margin:38px 0}
.swatches{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px}
.swatch{border:1px solid var(--hairline);border-radius:var(--r-md);overflow:hidden;background:rgba(255,255,255,0.7);backdrop-filter:blur(8px)}
.swatch .chip{height:96px;border-bottom:1px solid var(--hairline-soft)}
.swatch .meta{padding:12px 14px}
.swatch .name{font-weight:700;font-size:13px}
.swatch .hex{font-family:var(--font-mono);font-size:11.5px;color:var(--slate);margin-top:2px}
.swatch .role{font-size:11px;color:var(--stone);margin-top:6px}
.type-row{display:grid;grid-template-columns:200px 1fr;gap:24px;align-items:baseline;padding:22px 0;border-bottom:1px solid var(--hairline-soft)}
.type-row:last-child{border-bottom:0}
.type-meta .name{font-weight:700;font-size:13px}
.type-meta .token{font-family:var(--font-mono);font-size:11.5px;color:var(--slate);margin-top:2px}
.type-meta .use{font-size:11.5px;color:var(--stone);margin-top:6px}
.specimen-display{font-family:var(--font-display);font-weight:700;font-size:62px;line-height:1.1;letter-spacing:-0.025em;color:var(--ink)}
.specimen-h1{font-family:var(--font-display);font-weight:700;font-size:42px;line-height:1.15;letter-spacing:-0.02em}
.specimen-h2{font-family:var(--font-display);font-weight:700;font-size:28px;line-height:1.2;letter-spacing:-0.015em}
.specimen-h3{font-family:var(--font-body);font-weight:700;font-size:20px;line-height:1.3}
.specimen-body{font-family:var(--font-body);font-weight:400;font-size:16px;line-height:1.65}
.specimen-medium{font-family:var(--font-body);font-weight:600;font-size:16px}
.specimen-small{font-family:var(--font-body);font-weight:400;font-size:14px;color:var(--slate)}
.specimen-caption{font-family:var(--font-body);font-weight:400;font-size:13px;color:var(--stone)}
.specimen-mono{font-family:var(--font-mono);font-size:13px;color:var(--charcoal)}
.space-rows{display:flex;flex-direction:column;gap:4px}
.space-row{display:grid;grid-template-columns:80px 1fr 60px;align-items:center;gap:16px;padding:8px 0}
.space-row .lbl{font-family:var(--font-mono);font-size:12px;color:var(--slate)}
.space-row .bar{background:linear-gradient(90deg,var(--brand-magenta),var(--brand-blue));height:10px;border-radius:var(--r-pill)}
.space-row .val{font-family:var(--font-mono);font-size:12px;color:var(--stone);text-align:right}
.radius-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:18px}
.radius-tile{text-align:center}
.radius-tile .box{width:100%;aspect-ratio:1.2;background:linear-gradient(135deg,var(--brand-magenta),var(--brand-blue));margin-bottom:10px;box-shadow:var(--shadow-glow)}
.radius-tile .lbl{font-weight:700;font-size:12.5px}
.radius-tile .tok{font-family:var(--font-mono);font-size:11px;color:var(--slate)}
.shadow-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:24px}
.shadow-tile{background:rgba(255,255,255,0.8);backdrop-filter:blur(10px);padding:28px;border-radius:var(--r-md);border:1px solid var(--hairline-soft)}
.shadow-tile .lbl{font-weight:700;font-size:13px;margin-top:14px}
.shadow-tile .tok{font-family:var(--font-mono);font-size:11px;color:var(--slate)}
.shadow-card-tile{box-shadow:var(--shadow-card)}
.shadow-glow-tile{box-shadow:var(--shadow-glow)}
.shadow-glow2-tile{box-shadow:var(--shadow-glow2)}
.btn-row{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-bottom:16px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:11px 20px;font-family:var(--font-body);font-weight:600;font-size:14px;border:1px solid transparent;cursor:pointer;transition:all 0.2s ease;text-decoration:none;border-radius:var(--r-pill)}
.btn-primary{background:linear-gradient(135deg,var(--brand-magenta),var(--brand-blue));color:#fff;box-shadow:var(--shadow-glow)}
.btn-primary:hover{transform:translateY(-1px);box-shadow:0 16px 40px -10px rgba(168,140,255,0.55)}
.btn-secondary{background:rgba(255,255,255,0.7);color:var(--ink);border:1px solid var(--hairline);backdrop-filter:blur(8px)}
.btn-secondary:hover{background:#fff;border-color:var(--brand-magenta)}
.btn-coral{background:linear-gradient(135deg,#ffb3c1,#ff9eb5);color:#fff}
.btn-magenta{background:linear-gradient(135deg,#e0b3ff,#d8a8ff);color:#fff}
.btn-blue{background:linear-gradient(135deg,#b3d4ff,#a8c8ff);color:#fff}
.btn-purple{background:linear-gradient(135deg,#d4b3ff,#c5a8ff);color:#fff}
.btn-square{border-radius:var(--r-sm)}
.btn-lg{padding:14px 26px;font-size:15px}
.btn-sm{padding:8px 16px;font-size:13px}
.btn-block{display:flex;width:100%;justify-content:center}
.pill{display:inline-flex;align-items:center;gap:6px;padding:5px 14px;font-size:12px;font-weight:600;border-radius:var(--r-pill);background:rgba(255,255,255,0.7);color:var(--charcoal);backdrop-filter:blur(8px);border:1px solid var(--hairline-soft)}
.pill .dot{width:6px;height:6px;border-radius:50%;background:var(--brand-blue)}
.pill.coral{background:rgba(255,158,181,0.2);color:#c4527a}
.pill.coral .dot{background:#ff9eb5}
.pill.magenta{background:rgba(216,168,255,0.25);color:#7a4ec4}
.pill.magenta .dot{background:#d8a8ff}
.pill.blue{background:rgba(168,200,255,0.25);color:#4a6ec4}
.pill.purple{background:rgba(197,168,255,0.3);color:#6e4ec4}
.pill.purple .dot{background:#c5a8ff}
.pill.success{background:rgba(154,225,180,0.25);color:#3a8a5e}
.pill.success .dot{background:#6ed4a0}
.card-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px}
.card{border-radius:var(--r-md);background:rgba(255,255,255,0.75);border:1px solid var(--hairline-soft);padding:22px;backdrop-filter:blur(10px);box-shadow:var(--shadow-card)}
.card .card-kicker{font-size:10.5px;text-transform:uppercase;letter-spacing:0.12em;color:var(--brand-purple);font-weight:700}
.card .card-title{font-family:var(--font-display);font-weight:700;font-size:20px;margin:8px 0 8px;color:var(--ink)}
.card .card-body{font-size:13.5px;color:var(--slate);line-height:1.55}
.product-card{border-radius:var(--r-xl);padding:28px;color:#fff;min-height:180px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:var(--shadow-glow)}
.product-card .model{font-family:var(--font-display);font-weight:700;font-size:26px;letter-spacing:-0.01em}
.product-card .sub{font-size:13px;opacity:0.92;margin-top:4px;font-weight:500}
.pc-coral{background:linear-gradient(135deg,#ffb3c1 0%,#ffd6e0 100%)}
.pc-magenta{background:linear-gradient(135deg,#e0b3ff 0%,#f0d6ff 100%)}
.pc-blue{background:linear-gradient(135deg,#b3d4ff 0%,#d0e4ff 100%)}
.pc-purple{background:linear-gradient(135deg,#d4b3ff 0%,#e8d4ff 100%)}
.field{display:flex;flex-direction:column;gap:6px;max-width:360px}
.field label{font-size:12.5px;color:var(--slate);font-weight:600}
.input{padding:11px 16px;border-radius:var(--r-pill);border:1px solid var(--hairline);background:rgba(255,255,255,0.7);backdrop-filter:blur(8px);font-size:14px;color:var(--ink);font-family:var(--font-body);outline:none}
.input:focus{border-color:var(--brand-magenta);box-shadow:0 0 0 4px rgba(216,168,255,0.25)}
.input.square{border-radius:var(--r-sm)}
.icon-grid{display:grid;grid-template-columns:repeat(8,1fr);gap:8px}
.icon-tile{aspect-ratio:1;display:grid;place-items:center;background:rgba(255,255,255,0.6);border:1px solid var(--hairline-soft);border-radius:var(--r-sm);backdrop-filter:blur(8px)}
.icon-tile svg{width:22px;height:22px;stroke:var(--ink);fill:none;stroke-width:1.6}
.dodont{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.dodont .item{padding:18px;border-radius:var(--r-md);border:1px solid var(--hairline-soft)}
.dodont .do{background:rgba(154,225,180,0.18);border-color:rgba(154,225,180,0.5)}
.dodont .dont{background:rgba(255,158,181,0.15);border-color:rgba(255,158,181,0.5)}
.dodont .head{font-weight:700;font-size:12px;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px}
.dodont .do .head{color:#3a8a5e}
.dodont .dont .head{color:#c4527a}
.dodont .item p{margin:0;font-size:13.5px;color:var(--charcoal);line-height:1.55}
table.tokens{width:100%;border-collapse:collapse;font-size:13.5px;background:rgba(255,255,255,0.6);border-radius:var(--r-md);overflow:hidden;border:1px solid var(--hairline-soft)}
table.tokens th,table.tokens td{text-align:left;padding:11px 14px;border-bottom:1px solid var(--hairline-soft)}
table.tokens th{font-size:11px;text-transform:uppercase;letter-spacing:0.08em;color:var(--brand-purple);font-weight:700;background:var(--surface-soft)}
table.tokens td.mono{font-family:var(--font-mono);font-size:12.5px}
table.tokens td .swatch-mini{display:inline-block;width:14px;height:14px;border-radius:50%;vertical-align:middle;margin-right:8px;border:1px solid var(--hairline)}
.hero-band{background:linear-gradient(135deg,#3a2f5e 0%,#5e4a8e 50%,#8a6ec4 100%);color:#fff;border-radius:var(--r-xl);padding:64px 56px;margin-bottom:32px;position:relative;overflow:hidden;box-shadow:var(--shadow-glow)}
.hero-band::after{content:"";position:absolute;right:-80px;top:-80px;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(255,200,230,0.35) 0%,transparent 70%)}
.hero-band h1{font-family:var(--font-display);font-size:72px;font-weight:700;letter-spacing:-0.03em;line-height:1.05;margin:0;position:relative;z-index:1}
.hero-band p{font-size:16px;color:rgba(255,255,255,0.85);max-width:540px;margin:18px 0 28px;position:relative;z-index:1;line-height:1.6}
.hero-band .cta-row{display:flex;gap:10px;position:relative;z-index:1}
.hero-band .btn-primary{background:rgba(255,255,255,0.95);color:var(--ink)}
.hero-band .btn-secondary{background:transparent;border-color:rgba(255,255,255,0.4);color:#fff}
.tag{display:inline-block;font-size:11px;padding:3px 10px;border-radius:var(--r-pill);background:var(--brand-blue);color:#fff;font-weight:600}
.footer-block{background:linear-gradient(135deg,#3a2f5e,#5e4a8e);color:#fff;border-radius:var(--r-xl);padding:54px;margin-top:36px;box-shadow:var(--shadow-glow)}
.footer-block h3{color:#fff;font-family:var(--font-display);font-size:20px;margin:0 0 16px;font-weight:700}
.footer-block .links{display:grid;grid-template-columns:repeat(4,1fr);gap:32px}
.footer-block .col h4{font-size:11px;text-transform:uppercase;letter-spacing:0.12em;color:rgba(255,255,255,0.6);margin:0 0 12px;font-weight:700}
.footer-block .col a{display:block;color:rgba(255,255,255,0.82);text-decoration:none;font-size:13.5px;padding:4px 0;border-radius:8px;padding-left:8px;margin-left:-8px}
.footer-block .col a:hover{color:#fff;background:rgba(255,255,255,0.1)}
@media (max-width:860px){.shell{grid-template-columns:1fr}nav.side{position:relative;height:auto}main{padding:32px 20px 80px}.hero-band h1{font-size:42px}}
        """,
        "nav_active": "01",
        "swatches": {
            "surface": [
                ("Canvas", "#fdfcff", "Page bg", "#fdfcff"),
                ("Surface", "#f5f1ff", "Section bg", "#f5f1ff"),
                ("Surface Soft", "#ece6ff", "Quieter sections", "#ece6ff"),
                ("Footer", "#3a2f5e", "Dark footer", "#3a2f5e"),
                ("Surface Deep", "#3a2f5e", "Hero bands", "#3a2f5e"),
            ],
            "ink": [
                ("Ink", "#2d2454", "Headlines, CTAs", "#2d2454"),
                ("Ink 2", "#3a2f5e", "Primary text", "#3a2f5e"),
                ("Charcoal", "#4a3f70", "Body text", "#4a3f70"),
                ("Slate", "#6b5f95", "Secondary text", "#6b5f95"),
                ("Steel", "#8a7eb5", "Tertiary", "#8a7eb5"),
                ("Stone", "#a89cc8", "Muted captions", "#a89cc8"),
                ("Muted", "#c4b8e0", "Footer links", "#c4b8e0"),
            ],
            "hairline": [
                ("Hairline", "#d8c8f5", "Borders", "#d8c8f5"),
                ("Hairline Soft", "#e6daf8", "Quiet dividers", "#e6daf8"),
            ],
            "brand": [
                ("Brand Coral", "#ff9eb5", "M2.7 identity", "#ff9eb5"),
                ("Brand Magenta", "#d8a8ff", "Music 2.6 identity", "#d8a8ff"),
                ("Brand Blue", "#a8c8ff", "Hailuo / primary", "#a8c8ff"),
                ("Brand Cyan", "#9ee5f5", "Atmospheric", "#9ee5f5"),
                ("Brand Purple", "#c5a8ff", "Speech 2.8 identity", "#c5a8ff"),
            ],
            "semantic": [
                ("Success", "#6ed4a0", "Inline success", "#6ed4a0"),
                ("Success BG", "#e0f5e8", "Success badge bg", "#e0f5e8"),
                ("Error", "#ff9eb5", "Destructive, error", "#ff9eb5"),
            ],
        },
    }


def style_brutalist():
    """3 · Brutalist — neon on cream, sharp corners, thick borders, oversized."""
    return {
        "slug": "brutalist",
        "name": "Brutalist",
        "tag": "Neon · sharp · zine",
        "fonts": "Space+Mono:wght@400;700&family=Inter:wght@400;500;600;700;800;900&display=swap",
        "css": r"""
:root{
  --canvas:#f4ede1;--surface:#ebe1cf;--surface-soft:#e0d4bd;
  --surface-deep:#0a0a0a;
  --ink:#0a0a0a;--ink-2:#1a1a1a;--charcoal:#222;--slate:#444;--steel:#666;--stone:#888;--muted:#aaa;
  --hairline:#0a0a0a;--hairline-soft:#7a6a4a;
  --brand-coral:#ff4500;--brand-magenta:#ff00ff;--brand-blue:#0033ff;--brand-cyan:#00e5ff;--brand-purple:#9d00ff;--brand-yellow:#ffd400;--brand-green:#00ff66;
  --shadow-card:8px 8px 0 #0a0a0a;--shadow-glow:0 0 0 4px #ff4500, 8px 8px 0 #0a0a0a;--shadow-glow2:8px 8px 0 #ff00ff;
  --r-xs:0;--r-sm:0;--r-md:0;--r-lg:0;--r-xl:0;--r-pill:0;
  --font-display:'Space Mono',monospace;--font-body:'Inter',sans-serif;--font-mono:'Space Mono',monospace;
}
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{font-family:var(--font-body);background:var(--canvas);color:var(--ink);line-height:1.5;-webkit-font-smoothing:antialiased;background-image:repeating-linear-gradient(0deg,transparent 0 24px,rgba(0,0,0,0.03) 24px 25px)}
code,pre,.mono{font-family:var(--font-mono)}
.shell{display:grid;grid-template-columns:280px 1fr;min-height:100vh}
nav.side{position:sticky;top:0;align-self:start;height:100vh;overflow:auto;border-right:4px solid var(--ink);background:var(--canvas);padding:24px 20px}
nav.side .brand{display:flex;align-items:center;gap:12px;margin-bottom:24px;padding-bottom:20px;border-bottom:4px solid var(--ink)}
nav.side .logo{width:42px;height:42px;background:var(--brand-yellow);border:3px solid var(--ink);display:grid;place-items:center;color:var(--ink);font-weight:900;font-size:20px;font-family:var(--font-display);box-shadow:4px 4px 0 var(--ink)}
nav.side .brand-name{font-family:var(--font-display);font-weight:700;font-size:18px;letter-spacing:-0.02em;text-transform:uppercase}
nav.side .brand-sub{font-size:11px;color:var(--ink);margin-top:2px;font-family:var(--font-mono);text-transform:uppercase;letter-spacing:0.05em}
nav.side .group{font-size:11px;text-transform:uppercase;letter-spacing:0.14em;color:var(--ink);margin:20px 0 8px;font-weight:800;background:var(--brand-yellow);padding:4px 8px;display:inline-block;border:2px solid var(--ink)}
nav.side a{display:block;padding:8px 12px;color:var(--ink);text-decoration:none;font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:0.02em;border-bottom:2px solid var(--ink);transition:none}
nav.side a:hover{background:var(--ink);color:var(--brand-yellow);padding-left:16px}
nav.side a.active{background:var(--brand-coral);color:#fff;border-bottom:2px solid var(--ink)}
main{padding:50px 60px 110px;max-width:1200px}
section{margin-bottom:88px;scroll-margin-top:24px}
h1.doc-title{font-family:var(--font-display);font-size:72px;font-weight:700;letter-spacing:-0.04em;line-height:0.95;margin:0 0 16px;text-transform:uppercase;color:var(--ink)}
.doc-kicker{font-size:12px;text-transform:uppercase;letter-spacing:0.2em;color:var(--ink);margin-bottom:10px;font-family:var(--font-mono);font-weight:700;background:var(--brand-yellow);padding:4px 10px;display:inline-block;border:3px solid var(--ink)}
.doc-lead{color:var(--ink);font-size:17px;max-width:740px;margin:0 0 44px;line-height:1.5;font-weight:500}
h2.section{font-family:var(--font-display);font-size:36px;font-weight:700;letter-spacing:-0.03em;margin:0 0 10px;text-transform:uppercase;color:var(--ink);display:flex;align-items:baseline;gap:14px}
h2.section .num{font-family:var(--font-display);font-size:14px;color:var(--ink);font-weight:700;background:var(--brand-coral);color:#fff;padding:4px 10px;border:3px solid var(--ink)}
.section-blurb{color:var(--charcoal);font-size:15px;margin:14px 0 28px;max-width:660px;line-height:1.55;font-weight:500}
h3{font-family:var(--font-display);font-size:18px;font-weight:700;margin:30px 0 14px;text-transform:uppercase;letter-spacing:-0.01em;color:var(--ink);background:var(--canvas);padding:6px 12px;border:3px solid var(--ink);display:inline-block}
hr.rule{border:0;border-top:4px solid var(--ink);margin:40px 0}
.swatches{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:14px}
.swatch{border:3px solid var(--ink);background:#fff}
.swatch .chip{height:96px;border-bottom:3px solid var(--ink)}
.swatch .meta{padding:12px 14px}
.swatch .name{font-weight:800;font-size:13.5px;font-family:var(--font-display);text-transform:uppercase;letter-spacing:-0.01em}
.swatch .hex{font-family:var(--font-mono);font-size:12px;color:var(--ink);margin-top:3px;font-weight:700}
.swatch .role{font-size:11px;color:var(--slate);margin-top:6px;font-weight:600}
.type-row{display:grid;grid-template-columns:220px 1fr;gap:24px;align-items:baseline;padding:22px 0;border-bottom:3px solid var(--ink)}
.type-row:last-child{border-bottom:0}
.type-meta .name{font-weight:800;font-size:13px;font-family:var(--font-display);text-transform:uppercase}
.type-meta .token{font-family:var(--font-mono);font-size:11.5px;color:var(--ink);margin-top:3px;font-weight:700}
.type-meta .use{font-size:11.5px;color:var(--slate);margin-top:6px;font-weight:600}
.specimen-display{font-family:var(--font-display);font-weight:700;font-size:72px;line-height:0.95;letter-spacing:-0.04em;text-transform:uppercase;color:var(--ink)}
.specimen-h1{font-family:var(--font-display);font-weight:700;font-size:48px;line-height:1;letter-spacing:-0.03em;text-transform:uppercase}
.specimen-h2{font-family:var(--font-display);font-weight:700;font-size:32px;line-height:1.05;letter-spacing:-0.02em;text-transform:uppercase}
.specimen-h3{font-family:var(--font-body);font-weight:800;font-size:22px;line-height:1.2;text-transform:uppercase;letter-spacing:-0.01em}
.specimen-body{font-family:var(--font-body);font-weight:500;font-size:16px;line-height:1.55}
.specimen-medium{font-family:var(--font-body);font-weight:700;font-size:16px}
.specimen-small{font-family:var(--font-body);font-weight:500;font-size:14px;color:var(--charcoal)}
.specimen-caption{font-family:var(--font-body);font-weight:500;font-size:13px;color:var(--slate)}
.specimen-mono{font-family:var(--font-mono);font-size:13px;color:var(--ink);font-weight:700}
.space-rows{display:flex;flex-direction:column;gap:4px}
.space-row{display:grid;grid-template-columns:100px 1fr 70px;align-items:center;gap:16px;padding:8px 0;border-bottom:2px solid var(--ink)}
.space-row .lbl{font-family:var(--font-display);font-size:12px;color:var(--ink);font-weight:700}
.space-row .bar{background:var(--brand-coral);height:14px;border:2px solid var(--ink)}
.space-row .val{font-family:var(--font-mono);font-size:12px;color:var(--ink);text-align:right;font-weight:700}
.radius-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:16px}
.radius-tile{text-align:center}
.radius-tile .box{width:100%;aspect-ratio:1.2;background:var(--brand-yellow);margin-bottom:10px;border:3px solid var(--ink)}
.radius-tile .lbl{font-weight:800;font-size:13px;font-family:var(--font-display);text-transform:uppercase}
.radius-tile .tok{font-family:var(--font-mono);font-size:11.5px;color:var(--ink);font-weight:700}
.shadow-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:28px}
.shadow-tile{background:#fff;padding:26px;border:3px solid var(--ink)}
.shadow-tile .lbl{font-weight:800;font-size:13.5px;margin-top:14px;font-family:var(--font-display);text-transform:uppercase}
.shadow-tile .tok{font-family:var(--font-mono);font-size:11px;color:var(--ink);font-weight:700}
.shadow-card-tile{box-shadow:var(--shadow-card)}
.shadow-glow-tile{box-shadow:var(--shadow-glow)}
.shadow-glow2-tile{box-shadow:var(--shadow-glow2)}
.btn-row{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-bottom:16px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:12px 22px;font-family:var(--font-display);font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:0.02em;border:3px solid var(--ink);cursor:pointer;text-decoration:none;transition:none;background:var(--canvas);color:var(--ink)}
.btn:hover{transform:translate(-3px,-3px);box-shadow:6px 6px 0 var(--ink)}
.btn-primary{background:var(--brand-yellow);color:var(--ink)}
.btn-secondary{background:#fff;color:var(--ink)}
.btn-coral{background:var(--brand-coral);color:#fff}
.btn-magenta{background:var(--brand-magenta);color:#fff}
.btn-blue{background:var(--brand-blue);color:#fff}
.btn-purple{background:var(--brand-purple);color:#fff}
.btn-square{border-radius:0}
.btn-lg{padding:16px 28px;font-size:15px}
.btn-sm{padding:8px 14px;font-size:12px}
.btn-block{display:flex;width:100%;justify-content:center}
.pill{display:inline-flex;align-items:center;gap:6px;padding:5px 14px;font-size:12px;font-weight:700;background:var(--canvas);color:var(--ink);border:2px solid var(--ink);font-family:var(--font-display);text-transform:uppercase;letter-spacing:0.02em}
.pill .dot{width:8px;height:8px;background:var(--ink)}
.pill.coral{background:var(--brand-coral);color:#fff;border-color:var(--ink)}.pill.coral .dot{background:#fff}
.pill.magenta{background:var(--brand-magenta);color:#fff;border-color:var(--ink)}.pill.magenta .dot{background:#fff}
.pill.blue{background:var(--brand-blue);color:#fff;border-color:var(--ink)}.pill.blue .dot{background:#fff}
.pill.purple{background:var(--brand-purple);color:#fff;border-color:var(--ink)}.pill.purple .dot{background:#fff}
.pill.success{background:var(--brand-green);color:var(--ink);border-color:var(--ink)}.pill.success .dot{background:var(--ink)}
.card-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px}
.card{border:3px solid var(--ink);background:#fff;padding:22px;box-shadow:var(--shadow-card)}
.card .card-kicker{font-size:11px;text-transform:uppercase;letter-spacing:0.14em;color:#fff;font-weight:800;font-family:var(--font-display);background:var(--ink);padding:3px 8px;display:inline-block}
.card .card-title{font-family:var(--font-display);font-weight:700;font-size:22px;margin:10px 0 8px;text-transform:uppercase;letter-spacing:-0.02em;line-height:1.05}
.card .card-body{font-size:13.5px;color:var(--ink);line-height:1.5;font-weight:500}
.product-card{border:3px solid var(--ink);padding:28px;color:#fff;min-height:190px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:var(--shadow-card)}
.product-card .model{font-family:var(--font-display);font-weight:700;font-size:30px;letter-spacing:-0.02em;text-transform:uppercase;line-height:0.95}
.product-card .sub{font-size:13px;margin-top:4px;font-family:var(--font-mono);text-transform:uppercase;letter-spacing:0.06em;font-weight:700}
.pc-coral{background:var(--brand-coral);color:#fff}.pc-magenta{background:var(--brand-magenta);color:#fff}.pc-blue{background:var(--brand-blue);color:#fff}.pc-purple{background:var(--brand-purple);color:#fff}
.field{display:flex;flex-direction:column;gap:6px;max-width:360px}
.field label{font-size:12px;color:var(--ink);font-weight:800;font-family:var(--font-display);text-transform:uppercase;letter-spacing:0.06em}
.input{padding:11px 16px;border:3px solid var(--ink);background:#fff;font-size:14px;color:var(--ink);font-family:var(--font-body);outline:none;font-weight:600}
.input:focus{background:var(--brand-yellow)}
.input.square{border-radius:0}
.icon-grid{display:grid;grid-template-columns:repeat(8,1fr);gap:8px}
.icon-tile{aspect-ratio:1;display:grid;place-items:center;background:#fff;border:3px solid var(--ink)}
.icon-tile svg{width:24px;height:24px;stroke:var(--ink);fill:none;stroke-width:2.4}
.dodont{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.dodont .item{padding:18px;border:3px solid var(--ink);background:#fff}
.dodont .do{background:#e8ffe0}
.dodont .dont{background:#ffe0e0}
.dodont .head{font-weight:800;font-size:12.5px;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;font-family:var(--font-display)}
.dodont .do .head{color:var(--ink);background:var(--brand-green);padding:3px 8px;display:inline-block;border:2px solid var(--ink)}
.dodont .dont .head{color:#fff;background:var(--brand-coral);padding:3px 8px;display:inline-block;border:2px solid var(--ink)}
.dodont .item p{margin:8px 0 0;font-size:13.5px;color:var(--ink);line-height:1.5;font-weight:500}
table.tokens{width:100%;border-collapse:collapse;font-size:13.5px;border:3px solid var(--ink)}
table.tokens th,table.tokens td{text-align:left;padding:11px 13px;border-bottom:2px solid var(--ink)}
table.tokens th{font-size:11px;text-transform:uppercase;letter-spacing:0.1em;color:var(--ink);font-weight:800;font-family:var(--font-display);background:var(--brand-yellow)}
table.tokens td.mono{font-family:var(--font-mono);font-size:12.5px;font-weight:700}
table.tokens td .swatch-mini{display:inline-block;width:14px;height:14px;vertical-align:middle;margin-right:8px;border:2px solid var(--ink)}
.hero-band{background:var(--brand-yellow);color:var(--ink);border:4px solid var(--ink);padding:64px 56px;margin-bottom:32px;position:relative;overflow:hidden;box-shadow:var(--shadow-card)}
.hero-band::after{content:"/// 2026";position:absolute;right:30px;bottom:24px;font-family:var(--font-display);font-size:14px;font-weight:700;color:var(--ink);opacity:0.5}
.hero-band h1{font-family:var(--font-display);font-size:80px;font-weight:700;letter-spacing:-0.04em;line-height:0.92;margin:0;position:relative;z-index:1;text-transform:uppercase;color:var(--ink)}
.hero-band p{font-size:17px;color:var(--ink);max-width:560px;margin:20px 0 30px;position:relative;z-index:1;line-height:1.45;font-weight:600}
.hero-band .cta-row{display:flex;gap:12px;position:relative;z-index:1}
.hero-band .btn-primary{background:var(--ink);color:var(--brand-yellow);border-color:var(--ink)}
.hero-band .btn-secondary{background:transparent;color:var(--ink);border-color:var(--ink)}
.tag{display:inline-block;font-size:11px;padding:3px 10px;background:var(--ink);color:var(--brand-yellow);font-family:var(--font-display);text-transform:uppercase;letter-spacing:0.08em;font-weight:700;border:2px solid var(--ink)}
.footer-block{background:var(--ink);color:var(--brand-yellow);border:4px solid var(--ink);padding:54px;margin-top:36px;box-shadow:var(--shadow-card)}
.footer-block h3{color:var(--brand-yellow);font-family:var(--font-display);font-size:24px;margin:0 0 18px;font-weight:700;text-transform:uppercase;letter-spacing:-0.02em}
.footer-block .links{display:grid;grid-template-columns:repeat(4,1fr);gap:32px}
.footer-block .col h4{font-size:11px;text-transform:uppercase;letter-spacing:0.14em;color:var(--brand-coral);margin:0 0 14px;font-weight:800;font-family:var(--font-display)}
.footer-block .col a{display:block;color:var(--brand-yellow);text-decoration:none;font-size:13.5px;padding:5px 0;font-weight:600;border-bottom:1px solid transparent}
.footer-block .col a:hover{color:#fff;border-bottom:1px solid var(--brand-yellow)}
@media (max-width:860px){.shell{grid-template-columns:1fr}nav.side{position:relative;height:auto;border-right:0;border-bottom:4px solid var(--ink)}main{padding:32px 20px 80px}.hero-band h1{font-size:46px}}
        """,
        "nav_active": "01",
        "swatches": {
            "surface": [
                ("Canvas", "#f4ede1", "Page bg", "#f4ede1"),
                ("Surface", "#ebe1cf", "Section bg", "#ebe1cf"),
                ("Surface Soft", "#e0d4bd", "Quieter sections", "#e0d4bd"),
                ("Footer", "#0a0a0a", "Dark footer", "#0a0a0a"),
                ("Surface Deep", "#0a0a0a", "Hero bands", "#0a0a0a"),
            ],
            "ink": [
                ("Ink", "#0a0a0a", "Headlines, CTAs", "#0a0a0a"),
                ("Ink 2", "#1a1a1a", "Primary text", "#1a1a1a"),
                ("Charcoal", "#222222", "Body text", "#222222"),
                ("Slate", "#444444", "Secondary text", "#444444"),
                ("Steel", "#666666", "Tertiary", "#666666"),
                ("Stone", "#888888", "Muted captions", "#888888"),
                ("Muted", "#aaaaaa", "Footer links", "#aaaaaa"),
            ],
            "hairline": [
                ("Hairline", "#0a0a0a", "Borders (3px)", "#0a0a0a"),
                ("Hairline Soft", "#7a6a4a", "Quiet dividers", "#7a6a4a"),
            ],
            "brand": [
                ("Brand Coral", "#ff4500", "M2.7 identity", "#ff4500"),
                ("Brand Magenta", "#ff00ff", "Music 2.6 identity", "#ff00ff"),
                ("Brand Blue", "#0033ff", "Hailuo / primary", "#0033ff"),
                ("Brand Cyan", "#00e5ff", "Atmospheric", "#00e5ff"),
                ("Brand Yellow", "#ffd400", "Highlights", "#ffd400"),
                ("Brand Green", "#00ff66", "Success", "#00ff66"),
                ("Brand Purple", "#9d00ff", "Speech 2.8 identity", "#9d00ff"),
            ],
            "semantic": [
                ("Success", "#00ff66", "Inline success", "#00ff66"),
                ("Success BG", "#e8ffe0", "Success badge bg", "#e8ffe0"),
                ("Error", "#ff4500", "Destructive, error", "#ff4500"),
            ],
        },
    }


def style_editorial():
    """4 · Editorial — newspaper serif, warm cream, deep navy, generous margins."""
    return {
        "slug": "editorial",
        "name": "Editorial",
        "tag": "Serif · newspaper · warm",
        "fonts": "Playfair+Display:wght@400;500;600;700;800;900&family=Source+Serif+4:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap",
        "css": r"""
:root{
  --canvas:#f6f1e7;--surface:#efe8d8;--surface-soft:#e6dcc6;
  --surface-deep:#0f1e3d;
  --ink:#0f1e3d;--ink-2:#1a2d54;--charcoal:#2a3a5c;--slate:#5a6783;--steel:#7a85a0;--stone:#9aa3b8;--muted:#b8bfd0;
  --hairline:#c8bfa6;--hairline-soft:#d8d0b8;
  --brand-coral:#b04a3e;--brand-magenta:#8e3a6e;--brand-blue:#1e4a8e;--brand-cyan:#3a7a8e;--brand-purple:#5e3a8e;--brand-gold:#a87a2e;
  --shadow-card:0 1px 0 var(--hairline), 0 2px 8px -4px rgba(15,30,61,0.12);
  --shadow-glow:0 0 0 1px var(--brand-gold), 0 6px 24px -10px rgba(168,122,46,0.4);
  --shadow-glow2:0 1px 0 var(--hairline), 0 8px 28px -8px rgba(94,58,142,0.25);
  --r-xs:2px;--r-sm:4px;--r-md:8px;--r-lg:12px;--r-xl:18px;--r-pill:4px;
  --font-display:'Playfair Display',serif;--font-body:'Source Serif 4',Georgia,serif;--font-mono:'JetBrains Mono',monospace;
}
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{font-family:var(--font-body);background:var(--canvas);color:var(--ink);line-height:1.65;-webkit-font-smoothing:antialiased;font-feature-settings:'liga','kern'}
code,pre,.mono{font-family:var(--font-mono)}
.shell{display:grid;grid-template-columns:240px 1fr;min-height:100vh}
nav.side{position:sticky;top:0;align-self:start;height:100vh;overflow:auto;border-right:1px solid var(--hairline);background:var(--surface);padding:32px 22px;font-family:'Source Serif 4',serif}
nav.side .brand{margin-bottom:32px;padding-bottom:22px;border-bottom:2px double var(--ink);text-align:center}
nav.side .logo{width:46px;height:46px;border-radius:50%;background:var(--ink);display:grid;place-items:center;color:var(--brand-gold);font-weight:700;font-size:22px;font-family:var(--font-display);margin:0 auto 10px;border:2px solid var(--brand-gold)}
nav.side .brand-name{font-family:var(--font-display);font-weight:700;font-size:20px;letter-spacing:0.01em;font-style:italic}
nav.side .brand-sub{font-size:11.5px;color:var(--slate);margin-top:4px;font-style:italic}
nav.side .group{font-size:11px;text-transform:uppercase;letter-spacing:0.18em;color:var(--ink);margin:20px 0 8px;font-weight:700;font-family:'Source Serif 4',serif;border-bottom:1px solid var(--ink);padding-bottom:3px}
nav.side a{display:block;padding:6px 4px;color:var(--charcoal);text-decoration:none;font-size:13.5px;border-bottom:1px dotted var(--hairline-soft);font-style:italic}
nav.side a:hover{color:var(--brand-gold);padding-left:8px}
nav.side a.active{color:var(--brand-gold);font-weight:700;font-style:normal;padding-left:8px;border-bottom:1px solid var(--brand-gold)}
main{padding:60px 70px 120px;max-width:960px}
section{margin-bottom:84px;scroll-margin-top:24px}
h1.doc-title{font-family:var(--font-display);font-size:64px;font-weight:700;letter-spacing:-0.02em;line-height:1.02;margin:0 0 12px;color:var(--ink);font-style:italic}
.doc-kicker{font-size:12px;text-transform:uppercase;letter-spacing:0.16em;color:var(--brand-gold);margin-bottom:10px;font-weight:700;font-family:'Source Serif 4',serif}
.doc-lead{color:var(--charcoal);font-size:18px;max-width:700px;margin:0 0 48px;line-height:1.6;font-style:italic;border-left:3px solid var(--brand-gold);padding-left:18px}
h2.section{font-family:var(--font-display);font-size:34px;font-weight:700;letter-spacing:-0.015em;margin:0 0 8px;color:var(--ink);display:flex;align-items:baseline;gap:14px;border-bottom:1px solid var(--ink);padding-bottom:10px}
h2.section .num{font-family:'Source Serif 4',serif;font-size:13px;color:var(--brand-gold);font-weight:700;font-style:italic}
.section-blurb{color:var(--charcoal);font-size:15.5px;margin:14px 0 26px;max-width:640px;line-height:1.65;font-style:italic}
h3{font-family:var(--font-display);font-size:20px;font-weight:700;margin:30px 0 14px;color:var(--ink);font-style:italic}
hr.rule{border:0;border-top:2px double var(--ink);margin:42px 0}
.swatches{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px}
.swatch{border:1px solid var(--hairline);border-radius:var(--r-sm);overflow:hidden;background:#fff}
.swatch .chip{height:90px;border-bottom:1px solid var(--hairline)}
.swatch .meta{padding:12px 14px}
.swatch .name{font-weight:700;font-size:13px;font-family:var(--font-display);font-style:italic}
.swatch .hex{font-family:var(--font-mono);font-size:11.5px;color:var(--slate);margin-top:3px}
.swatch .role{font-size:11.5px;color:var(--steel);margin-top:6px;font-style:italic}
.type-row{display:grid;grid-template-columns:200px 1fr;gap:24px;align-items:baseline;padding:22px 0;border-bottom:1px solid var(--hairline-soft)}
.type-row:last-child{border-bottom:0}
.type-meta .name{font-weight:700;font-size:13px;font-style:italic}
.type-meta .token{font-family:var(--font-mono);font-size:11.5px;color:var(--slate);margin-top:3px}
.type-meta .use{font-size:11.5px;color:var(--steel);margin-top:6px;font-style:italic}
.specimen-display{font-family:var(--font-display);font-weight:700;font-size:64px;line-height:1.05;letter-spacing:-0.02em;color:var(--ink);font-style:italic}
.specimen-h1{font-family:var(--font-display);font-weight:700;font-size:44px;line-height:1.1;letter-spacing:-0.015em;font-style:italic}
.specimen-h2{font-family:var(--font-display);font-weight:700;font-size:30px;line-height:1.15;font-style:italic}
.specimen-h3{font-family:var(--font-display);font-weight:700;font-size:22px;line-height:1.2;font-style:italic}
.specimen-body{font-family:var(--font-body);font-weight:400;font-size:17px;line-height:1.7}
.specimen-medium{font-family:var(--font-body);font-weight:600;font-size:16px}
.specimen-small{font-family:var(--font-body);font-weight:400;font-size:14px;color:var(--slate)}
.specimen-caption{font-family:var(--font-body);font-weight:400;font-size:13px;color:var(--steel);font-style:italic}
.specimen-mono{font-family:var(--font-mono);font-size:13px;color:var(--charcoal)}
.space-rows{display:flex;flex-direction:column;gap:4px}
.space-row{display:grid;grid-template-columns:90px 1fr 70px;align-items:center;gap:16px;padding:8px 0;border-bottom:1px dotted var(--hairline)}
.space-row .lbl{font-family:var(--font-mono);font-size:12px;color:var(--ink);font-style:italic}
.space-row .bar{background:var(--ink);height:6px}
.space-row .val{font-family:var(--font-mono);font-size:12px;color:var(--slate);text-align:right}
.radius-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:18px}
.radius-tile{text-align:center}
.radius-tile .box{width:100%;aspect-ratio:1.2;background:var(--ink);margin-bottom:10px}
.radius-tile .lbl{font-weight:700;font-size:13px;font-family:var(--font-display);font-style:italic}
.radius-tile .tok{font-family:var(--font-mono);font-size:11px;color:var(--slate)}
.shadow-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:26px}
.shadow-tile{background:#fff;padding:26px;border-radius:var(--r-sm);border:1px solid var(--hairline)}
.shadow-tile .lbl{font-weight:700;font-size:13.5px;margin-top:14px;font-family:var(--font-display);font-style:italic}
.shadow-tile .tok{font-family:var(--font-mono);font-size:11px;color:var(--slate)}
.shadow-card-tile{box-shadow:var(--shadow-card)}
.shadow-glow-tile{box-shadow:var(--shadow-glow)}
.shadow-glow2-tile{box-shadow:var(--shadow-glow2)}
.btn-row{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-bottom:16px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:11px 22px;font-family:var(--font-body);font-weight:600;font-size:14px;border:1px solid var(--ink);cursor:pointer;transition:all 0.2s ease;text-decoration:none;background:#fff;color:var(--ink);border-radius:var(--r-pill);letter-spacing:0.02em}
.btn:hover{background:var(--ink);color:#fff}
.btn-primary{background:var(--ink);color:#fff}
.btn-primary:hover{background:var(--brand-gold);border-color:var(--brand-gold)}
.btn-secondary{background:transparent;color:var(--ink)}
.btn-coral{background:var(--brand-coral);color:#fff;border-color:var(--brand-coral)}
.btn-magenta{background:var(--brand-magenta);color:#fff;border-color:var(--brand-magenta)}
.btn-blue{background:var(--brand-blue);color:#fff;border-color:var(--brand-blue)}
.btn-purple{background:var(--brand-purple);color:#fff;border-color:var(--brand-purple)}
.btn-square{border-radius:var(--r-sm)}
.btn-lg{padding:14px 26px;font-size:15px}
.btn-sm{padding:8px 16px;font-size:13px}
.btn-block{display:flex;width:100%;justify-content:center}
.pill{display:inline-flex;align-items:center;gap:6px;padding:4px 14px;font-size:12px;font-weight:600;border-radius:var(--r-pill);background:var(--surface);color:var(--charcoal);border:1px solid var(--hairline)}
.pill .dot{width:6px;height:6px;border-radius:50%;background:var(--brand-blue)}
.pill.coral{background:rgba(176,74,62,0.1);color:var(--brand-coral)}.pill.coral .dot{background:var(--brand-coral)}
.pill.magenta{background:rgba(142,58,110,0.1);color:var(--brand-magenta)}.pill.magenta .dot{background:var(--brand-magenta)}
.pill.blue{background:rgba(30,74,142,0.1);color:var(--brand-blue)}
.pill.purple{background:rgba(94,58,142,0.12);color:var(--brand-purple)}.pill.purple .dot{background:var(--brand-purple)}
.pill.success{background:rgba(58,122,78,0.1);color:#3a7a4e}.pill.success .dot{background:#3a7a4e}
.card-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px}
.card{border-radius:var(--r-sm);background:#fff;border:1px solid var(--hairline);padding:22px;box-shadow:var(--shadow-card)}
.card .card-kicker{font-size:11px;text-transform:uppercase;letter-spacing:0.14em;color:var(--brand-gold);font-weight:700;font-style:italic}
.card .card-title{font-family:var(--font-display);font-weight:700;font-size:22px;margin:8px 0 8px;color:var(--ink);font-style:italic;line-height:1.15}
.card .card-body{font-size:14px;color:var(--slate);line-height:1.6}
.product-card{border-radius:var(--r-md);padding:26px;color:#fff;min-height:180px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:var(--shadow-glow);border:1px solid rgba(255,255,255,0.2)}
.product-card .model{font-family:var(--font-display);font-weight:700;font-size:28px;letter-spacing:-0.01em;font-style:italic;line-height:1}
.product-card .sub{font-size:13px;opacity:0.92;margin-top:6px;font-style:italic}
.pc-coral{background:linear-gradient(135deg,var(--brand-coral) 0%,#c85e54 100%)}
.pc-magenta{background:linear-gradient(135deg,var(--brand-magenta) 0%,#a85a8a 100%)}
.pc-blue{background:linear-gradient(135deg,var(--brand-blue) 0%,#3a6eaa 100%)}
.pc-purple{background:linear-gradient(135deg,var(--brand-purple) 0%,#7e5eaa 100%)}
.field{display:flex;flex-direction:column;gap:6px;max-width:360px}
.field label{font-size:13px;color:var(--ink);font-weight:600;font-style:italic}
.input{padding:11px 16px;border-radius:var(--r-pill);border:1px solid var(--ink);background:#fff;font-size:14.5px;color:var(--ink);font-family:var(--font-body);outline:none}
.input:focus{border-color:var(--brand-gold);box-shadow:0 0 0 3px rgba(168,122,46,0.18)}
.input.square{border-radius:var(--r-sm)}
.icon-grid{display:grid;grid-template-columns:repeat(8,1fr);gap:8px}
.icon-tile{aspect-ratio:1;display:grid;place-items:center;background:#fff;border:1px solid var(--hairline);border-radius:var(--r-sm)}
.icon-tile svg{width:22px;height:22px;stroke:var(--ink);fill:none;stroke-width:1.4}
.dodont{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.dodont .item{padding:20px;border-radius:var(--r-sm);border:1px solid var(--hairline);background:#fff}
.dodont .do{border-left:4px solid #3a7a4e}
.dodont .dont{border-left:4px solid var(--brand-coral)}
.dodont .head{font-weight:700;font-size:12px;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:8px;font-family:var(--font-display);font-style:italic}
.dodont .do .head{color:#3a7a4e}.dodont .dont .head{color:var(--brand-coral)}
.dodont .item p{margin:0;font-size:14px;color:var(--charcoal);line-height:1.6}
table.tokens{width:100%;border-collapse:collapse;font-size:14px;border:1px solid var(--hairline)}
table.tokens th,table.tokens td{text-align:left;padding:11px 14px;border-bottom:1px solid var(--hairline-soft)}
table.tokens th{font-size:11px;text-transform:uppercase;letter-spacing:0.1em;color:var(--ink);font-weight:700;font-style:italic;background:var(--surface)}
table.tokens td.mono{font-family:var(--font-mono);font-size:12.5px}
table.tokens td .swatch-mini{display:inline-block;width:14px;height:14px;border-radius:50%;vertical-align:middle;margin-right:8px;border:1px solid var(--hairline)}
.hero-band{background:var(--ink);color:#fff;border-radius:var(--r-md);padding:68px 60px;margin-bottom:32px;position:relative;overflow:hidden;border:1px solid var(--brand-gold)}
.hero-band::after{content:"";position:absolute;right:30px;bottom:24px;width:60px;height:60px;border-radius:50%;background:radial-gradient(circle,rgba(168,122,46,0.4) 0%,transparent 70%)}
.hero-band h1{font-family:var(--font-display);font-size:68px;font-weight:700;letter-spacing:-0.02em;line-height:1.05;margin:0;position:relative;z-index:1;font-style:italic}
.hero-band p{font-size:17px;color:rgba(255,255,255,0.85);max-width:560px;margin:18px 0 30px;position:relative;z-index:1;line-height:1.6;font-style:italic}
.hero-band .cta-row{display:flex;gap:12px;position:relative;z-index:1}
.hero-band .btn-primary{background:var(--brand-gold);color:var(--ink);border-color:var(--brand-gold)}
.hero-band .btn-secondary{background:transparent;border-color:rgba(255,255,255,0.4);color:#fff}
.tag{display:inline-block;font-size:11px;padding:3px 10px;border-radius:var(--r-pill);background:var(--brand-blue);color:#fff;font-weight:600;font-style:italic}
.footer-block{background:var(--ink);color:#fff;border-radius:var(--r-md);padding:54px;margin-top:36px;border:1px solid var(--brand-gold)}
.footer-block h3{color:var(--brand-gold);font-family:var(--font-display);font-size:24px;margin:0 0 18px;font-style:italic}
.footer-block .links{display:grid;grid-template-columns:repeat(4,1fr);gap:32px}
.footer-block .col h4{font-size:11px;text-transform:uppercase;letter-spacing:0.14em;color:var(--brand-gold);margin:0 0 14px;font-weight:700;font-style:italic}
.footer-block .col a{display:block;color:rgba(255,255,255,0.82);text-decoration:none;font-size:14px;padding:4px 0;font-style:italic}
.footer-block .col a:hover{color:var(--brand-gold)}
@media (max-width:860px){.shell{grid-template-columns:1fr}nav.side{position:relative;height:auto}main{padding:32px 20px 80px}.hero-band h1{font-size:42px}}
        """,
        "nav_active": "01",
        "swatches": {
            "surface": [
                ("Canvas", "#f6f1e7", "Page bg", "#f6f1e7"),
                ("Surface", "#efe8d8", "Section bg", "#efe8d8"),
                ("Surface Soft", "#e6dcc6", "Quieter sections", "#e6dcc6"),
                ("Footer", "#0f1e3d", "Dark footer", "#0f1e3d"),
                ("Surface Deep", "#0f1e3d", "Hero bands", "#0f1e3d"),
            ],
            "ink": [
                ("Ink", "#0f1e3d", "Headlines, CTAs", "#0f1e3d"),
                ("Ink 2", "#1a2d54", "Primary text", "#1a2d54"),
                ("Charcoal", "#2a3a5c", "Body text", "#2a3a5c"),
                ("Slate", "#5a6783", "Secondary text", "#5a6783"),
                ("Steel", "#7a85a0", "Tertiary", "#7a85a0"),
                ("Stone", "#9aa3b8", "Muted captions", "#9aa3b8"),
                ("Muted", "#b8bfd0", "Footer links", "#b8bfd0"),
            ],
            "hairline": [
                ("Hairline", "#c8bfa6", "Borders", "#c8bfa6"),
                ("Hairline Soft", "#d8d0b8", "Quiet dividers", "#d8d0b8"),
            ],
            "brand": [
                ("Brand Coral", "#b04a3e", "M2.7 identity", "#b04a3e"),
                ("Brand Magenta", "#8e3a6e", "Music 2.6 identity", "#8e3a6e"),
                ("Brand Blue", "#1e4a8e", "Hailuo / primary", "#1e4a8e"),
                ("Brand Cyan", "#3a7a8e", "Atmospheric", "#3a7a8e"),
                ("Brand Gold", "#a87a2e", "Highlights", "#a87a2e"),
                ("Brand Purple", "#5e3a8e", "Speech 2.8 identity", "#5e3a8e"),
            ],
            "semantic": [
                ("Success", "#3a7a4e", "Inline success", "#3a7a4e"),
                ("Success BG", "#e8f0e0", "Success badge bg", "#e8f0e0"),
                ("Error", "#b04a3e", "Destructive, error", "#b04a3e"),
            ],
        },
    }


def style_cyber():
    """5 · Cyber-Synthwave — deep purple/navy, neon glow, geometric display."""
    return {
        "slug": "cyber",
        "name": "Cyber-Synthwave",
        "tag": "Neon · dark · geometric",
        "fonts": "Orbitron:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap",
        "css": r"""
:root{
  --canvas:#0a0a1a;--surface:#12122a;--surface-soft:#1a1a3a;
  --surface-deep:#000510;
  --ink:#e8e8ff;--ink-2:#d0d0f0;--charcoal:#b0b0d8;--slate:#8888c0;--steel:#6868a8;--stone:#5050a0;--muted:#3a3a78;
  --hairline:#2a2a5e;--hairline-soft:#1a1a4a;
  --brand-coral:#ff3a6e;--brand-magenta:#ff00d4;--brand-blue:#00aaff;--brand-cyan:#00f0ff;--brand-purple:#a855ff;--brand-yellow:#fff700;--brand-green:#00ff88;
  --shadow-card:0 0 0 1px rgba(0,240,255,0.18), 0 8px 24px -8px rgba(0,240,255,0.25);
  --shadow-glow:0 0 20px rgba(0,240,255,0.55), 0 0 40px rgba(168,85,255,0.35);
  --shadow-glow2:0 0 30px rgba(255,0,212,0.55), 0 0 60px rgba(255,58,110,0.3);
  --r-xs:2px;--r-sm:6px;--r-md:12px;--r-lg:18px;--r-xl:24px;--r-pill:9999px;
  --font-display:'Orbitron',sans-serif;--font-body:'Inter',sans-serif;--font-mono:'JetBrains Mono',monospace;
}
*{box-sizing:border-box}html,body{margin:0;padding:0}
body{font-family:var(--font-body);background:var(--canvas);background-image:linear-gradient(180deg,#0a0a1a 0%,#12122a 50%,#0a0a1a 100%);color:var(--ink);line-height:1.6;-webkit-font-smoothing:antialiased}
code,pre,.mono{font-family:var(--font-mono)}
.shell{display:grid;grid-template-columns:260px 1fr;min-height:100vh}
nav.side{position:sticky;top:0;align-self:start;height:100vh;overflow:auto;background:linear-gradient(180deg,rgba(18,18,42,0.92),rgba(10,10,26,0.92));backdrop-filter:blur(12px);border-right:1px solid var(--brand-cyan);padding:28px 20px;box-shadow:0 0 20px rgba(0,240,255,0.08)}
nav.side .brand{display:flex;align-items:center;gap:12px;margin-bottom:28px;padding-bottom:22px;border-bottom:1px solid var(--hairline)}
nav.side .logo{width:38px;height:38px;border-radius:8px;background:linear-gradient(135deg,var(--brand-cyan),var(--brand-purple));display:grid;place-items:center;color:#000;font-weight:800;font-size:16px;font-family:var(--font-display);box-shadow:0 0 20px rgba(0,240,255,0.5)}
nav.side .brand-name{font-family:var(--font-display);font-weight:700;font-size:15px;letter-spacing:0.08em;text-transform:uppercase;color:var(--brand-cyan);text-shadow:0 0 12px rgba(0,240,255,0.5)}
nav.side .brand-sub{font-size:11px;color:var(--slate);margin-top:3px;font-family:var(--font-mono);letter-spacing:0.06em}
nav.side .group{font-size:10.5px;text-transform:uppercase;letter-spacing:0.2em;color:var(--brand-magenta);margin:20px 0 8px;font-weight:700;text-shadow:0 0 8px rgba(255,0,212,0.4)}
nav.side a{display:block;padding:8px 12px;border-radius:6px;color:var(--ink-2);text-decoration:none;font-size:13px;transition:all 0.2s ease;border-left:2px solid transparent;font-weight:500}
nav.side a:hover{background:rgba(0,240,255,0.08);color:var(--brand-cyan);border-left-color:var(--brand-cyan)}
nav.side a.active{background:linear-gradient(90deg,rgba(0,240,255,0.18),transparent);color:var(--brand-cyan);border-left:2px solid var(--brand-cyan);box-shadow:inset 0 0 12px rgba(0,240,255,0.12)}
main{padding:54px 64px 110px;max-width:1120px}
section{margin-bottom:92px;scroll-margin-top:24px}
h1.doc-title{font-family:var(--font-display);font-size:60px;font-weight:800;letter-spacing:0.01em;line-height:1.05;margin:0 0 14px;text-transform:uppercase;color:var(--ink);text-shadow:0 0 24px rgba(0,240,255,0.3)}
.doc-kicker{font-size:11.5px;text-transform:uppercase;letter-spacing:0.22em;color:var(--brand-magenta);margin-bottom:10px;font-weight:700;font-family:var(--font-display);text-shadow:0 0 10px rgba(255,0,212,0.4)}
.doc-lead{color:var(--ink-2);font-size:16px;max-width:720px;margin:0 0 46px;line-height:1.65;border-left:3px solid var(--brand-cyan);padding-left:18px}
h2.section{font-family:var(--font-display);font-size:28px;font-weight:700;letter-spacing:0.04em;margin:0 0 8px;text-transform:uppercase;color:var(--ink);display:flex;align-items:baseline;gap:14px}
h2.section .num{font-family:var(--font-mono);font-size:11px;color:var(--brand-cyan);font-weight:700;background:rgba(0,240,255,0.1);padding:4px 10px;border-radius:4px;border:1px solid var(--brand-cyan);text-shadow:0 0 6px rgba(0,240,255,0.6)}
.section-blurb{color:var(--ink-2);font-size:14.5px;margin:0 0 26px;max-width:640px;line-height:1.65}
h3{font-family:var(--font-display);font-size:17px;font-weight:700;margin:30px 0 14px;text-transform:uppercase;letter-spacing:0.06em;color:var(--brand-cyan);text-shadow:0 0 10px rgba(0,240,255,0.4)}
hr.rule{border:0;border-top:1px solid var(--hairline);margin:40px 0;background:linear-gradient(90deg,transparent,var(--brand-cyan),transparent);height:1px}
.swatches{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px}
.swatch{border:1px solid var(--hairline);border-radius:var(--r-md);overflow:hidden;background:var(--surface)}
.swatch .chip{height:96px;border-bottom:1px solid var(--hairline)}
.swatch .meta{padding:12px 14px}
.swatch .name{font-weight:700;font-size:13px;font-family:var(--font-display);text-transform:uppercase;letter-spacing:0.04em}
.swatch .hex{font-family:var(--font-mono);font-size:11.5px;color:var(--brand-cyan);margin-top:3px}
.swatch .role{font-size:11px;color:var(--slate);margin-top:6px}
.type-row{display:grid;grid-template-columns:200px 1fr;gap:24px;align-items:baseline;padding:22px 0;border-bottom:1px solid var(--hairline-soft)}
.type-row:last-child{border-bottom:0}
.type-meta .name{font-weight:700;font-size:13px;font-family:var(--font-display);text-transform:uppercase;letter-spacing:0.06em}
.type-meta .token{font-family:var(--font-mono);font-size:11.5px;color:var(--brand-cyan);margin-top:3px}
.type-meta .use{font-size:11.5px;color:var(--slate);margin-top:6px}
.specimen-display{font-family:var(--font-display);font-weight:800;font-size:64px;line-height:1.05;letter-spacing:0.01em;text-transform:uppercase;color:var(--ink);text-shadow:0 0 18px rgba(0,240,255,0.4)}
.specimen-h1{font-family:var(--font-display);font-weight:700;font-size:44px;line-height:1.1;letter-spacing:0.02em;text-transform:uppercase;text-shadow:0 0 14px rgba(168,85,255,0.35)}
.specimen-h2{font-family:var(--font-display);font-weight:700;font-size:28px;line-height:1.15;text-transform:uppercase;letter-spacing:0.03em}
.specimen-h3{font-family:var(--font-body);font-weight:600;font-size:20px;line-height:1.3}
.specimen-body{font-family:var(--font-body);font-weight:400;font-size:16px;line-height:1.65}
.specimen-medium{font-family:var(--font-body);font-weight:500;font-size:16px;color:var(--ink)}
.specimen-small{font-family:var(--font-body);font-weight:400;font-size:14px;color:var(--ink-2)}
.specimen-caption{font-family:var(--font-body);font-weight:400;font-size:13px;color:var(--slate)}
.specimen-mono{font-family:var(--font-mono);font-size:13px;color:var(--brand-cyan)}
.space-rows{display:flex;flex-direction:column;gap:4px}
.space-row{display:grid;grid-template-columns:80px 1fr 60px;align-items:center;gap:16px;padding:8px 0}
.space-row .lbl{font-family:var(--font-mono);font-size:12px;color:var(--brand-cyan)}
.space-row .bar{background:linear-gradient(90deg,var(--brand-cyan),var(--brand-magenta));height:10px;border-radius:2px;box-shadow:0 0 12px rgba(0,240,255,0.4)}
.space-row .val{font-family:var(--font-mono);font-size:12px;color:var(--slate);text-align:right}
.radius-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:18px}
.radius-tile{text-align:center}
.radius-tile .box{width:100%;aspect-ratio:1.2;background:linear-gradient(135deg,var(--brand-cyan),var(--brand-purple));margin-bottom:10px;box-shadow:0 0 20px rgba(0,240,255,0.3)}
.radius-tile .lbl{font-weight:700;font-size:12.5px;font-family:var(--font-display);text-transform:uppercase;letter-spacing:0.04em}
.radius-tile .tok{font-family:var(--font-mono);font-size:11px;color:var(--brand-cyan)}
.shadow-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:26px}
.shadow-tile{background:var(--surface);padding:28px;border-radius:var(--r-md);border:1px solid var(--hairline)}
.shadow-tile .lbl{font-weight:700;font-size:13px;margin-top:14px;font-family:var(--font-display);text-transform:uppercase;letter-spacing:0.04em}
.shadow-tile .tok{font-family:var(--font-mono);font-size:11px;color:var(--brand-cyan)}
.shadow-card-tile{box-shadow:var(--shadow-card)}
.shadow-glow-tile{box-shadow:var(--shadow-glow)}
.shadow-glow2-tile{box-shadow:var(--shadow-glow2)}
.btn-row{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-bottom:16px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:11px 22px;font-family:var(--font-display);font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:0.06em;border:1px solid transparent;cursor:pointer;transition:all 0.2s ease;text-decoration:none;background:transparent;color:var(--ink);border-radius:var(--r-pill)}
.btn-primary{background:var(--brand-cyan);color:#000;border-color:var(--brand-cyan);box-shadow:0 0 18px rgba(0,240,255,0.5)}
.btn-primary:hover{box-shadow:0 0 28px rgba(0,240,255,0.7);transform:translateY(-1px)}
.btn-secondary{background:transparent;color:var(--ink);border:1px solid var(--brand-cyan)}
.btn-secondary:hover{background:rgba(0,240,255,0.1)}
.btn-coral{background:var(--brand-coral);color:#fff;border-color:var(--brand-coral);box-shadow:0 0 18px rgba(255,58,110,0.5)}
.btn-magenta{background:var(--brand-magenta);color:#fff;border-color:var(--brand-magenta);box-shadow:0 0 18px rgba(255,0,212,0.5)}
.btn-blue{background:var(--brand-blue);color:#000;border-color:var(--brand-blue);box-shadow:0 0 18px rgba(0,170,255,0.5)}
.btn-purple{background:var(--brand-purple);color:#fff;border-color:var(--brand-purple);box-shadow:0 0 18px rgba(168,85,255,0.5)}
.btn-square{border-radius:var(--r-sm)}
.btn-lg{padding:14px 26px;font-size:14px}
.btn-sm{padding:8px 16px;font-size:12px}
.btn-block{display:flex;width:100%;justify-content:center}
.pill{display:inline-flex;align-items:center;gap:6px;padding:5px 14px;font-size:11.5px;font-weight:600;border-radius:var(--r-pill);background:var(--surface-soft);color:var(--ink);border:1px solid var(--hairline);font-family:var(--font-display);text-transform:uppercase;letter-spacing:0.06em}
.pill .dot{width:6px;height:6px;border-radius:50%;background:var(--brand-cyan);box-shadow:0 0 8px var(--brand-cyan)}
.pill.coral{background:rgba(255,58,110,0.15);color:var(--brand-coral);border-color:var(--brand-coral)}.pill.coral .dot{background:var(--brand-coral);box-shadow:0 0 8px var(--brand-coral)}
.pill.magenta{background:rgba(255,0,212,0.15);color:var(--brand-magenta);border-color:var(--brand-magenta)}.pill.magenta .dot{background:var(--brand-magenta);box-shadow:0 0 8px var(--brand-magenta)}
.pill.blue{background:rgba(0,170,255,0.15);color:var(--brand-blue);border-color:var(--brand-blue)}
.pill.purple{background:rgba(168,85,255,0.18);color:var(--brand-purple);border-color:var(--brand-purple)}.pill.purple .dot{background:var(--brand-purple);box-shadow:0 0 8px var(--brand-purple)}
.pill.success{background:rgba(0,255,136,0.15);color:var(--brand-green);border-color:var(--brand-green)}.pill.success .dot{background:var(--brand-green);box-shadow:0 0 8px var(--brand-green)}
.card-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:18px}
.card{border-radius:var(--r-md);background:var(--surface);border:1px solid var(--hairline);padding:22px;box-shadow:var(--shadow-card)}
.card .card-kicker{font-size:10.5px;text-transform:uppercase;letter-spacing:0.16em;color:var(--brand-cyan);font-weight:700;font-family:var(--font-display);text-shadow:0 0 8px rgba(0,240,255,0.4)}
.card .card-title{font-family:var(--font-display);font-weight:700;font-size:20px;margin:8px 0 8px;color:var(--ink);text-transform:uppercase;letter-spacing:0.02em}
.card .card-body{font-size:13.5px;color:var(--ink-2);line-height:1.6}
.product-card{border-radius:var(--r-md);padding:28px;color:#fff;min-height:180px;display:flex;flex-direction:column;justify-content:space-between;border:1px solid rgba(255,255,255,0.1)}
.product-card .model{font-family:var(--font-display);font-weight:800;font-size:26px;letter-spacing:0.02em;text-transform:uppercase;text-shadow:0 0 12px rgba(0,0,0,0.5)}
.product-card .sub{font-size:12.5px;opacity:0.92;margin-top:6px;font-family:var(--font-mono);text-transform:uppercase;letter-spacing:0.08em}
.pc-coral{background:linear-gradient(135deg,var(--brand-coral) 0%,#ff6a8a 100%);box-shadow:0 0 30px rgba(255,58,110,0.4)}
.pc-magenta{background:linear-gradient(135deg,var(--brand-magenta) 0%,#ff5ce8 100%);box-shadow:0 0 30px rgba(255,0,212,0.4)}
.pc-blue{background:linear-gradient(135deg,var(--brand-blue) 0%,#5fcfff 100%);box-shadow:0 0 30px rgba(0,170,255,0.4)}
.pc-purple{background:linear-gradient(135deg,var(--brand-purple) 0%,#c87aff 100%);box-shadow:0 0 30px rgba(168,85,255,0.4)}
.field{display:flex;flex-direction:column;gap:6px;max-width:360px}
.field label{font-size:12px;color:var(--brand-cyan);font-weight:600;font-family:var(--font-display);text-transform:uppercase;letter-spacing:0.08em}
.input{padding:11px 16px;border-radius:var(--r-pill);border:1px solid var(--brand-cyan);background:var(--surface);font-size:14px;color:var(--ink);font-family:var(--font-body);outline:none}
.input:focus{border-color:var(--brand-magenta);box-shadow:0 0 0 3px rgba(255,0,212,0.2)}
.input.square{border-radius:var(--r-sm)}
.icon-grid{display:grid;grid-template-columns:repeat(8,1fr);gap:8px}
.icon-tile{aspect-ratio:1;display:grid;place-items:center;background:var(--surface);border:1px solid var(--hairline);border-radius:var(--r-sm)}
.icon-tile svg{width:22px;height:22px;stroke:var(--brand-cyan);fill:none;stroke-width:1.6;filter:drop-shadow(0 0 4px rgba(0,240,255,0.4))}
.dodont{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.dodont .item{padding:18px;border-radius:var(--r-md);border:1px solid var(--hairline);background:var(--surface)}
.dodont .do{border-color:var(--brand-green);box-shadow:0 0 16px rgba(0,255,136,0.15)}
.dodont .dont{border-color:var(--brand-coral);box-shadow:0 0 16px rgba(255,58,110,0.15)}
.dodont .head{font-weight:700;font-size:11.5px;text-transform:uppercase;letter-spacing:0.12em;margin-bottom:6px;font-family:var(--font-display)}
.dodont .do .head{color:var(--brand-green);text-shadow:0 0 8px rgba(0,255,136,0.4)}
.dodont .dont .head{color:var(--brand-coral);text-shadow:0 0 8px rgba(255,58,110,0.4)}
.dodont .item p{margin:0;font-size:13.5px;color:var(--ink-2);line-height:1.6}
table.tokens{width:100%;border-collapse:collapse;font-size:13.5px;background:var(--surface);border-radius:var(--r-md);overflow:hidden;border:1px solid var(--hairline)}
table.tokens th,table.tokens td{text-align:left;padding:11px 14px;border-bottom:1px solid var(--hairline-soft)}
table.tokens th{font-size:11px;text-transform:uppercase;letter-spacing:0.1em;color:var(--brand-cyan);font-weight:700;font-family:var(--font-display);background:var(--surface-soft)}
table.tokens td.mono{font-family:var(--font-mono);font-size:12.5px;color:var(--ink)}
table.tokens td .swatch-mini{display:inline-block;width:14px;height:14px;border-radius:50%;vertical-align:middle;margin-right:8px;border:1px solid var(--hairline)}
.hero-band{background:linear-gradient(135deg,#0a0a1a 0%,#1a0a3a 50%,#3a0a4a 100%);color:#fff;border-radius:var(--r-md);padding:64px 56px;margin-bottom:32px;position:relative;overflow:hidden;border:1px solid var(--brand-cyan);box-shadow:0 0 40px rgba(0,240,255,0.25),inset 0 0 60px rgba(168,85,255,0.1)}
.hero-band::after{content:"";position:absolute;right:-100px;top:-100px;width:320px;height:320px;border-radius:50%;background:radial-gradient(circle,rgba(255,0,212,0.35) 0%,transparent 70%)}
.hero-band h1{font-family:var(--font-display);font-size:74px;font-weight:800;letter-spacing:0.02em;line-height:1.02;margin:0;position:relative;z-index:1;text-transform:uppercase;color:#fff;text-shadow:0 0 30px rgba(0,240,255,0.6),0 0 60px rgba(168,85,255,0.4)}
.hero-band p{font-size:16px;color:rgba(255,255,255,0.8);max-width:540px;margin:20px 0 30px;position:relative;z-index:1;line-height:1.6}
.hero-band .cta-row{display:flex;gap:12px;position:relative;z-index:1}
.hero-band .btn-primary{background:var(--brand-cyan);color:#000}
.hero-band .btn-secondary{background:transparent;border-color:var(--brand-magenta);color:#fff}
.tag{display:inline-block;font-size:11px;padding:3px 10px;border-radius:var(--r-pill);background:var(--brand-blue);color:#000;font-weight:600;font-family:var(--font-display);text-transform:uppercase;letter-spacing:0.06em}
.footer-block{background:linear-gradient(135deg,#0a0a1a,#1a0a3a);color:#fff;border-radius:var(--r-md);padding:54px;margin-top:36px;border:1px solid var(--brand-purple);box-shadow:0 0 30px rgba(168,85,255,0.25)}
.footer-block h3{color:var(--brand-cyan);font-family:var(--font-display);font-size:20px;margin:0 0 16px;text-transform:uppercase;letter-spacing:0.04em;text-shadow:0 0 12px rgba(0,240,255,0.4)}
.footer-block .links{display:grid;grid-template-columns:repeat(4,1fr);gap:32px}
.footer-block .col h4{font-size:11px;text-transform:uppercase;letter-spacing:0.16em;color:var(--brand-magenta);margin:0 0 14px;font-weight:700;font-family:var(--font-display)}
.footer-block .col a{display:block;color:rgba(255,255,255,0.78);text-decoration:none;font-size:13.5px;padding:4px 0;transition:color 0.15s ease}
.footer-block .col a:hover{color:var(--brand-cyan)}
@media (max-width:860px){.shell{grid-template-columns:1fr}nav.side{position:relative;height:auto;border-right:0;border-bottom:1px solid var(--brand-cyan)}main{padding:32px 20px 80px}.hero-band h1{font-size:42px}}
        """,
        "nav_active": "01",
        "swatches": {
            "surface": [
                ("Canvas", "#0a0a1a", "Page bg", "#0a0a1a"),
                ("Surface", "#12122a", "Section bg", "#12122a"),
                ("Surface Soft", "#1a1a3a", "Quieter sections", "#1a1a3a"),
                ("Footer", "#0a0a1a", "Dark footer", "#0a0a1a"),
                ("Surface Deep", "#000510", "Hero bands", "#000510"),
            ],
            "ink": [
                ("Ink", "#e8e8ff", "Headlines, CTAs", "#e8e8ff"),
                ("Ink 2", "#d0d0f0", "Primary text", "#d0d0f0"),
                ("Charcoal", "#b0b0d8", "Body text", "#b0b0d8"),
                ("Slate", "#8888c0", "Secondary text", "#8888c0"),
                ("Steel", "#6868a8", "Tertiary", "#6868a8"),
                ("Stone", "#5050a0", "Muted captions", "#5050a0"),
                ("Muted", "#3a3a78", "Footer links", "#3a3a78"),
            ],
            "hairline": [
                ("Hairline", "#2a2a5e", "Borders", "#2a2a5e"),
                ("Hairline Soft", "#1a1a4a", "Quiet dividers", "#1a1a4a"),
            ],
            "brand": [
                ("Brand Coral", "#ff3a6e", "M2.7 identity", "#ff3a6e"),
                ("Brand Magenta", "#ff00d4", "Music 2.6 identity", "#ff00d4"),
                ("Brand Blue", "#00aaff", "Hailuo / primary", "#00aaff"),
                ("Brand Cyan", "#00f0ff", "Atmospheric", "#00f0ff"),
                ("Brand Yellow", "#fff700", "Highlights", "#fff700"),
                ("Brand Green", "#00ff88", "Success", "#00ff88"),
                ("Brand Purple", "#a855ff", "Speech 2.8 identity", "#a855ff"),
            ],
            "semantic": [
                ("Success", "#00ff88", "Inline success", "#00ff88"),
                ("Success BG", "rgba(0,255,136,0.15)", "Success badge bg", "#00ff88"),
                ("Error", "#ff3a6e", "Destructive, error", "#ff3a6e"),
            ],
        },
    }


STYLES = [style_noir, style_aurora, style_brutalist, style_editorial, style_cyber]


def render_swatch_chips(swatches):
    """Render the color section: surface, ink, hairline, brand, semantic groups."""
    out = []
    for label, items in [
        ("Surface &amp; Canvas", swatches["surface"]),
        ("Ink &amp; Text", swatches["ink"]),
        ("Borders &amp; Hairlines", swatches["hairline"]),
        ("Brand &amp; Accent — Product Identity", swatches["brand"]),
        ("Semantic", swatches["semantic"]),
    ]:
        out.append(f"<h3>{label}</h3>")
        if "Product Identity" in label:
            out.append('<p class="section-blurb" style="margin-top:0">Saturated hues are reserved for product release identity. Don\'t apply them to general UI.</p>')
        out.append('<div class="swatches">')
        for name, hex_, role, chip_color in items:
            chip_style = f"background:{chip_color};"
            out.append(
                f'<div class="swatch"><div class="chip" style="{chip_style}"></div>'
                f'<div class="meta"><div class="name">{html.escape(name)}</div>'
                f'<div class="hex">{html.escape(hex_)}</div>'
                f'<div class="role">{html.escape(role)}</div></div></div>'
            )
        out.append('</div>')
    return "\n      ".join(out)


def render_page(s, n):
    """Render a full style-N.html page for style system s."""
    sw = s["swatches"]
    chips_html = render_swatch_chips(sw)

    # Token table rows
    token_rows = []
    for group_name, items in [
        ("surface", sw["surface"][:2]),
        ("ink", sw["ink"][:2]),
        ("brand", sw["brand"][:2]),
        ("hairline", sw["hairline"][:1]),
    ]:
        for name, hex_, role, chip in items:
            token_rows.append(
                f'<tr><td>{group_name}</td><td>{html.escape(name.lower().replace(" ", "-"))}</td>'
                f'<td class="mono"><span class="swatch-mini" style="background:{chip}"></span>{html.escape(hex_)}</td>'
                f'<td>{html.escape(role)}</td></tr>'
            )

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>MiniMax Style Guide — {s["name"]}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family={s["fonts"]}" rel="stylesheet" />
  <style>{s["css"]}</style>
</head>
<body>
<div class="shell">
  <nav class="side">
    <div class="brand">
      <div class="logo">M</div>
      <div>
        <div class="brand-name">{s["name"]}</div>
        <div class="brand-sub">{html.escape(s["tag"])}</div>
      </div>
    </div>
    <div class="group"><a href="styles.html" style="display:inline;padding:0;background:none;color:inherit;border:0;text-transform:uppercase;font-weight:700;letter-spacing:0.18em">← All styles</a></div>
    <div class="group">Style {n} of 6</div>
    <div class="group">Foundations</div>
    <a href="#intro">00 · Overview</a>
    <a href="#voice">01 · Brand Voice</a>
    <a href="#color">02 · Color</a>
    <a href="#type">03 · Typography</a>
    <a href="#space">04 · Spacing</a>
    <a href="#radius">05 · Radius &amp; Shape</a>
    <a href="#shadow">06 · Shadows</a>
    <div class="group">Components</div>
    <a href="#buttons">07 · Buttons</a>
    <a href="#badges">08 · Badges &amp; Pills</a>
    <a href="#cards">09 · Cards</a>
    <a href="#inputs">10 · Inputs</a>
    <a href="#icons">11 · Iconography</a>
    <div class="group">Patterns</div>
    <a href="#hero">12 · Hero Band</a>
    <a href="#footer">13 · Footer</a>
    <a href="#dodont">14 · Do &amp; Don't</a>
  </nav>

  <main>
    <section id="intro">
      <div class="doc-kicker">Style {n} of 6 · {s["name"]} · 2026</div>
      <h1 class="doc-title">MiniMax · {s["name"]}</h1>
      <p class="doc-lead">
        Variant {n} of the MiniMax design system exploration — {html.escape(s["tag"])}.
        Same 14-section structure, same content as the canonical guide; only the visual system changes.
        Compare each style to find the one that fits the brand voice best.
      </p>

      <div class="hero-band">
        <h1>Flagship<br/>Models</h1>
        <p>One typeface, four weights, ninety percent monochrome, one hundred percent identity.</p>
        <div class="cta-row">
          <a class="btn btn-primary btn-lg" href="#">Explore models</a>
          <a class="btn btn-secondary btn-lg" href="#">Read the docs</a>
        </div>
      </div>

      <div class="card-row">
        <div class="card">
          <div class="card-kicker">Principle 01</div>
          <div class="card-title">Monochrome by default</div>
          <div class="card-body">The page is the canvas. Let product moments bring the color, not the chrome.</div>
        </div>
        <div class="card">
          <div class="card-kicker">Principle 02</div>
          <div class="card-title">Pills over rectangles</div>
          <div class="card-body">Every button, tab, and badge is full-radius. Rectangles live only in data tables.</div>
        </div>
        <div class="card">
          <div class="card-kicker">Principle 03</div>
          <div class="card-title">One typeface, four weights</div>
          <div class="card-body">DM Sans carries the brand. Emphasis is weight, never slope.</div>
        </div>
      </div>
    </section>

    <section id="voice">
      <h2 class="section"><span class="num">01</span> Brand Voice</h2>
      <p class="section-blurb">How MiniMax sounds, not just how it looks. The brand pairs editorial confidence with quiet technicality.</p>
      <div class="dodont">
        <div class="item do"><div class="head">Do</div><p>Lead with the product. Use short, declarative sentences. Let visuals carry the warmth.</p></div>
        <div class="item dont"><div class="head">Don't</div><p>Lean on hype adjectives ("revolutionary", "groundbreaking") or generic AI tropes.</p></div>
        <div class="item do"><div class="head">Do</div><p>Write at grade 8–10. Use concrete nouns. Reference specific model capabilities.</p></div>
        <div class="item dont"><div class="head">Don't</div><p>Bury the action. Front-load qualifiers. Stack three clauses in one sentence.</p></div>
      </div>
    </section>

    <section id="color">
      <h2 class="section"><span class="num">02</span> Color</h2>
      <p class="section-blurb">Token set for the {s["name"]} variant. Grouped by surface, ink, hairline, brand, and semantic roles.</p>
      {chips_html}

      <h3>Token Reference</h3>
      <table class="tokens">
        <thead><tr><th>Group</th><th>Token</th><th>Value</th><th>Use</th></tr></thead>
        <tbody>
          {"".join(token_rows)}
        </tbody>
      </table>
    </section>

    <section id="type">
      <h2 class="section"><span class="num">03</span> Typography</h2>
      <p class="section-blurb">Type stack for the {s["name"]} variant. Display + body + mono. Weight does the work; italics don't.</p>

      <div class="type-row">
        <div class="type-meta"><div class="name">Display / Hero</div><div class="token">{html.escape(s["css"].split("--font-display:")[1].split(";")[0].strip())}</div><div class="use">64–80px / 700 / -0.03em</div></div>
        <div class="specimen-display">Flagship Models</div>
      </div>
      <div class="type-row">
        <div class="type-meta"><div class="name">H1</div><div class="token">{html.escape(s["css"].split("--font-display:")[1].split(";")[0].strip())}</div><div class="use">44px / 700 / -0.02em</div></div>
        <div class="specimen-h1">A platform for multimodal intelligence</div>
      </div>
      <div class="type-row">
        <div class="type-meta"><div class="name">H2</div><div class="token">{html.escape(s["css"].split("--font-display:")[1].split(";")[0].strip())}</div><div class="use">28px / 700</div></div>
        <div class="specimen-h2">Section heading</div>
      </div>
      <div class="type-row">
        <div class="type-meta"><div class="name">H3 / Card title</div><div class="token">{html.escape(s["css"].split("--font-body:")[1].split(";")[0].strip())}</div><div class="use">20px / 700</div></div>
        <div class="specimen-h3">Card or feature title</div>
      </div>
      <div class="type-row">
        <div class="type-meta"><div class="name">Body</div><div class="token">{html.escape(s["css"].split("--font-body:")[1].split(";")[0].strip())}</div><div class="use">16px / 400 / 1.6</div></div>
        <div class="specimen-body">Default paragraph. Generous line-height for long-form docs. Max 72ch per line.</div>
      </div>
      <div class="type-row">
        <div class="type-meta"><div class="name">Body medium</div><div class="token">{html.escape(s["css"].split("--font-body:")[1].split(";")[0].strip())}</div><div class="use">16px / 500</div></div>
        <div class="specimen-medium">Emphasized body — button labels, feature intros.</div>
      </div>
      <div class="type-row">
        <div class="type-meta"><div class="name">Small</div><div class="token">{html.escape(s["css"].split("--font-body:")[1].split(";")[0].strip())}</div><div class="use">14px / 400</div></div>
        <div class="specimen-small">Compact descriptions and metadata.</div>
      </div>
      <div class="type-row">
        <div class="type-meta"><div class="name">Caption</div><div class="token">{html.escape(s["css"].split("--font-body:")[1].split(";")[0].strip())}</div><div class="use">13px / 400</div></div>
        <div class="specimen-caption">Tertiary metadata and timestamps.</div>
      </div>
      <div class="type-row">
        <div class="type-meta"><div class="name">Mono / Code</div><div class="token">{html.escape(s["css"].split("--font-mono:")[1].split(";")[0].strip())}</div><div class="use">13px / 400</div></div>
        <div class="specimen-mono">const model = "MiniMax-M3";</div>
      </div>
    </section>

    <section id="space">
      <h2 class="section"><span class="num">04</span> Spacing</h2>
      <p class="section-blurb">A 4px base scale. The system rarely goes below 4px or above 96px on UI — larger values are reserved for hero rhythm.</p>
      <div class="space-rows">
        <div class="space-row"><div class="lbl">--space-1</div><div class="bar" style="width:4px"></div><div class="val">4px</div></div>
        <div class="space-row"><div class="lbl">--space-2</div><div class="bar" style="width:8px"></div><div class="val">8px</div></div>
        <div class="space-row"><div class="lbl">--space-3</div><div class="bar" style="width:12px"></div><div class="val">12px</div></div>
        <div class="space-row"><div class="lbl">--space-4</div><div class="bar" style="width:16px"></div><div class="val">16px</div></div>
        <div class="space-row"><div class="lbl">--space-5</div><div class="bar" style="width:20px"></div><div class="val">20px</div></div>
        <div class="space-row"><div class="lbl">--space-6</div><div class="bar" style="width:24px"></div><div class="val">24px</div></div>
        <div class="space-row"><div class="lbl">--space-8</div><div class="bar" style="width:32px"></div><div class="val">32px</div></div>
        <div class="space-row"><div class="lbl">--space-10</div><div class="bar" style="width:40px"></div><div class="val">40px</div></div>
        <div class="space-row"><div class="lbl">--space-12</div><div class="bar" style="width:48px"></div><div class="val">48px</div></div>
        <div class="space-row"><div class="lbl">--space-16</div><div class="bar" style="width:64px"></div><div class="val">64px</div></div>
        <div class="space-row"><div class="lbl">--space-24</div><div class="bar" style="width:96px"></div><div class="val">96px</div></div>
      </div>
    </section>

    <section id="radius">
      <h2 class="section"><span class="num">05</span> Radius &amp; Shape</h2>
      <p class="section-blurb">Radius tokens tuned for the {s["name"]} visual signature — pills, sharp corners, or soft rounds.</p>
      <div class="radius-grid">
        <div class="radius-tile"><div class="box" style="border-radius:4px"></div><div class="lbl">xs · chips</div><div class="tok">4px</div></div>
        <div class="radius-tile"><div class="box" style="border-radius:8px"></div><div class="lbl">sm · UI</div><div class="tok">8px</div></div>
        <div class="radius-tile"><div class="box" style="border-radius:12px"></div><div class="lbl">md</div><div class="tok">12px</div></div>
        <div class="radius-tile"><div class="box" style="border-radius:16px"></div><div class="lbl">md · doc cards</div><div class="tok">16px</div></div>
        <div class="radius-tile"><div class="box" style="border-radius:24px"></div><div class="lbl">lg</div><div class="tok">24px</div></div>
        <div class="radius-tile"><div class="box" style="border-radius:32px"></div><div class="lbl">xl · product</div><div class="tok">32px</div></div>
        <div class="radius-tile"><div class="box" style="border-radius:9999px"></div><div class="lbl">pill</div><div class="tok">9999px</div></div>
      </div>
    </section>

    <section id="shadow">
      <h2 class="section"><span class="num">06</span> Shadows</h2>
      <p class="section-blurb">Elevation system for the {s["name"]} variant — offset shadows, soft glows, or neon halos.</p>
      <div class="shadow-grid">
        <div class="shadow-tile shadow-card-tile"><div style="height:80px;background:var(--surface-soft);border-radius:8px"></div><div class="lbl">Card elevation</div><div class="tok">token: --shadow-card</div></div>
        <div class="shadow-tile shadow-glow-tile"><div style="height:80px;background:var(--surface-soft);border-radius:8px"></div><div class="lbl">Brand glow</div><div class="tok">token: --shadow-glow</div></div>
        <div class="shadow-tile shadow-glow2-tile"><div style="height:80px;background:var(--surface-soft);border-radius:8px"></div><div class="lbl">Brand glow offset</div><div class="tok">token: --shadow-glow2</div></div>
      </div>
    </section>

    <section id="buttons">
      <h2 class="section"><span class="num">07</span> Buttons</h2>
      <p class="section-blurb">Buttons tuned for the {s["name"]} shape language — pill, square, or hybrid.</p>
      <h3>Primary actions</h3>
      <div class="btn-row">
        <a class="btn btn-primary btn-lg" href="#">Get started</a>
        <a class="btn btn-primary" href="#">Default</a>
        <a class="btn btn-primary btn-sm" href="#">Small</a>
        <a class="btn btn-primary" href="#"><span>With icon</span> →</a>
      </div>
      <h3>Secondary</h3>
      <div class="btn-row">
        <a class="btn btn-secondary btn-lg" href="#">Learn more</a>
        <a class="btn btn-secondary" href="#">Default</a>
        <a class="btn btn-secondary btn-sm" href="#">Small</a>
      </div>
      <h3>Brand actions</h3>
      <p class="section-blurb" style="margin-top:0">Use only on product release surfaces.</p>
      <div class="btn-row">
        <a class="btn btn-coral" href="#">Try M2.7</a>
        <a class="btn btn-magenta" href="#">Try Music 2.6</a>
        <a class="btn btn-blue" href="#">Try Hailuo</a>
        <a class="btn btn-purple" href="#">Try Speech 2.8</a>
      </div>
      <h3>Square variants</h3>
      <div class="btn-row">
        <a class="btn btn-primary btn-square" href="#">Square</a>
        <a class="btn btn-secondary btn-square" href="#">Square secondary</a>
      </div>
    </section>

    <section id="badges">
      <h2 class="section"><span class="num">08</span> Badges &amp; Pills</h2>
      <p class="section-blurb">Tags, status indicators, category labels. Color encodes meaning, never decoration.</p>
      <div class="btn-row">
        <span class="pill"><span class="dot"></span>Default</span>
        <span class="pill coral"><span class="dot"></span>M2.7</span>
        <span class="pill magenta"><span class="dot"></span>Music 2.6</span>
        <span class="pill blue"><span class="dot"></span>Hailuo</span>
        <span class="pill purple"><span class="dot"></span>Speech 2.8</span>
        <span class="pill success"><span class="dot"></span>Live</span>
        <span class="tag">deprecated</span>
        <span class="tag" style="background:rgba(255,85,48,0.12);color:#c4381d">beta</span>
      </div>
    </section>

    <section id="cards">
      <h2 class="section"><span class="num">09</span> Cards</h2>
      <p class="section-blurb">Two card archetypes: documentation cards for prose surfaces, product identity cards for product moments.</p>
      <h3>Documentation cards</h3>
      <div class="card-row">
        <div class="card"><div class="card-kicker">Guide</div><div class="card-title">API quickstart</div><div class="card-body">Make your first request to the MiniMax API in under five minutes.</div></div>
        <div class="card"><div class="card-kicker">Release</div><div class="card-title">M3 is here</div><div class="card-body">Frontier coding with 1M context, now in general availability.</div></div>
        <div class="card"><div class="card-kicker">Concept</div><div class="card-title">Long-horizon agents</div><div class="card-body">A pattern for sustained, multi-stage work with verification gates.</div></div>
      </div>
      <h3>Product identity cards</h3>
      <div class="card-row">
        <div class="product-card pc-coral"><div><div class="model">M2.7</div><div class="sub">Language · Token plan</div></div><div class="sub" style="font-size:12px;opacity:0.85">Brand Coral</div></div>
        <div class="product-card pc-magenta"><div><div class="model">Music 2.6</div><div class="sub">Audio · Generation</div></div><div class="sub" style="font-size:12px;opacity:0.85">Brand Magenta</div></div>
        <div class="product-card pc-blue"><div><div class="model">Hailuo</div><div class="sub">Video · Generation</div></div><div class="sub" style="font-size:12px;opacity:0.85">Brand Blue</div></div>
        <div class="product-card pc-purple"><div><div class="model">Speech 2.8</div><div class="sub">Audio · TTS</div></div><div class="sub" style="font-size:12px;opacity:0.85">Brand Purple</div></div>
      </div>
    </section>

    <section id="inputs">
      <h2 class="section"><span class="num">10</span> Inputs</h2>
      <p class="section-blurb">Inputs tuned for the {s["name"]} variant — pill, square, or hybrid. Focus ring uses the brand accent.</p>
      <div class="card-row" style="grid-template-columns:1fr 1fr;max-width:760px">
        <div class="field"><label>Email</label><input class="input" type="email" placeholder="you@company.com" /></div>
        <div class="field"><label>Search</label><input class="input" type="search" placeholder="Search models…" /></div>
        <div class="field"><label>API key (square)</label><input class="input square" type="text" value="mmx-•••••••••••••" /></div>
        <div class="field"><label>Region</label><input class="input square" type="text" value="us-east-1" /></div>
      </div>
    </section>

    <section id="icons">
      <h2 class="section"><span class="num">11</span> Iconography</h2>
      <p class="section-blurb">1.6px stroke icons on a 22px box. Single weight. Color encodes state via the variant's accent.</p>
      <div class="icon-grid">{ICON_GRID}</div>
    </section>

    <section id="hero">
      <h2 class="section"><span class="num">12</span> Hero Band</h2>
      <p class="section-blurb">First-impression pattern for the {s["name"]} variant — dark canvas, oversized display, accent glow.</p>
      <div class="hero-band">
        <h1>Build with MiniMax</h1>
        <p>Frontier language, video, audio, and speech models — one platform, one API, one bill.</p>
        <div class="cta-row">
          <a class="btn btn-primary btn-lg" href="#">Start building</a>
          <a class="btn btn-secondary btn-lg" href="#">Talk to sales</a>
        </div>
      </div>
    </section>

    <section id="footer">
      <h2 class="section"><span class="num">13</span> Footer</h2>
      <p class="section-blurb">Dense, near-black, four-column. Low-contrast text, all links discoverable.</p>
      <div class="footer-block">
        <h3>MiniMax</h3>
        <div class="links">
          <div class="col"><h4>Product</h4><a href="#">MiniMax M3</a><a href="#">Hailuo Video</a><a href="#">Music 2.6</a><a href="#">Speech 2.8</a></div>
          <div class="col"><h4>Developers</h4><a href="#">API reference</a><a href="#">Quickstart</a><a href="#">Changelog</a><a href="#">Status</a></div>
          <div class="col"><h4>Company</h4><a href="#">About</a><a href="#">Careers</a><a href="#">Press</a><a href="#">Contact</a></div>
          <div class="col"><h4>Resources</h4><a href="#">Blog</a><a href="#">Research</a><a href="#">Trust</a><a href="#">Brand kit</a></div>
        </div>
      </div>
    </section>

    <section id="dodont">
      <h2 class="section"><span class="num">14</span> Do &amp; Don't</h2>
      <p class="section-blurb">The rules that hold the {s["name"]} system together.</p>
      <div class="dodont">
        <div class="item do"><div class="head">Do</div><p>Stay faithful to the variant's shape language — pills in Aurora/Cyber, sharp corners in Noir/Brutalist.</p></div>
        <div class="item dont"><div class="head">Don't</div><p>Mix shape languages. The {s["name"]} variant has a consistent radius signature.</p></div>
        <div class="item do"><div class="head">Do</div><p>Keep the type stack consistent across all variants for fair comparison.</p></div>
        <div class="item dont"><div class="head">Don't</div><p>Apply the {s["name"]} palette to general UI — saturated hues are for product identity only.</p></div>
        <div class="item do"><div class="head">Do</div><p>Test the variant against light and dark environments before committing.</p></div>
        <div class="item dont"><div class="head">Don't</div><p>Forget the mobile breakpoint — every variant must collapse gracefully.</p></div>
      </div>
    </section>

    <hr class="rule" />
    <p style="color:var(--stone);font-size:12.5px">MiniMax Style Guide · variant {n} · {s["name"]} · <a href="styles.html" style="color:inherit">back to all styles</a></p>
  </main>
</div>
</body>
</html>
"""
    return html_doc


def render_index():
    """The nav hub — landing page with preview cards for all 6 styles."""
    cards = []
    # index.html first (the canonical), then 5 variants
    all_meta = [
        ("index.html", "Original", "Canonical · monochrome · pills", "The baseline MiniMax design system. Saturated hues reserved for product identity moments. Pills everywhere.", "#0a0a0a", "#ffffff", "DM Sans / Outfit"),
    ]
    for i, fn in enumerate(STYLES, start=1):
        s = fn()
        preview = {
            "noir": ("#ffffff", "#000000", "IBM Plex Mono / IBM Plex Sans"),
            "aurora": ("linear-gradient(135deg,#fdfcff,#f5f1ff,#fce8f3)", "#2d2454", "Quicksand / Nunito"),
            "brutalist": ("#f4ede1", "#0a0a0a", "Space Mono / Inter"),
            "editorial": ("#f6f1e7", "#0f1e3d", "Playfair Display / Source Serif"),
            "cyber": ("linear-gradient(180deg,#0a0a1a,#12122a)", "#00f0ff", "Orbitron / Inter"),
        }[s["slug"]]
        all_meta.append((f"style-{i}.html", s["name"], s["tag"], preview[2], preview[1], preview[0], preview[2]))

    # Build cards manually since the tuple shape differs for original
    card_html = []
    # Card 0: Original
    card_html.append("""
    <a class="card" href="index.html" style="background:#ffffff;color:#0a0a0a;border-color:#E5E7EB">
      <div class="card-kicker">Style 1 of 6 · Original</div>
      <div class="card-title">Original · DM Sans + Outfit</div>
      <div class="card-body">Canonical MiniMax system. White canvas, 90% monochrome, saturated hues reserved for product identity moments.</div>
      <div class="palette">
        <span class="chip" style="background:#0a0a0a"></span>
        <span class="chip" style="background:#ffffff;border:1px solid #E5E7EB"></span>
        <span class="chip" style="background:#FF5530"></span>
        <span class="chip" style="background:#EA5EC1"></span>
        <span class="chip" style="background:#1456F0"></span>
        <span class="chip" style="background:#A855F7"></span>
      </div>
      <div class="card-meta">DM Sans / Outfit / JetBrains Mono</div>
    </a>
    """)

    for i, fn in enumerate(STYLES, start=1):
        s = fn()
        sw = s["swatches"]
        brand_chips = "".join(
            f'<span class="chip" style="background:{c}"></span>'
            for _, _, _, c in sw["brand"][:5]
        )
        # Pick representative colors for preview header
        ink = sw["ink"][0][3]
        canvas = sw["surface"][0][3]
        card_html.append(f"""
    <a class="card" href="style-{i}.html" style="background:{canvas};color:{ink};border-color:{sw['hairline'][0][3]}">
      <div class="card-kicker">Style {i+1} of 6 · {s["name"]}</div>
      <div class="card-title">{s["name"]}</div>
      <div class="card-body">{html.escape(s["tag"])}. Same 14-section content, different visual system. Click to preview the full guide.</div>
      <div class="palette">{brand_chips}</div>
      <div class="card-meta">{html.escape(s["name"])} tokens · preview →</div>
    </a>
    """)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>MiniMax Style · All Variants</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Outfit:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --canvas:#ffffff;--surface:#f7f8fa;--surface-soft:#f2f3f5;
      --ink:#0a0a0a;--ink-2:#18181B;--charcoal:#222;--slate:#45515E;--steel:#5F5F5F;--stone:#8E8E93;--muted:#A8AAB2;
      --hairline:#E5E7EB;--hairline-soft:#EAECF0;
      --brand-coral:#FF5530;--brand-magenta:#EA5EC1;--brand-blue:#1456F0;--brand-cyan:#3DAEFF;--brand-purple:#A855F7;
      --shadow-card:0 12px 16px -4px rgba(36,36,36,0.08), 0 2px 4px rgba(36,36,36,0.04);
      --shadow-glow:0 0 15px rgba(44,30,116,0.16);
      --r-md:16px;--r-lg:24px;--r-xl:32px;--r-pill:9999px;
    }}
    *{{box-sizing:border-box}}html,body{{margin:0;padding:0}}
    body{{font-family:"DM Sans","Helvetica Neue",Helvetica,Arial,sans-serif;background:var(--canvas);color:var(--ink);line-height:1.5;-webkit-font-smoothing:antialiased}}
    code,.mono{{font-family:"JetBrains Mono",ui-monospace,monospace}}
    .page{{max-width:1240px;margin:0 auto;padding:64px 56px 120px}}
    header{{margin-bottom:56px}}
    .kicker{{font-size:12px;text-transform:uppercase;letter-spacing:0.18em;color:var(--stone);font-weight:600;margin-bottom:10px}}
    h1{{font-family:"Outfit",sans-serif;font-size:64px;font-weight:600;letter-spacing:-0.025em;line-height:1.05;margin:0 0 16px}}
    .lead{{font-size:18px;color:var(--slate);max-width:760px;margin:0 0 36px;line-height:1.6}}
    .toolbar{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:40px;padding:18px 22px;background:var(--surface);border:1px solid var(--hairline);border-radius:var(--r-md)}}
    .toolbar .label{{font-size:11.5px;text-transform:uppercase;letter-spacing:0.12em;color:var(--stone);font-weight:700;margin-right:6px}}
    .toolbar a{{display:inline-flex;align-items:center;gap:8px;padding:8px 16px;background:#fff;border:1px solid var(--hairline);border-radius:var(--r-pill);color:var(--ink);text-decoration:none;font-size:13.5px;font-weight:500;transition:all 0.15s ease}}
    .toolbar a:hover{{background:var(--ink);color:#fff;border-color:var(--ink)}}
    .toolbar a.primary{{background:var(--ink);color:#fff;border-color:var(--ink)}}
    .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:22px}}
    .card{{display:flex;flex-direction:column;gap:10px;padding:28px;border:1px solid var(--hairline);border-radius:var(--r-lg);text-decoration:none;transition:all 0.2s ease;box-shadow:var(--shadow-card);min-height:280px}}
    .card:hover{{transform:translateY(-3px);box-shadow:0 18px 28px -10px rgba(36,36,36,0.15),0 4px 8px rgba(36,36,36,0.06)}}
    .card .card-kicker{{font-size:11px;text-transform:uppercase;letter-spacing:0.14em;font-weight:700;opacity:0.7}}
    .card .card-title{{font-family:"Outfit",sans-serif;font-weight:600;font-size:24px;letter-spacing:-0.015em;line-height:1.15;margin:0}}
    .card .card-body{{font-size:14px;line-height:1.55;opacity:0.78;flex-grow:1}}
    .card .palette{{display:flex;gap:6px;margin-top:6px}}
    .card .palette .chip{{width:24px;height:24px;border-radius:6px;display:block;border:1px solid rgba(0,0,0,0.08)}}
    .card .card-meta{{font-family:"JetBrains Mono",monospace;font-size:11.5px;opacity:0.6;margin-top:6px;text-transform:uppercase;letter-spacing:0.06em}}
    .compare{{margin-top:64px;padding:36px;background:var(--surface);border:1px solid var(--hairline);border-radius:var(--r-lg)}}
    .compare h2{{font-family:"Outfit",sans-serif;font-size:22px;font-weight:600;margin:0 0 14px}}
    .compare p{{margin:0 0 18px;color:var(--slate);font-size:14px;line-height:1.6}}
    .compare-table{{width:100%;border-collapse:collapse;font-size:13px;background:#fff;border-radius:var(--r-md);overflow:hidden;border:1px solid var(--hairline)}}
    .compare-table th,.compare-table td{{text-align:left;padding:11px 14px;border-bottom:1px solid var(--hairline-soft)}}
    .compare-table th{{font-size:11px;text-transform:uppercase;letter-spacing:0.08em;color:var(--stone);font-weight:700;background:var(--surface-soft)}}
    .compare-table td .name{{font-weight:600}}
    .compare-table td .desc{{font-size:11.5px;color:var(--slate);margin-top:2px}}
    .compare-table td a{{color:var(--brand-blue);text-decoration:none;font-weight:600}}
    .compare-table td a:hover{{text-decoration:underline}}
    footer{{margin-top:64px;text-align:center;color:var(--stone);font-size:12.5px}}
    @media (max-width:720px){{.page{{padding:32px 20px 80px}}h1{{font-size:42px}}.grid{{grid-template-columns:1fr}}}}
  </style>
</head>
<body>
<div class="page">
  <header>
    <div class="kicker">MiniMax Design System · Variant Explorer</div>
    <h1>Six style guides. One brand.</h1>
    <p class="lead">
      Each variant below restates the same MiniMax design system with a different visual language.
      Same 14 sections, same content, same brand voice — only the tokens change.
      Use the toolbar to jump to a specific style, or browse the cards to compare side by side.
    </p>
    <div class="toolbar">
      <span class="label">Jump to:</span>
      <a class="primary" href="index.html">1 · Original</a>
      <a href="style-1.html">2 · Noir</a>
      <a href="style-2.html">3 · Aurora</a>
      <a href="style-3.html">4 · Brutalist</a>
      <a href="style-4.html">5 · Editorial</a>
      <a href="style-5.html">6 · Cyber-Synthwave</a>
    </div>
  </header>

  <section class="grid">
    {"".join(card_html)}
  </section>

  <section class="compare">
    <h2>Side-by-side comparison</h2>
    <p>Pick the variant whose shape, color, and voice match the brand context. All variants are static, self-contained, and served by GitHub Pages.</p>
    <table class="compare-table">
      <thead><tr><th>#</th><th>Variant</th><th>Shape</th><th>Surface</th><th>Display font</th><th>Open</th></tr></thead>
      <tbody>
        <tr><td>1</td><td><div class="name">Original</div><div class="desc">Canonical MiniMax</div></td><td>Pills (9999px)</td><td>White</td><td>Outfit 600</td><td><a href="index.html">index.html →</a></td></tr>
        <tr><td>2</td><td><div class="name">Noir</div><div class="desc">Monochrome · terminal · zine</div></td><td>Sharp (0px)</td><td>White / black</td><td>IBM Plex Mono 700</td><td><a href="style-1.html">style-1.html →</a></td></tr>
        <tr><td>3</td><td><div class="name">Aurora</div><div class="desc">Pastel · glass · friendly</div></td><td>Rounded (28px)</td><td>Lilac gradient</td><td>Quicksand 700</td><td><a href="style-2.html">style-2.html →</a></td></tr>
        <tr><td>4</td><td><div class="name">Brutalist</div><div class="desc">Neon · sharp · oversized</div></td><td>Sharp (0px)</td><td>Cream</td><td>Space Mono 700</td><td><a href="style-3.html">style-3.html →</a></td></tr>
        <tr><td>5</td><td><div class="name">Editorial</div><div class="desc">Serif · newspaper · warm</div></td><td>Soft (4–12px)</td><td>Cream</td><td>Playfair Display 700</td><td><a href="style-4.html">style-4.html →</a></td></tr>
        <tr><td>6</td><td><div class="name">Cyber-Synthwave</div><div class="desc">Neon · dark · geometric</div></td><td>Rounded (12–24px)</td><td>Deep purple / navy</td><td>Orbitron 800</td><td><a href="style-5.html">style-5.html →</a></td></tr>
      </tbody>
    </table>
  </section>

  <footer>MiniMax Style Guide · variant explorer · 2026 · <a href="https://github.com/kajica2/minimax_style" style="color:inherit">github.com/kajica2/minimax_style</a></footer>
</div>
</body>
</html>
"""


def main():
    for i, style_fn in enumerate(STYLES, start=1):
        s = style_fn()
        path = os.path.join(OUT_DIR, f"style-{i}.html")
        with open(path, "w") as f:
            f.write(render_page(s, i + 1))  # i+1 because Original is style 1
        print(f"wrote {path} ({os.path.getsize(path):,} bytes)")
    # Nav hub lives at styles.html — keep index.html as the canonical Original.
    hub_path = os.path.join(OUT_DIR, "styles.html")
    with open(hub_path, "w") as f:
        f.write(render_index())
    print(f"wrote {hub_path} (navigation hub, {os.path.getsize(hub_path):,} bytes)")
    print("  -> index.html untouched (canonical Original preserved)")


if __name__ == "__main__":
    main()
