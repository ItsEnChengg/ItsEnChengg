"""Generate every SVG asset for EnChengg's GitHub profile README."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Svg, measure, wrap  # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
(OUT / "assets/light").mkdir(parents=True, exist_ok=True)
(OUT / "assets/dark").mkdir(parents=True, exist_ok=True)

DARK = dict(name="dark", card="#10161D", panel="#141C24", border="#25303A", ink="#F3F1EA",
            ink2="#C9D1D8", mute="#93A0AC", acc="#F2A541", accg="#F2A541", dot="#283440",
            chip="#34414D", soft=0.14, street="#1E2832")
LIGHT = dict(name="light", card="#FFFFFF", panel="#F6F5F0", border="#DCDBD3", ink="#111418",
             ink2="#3D434A", mute="#5B6169", acc="#B45309", accg="#D97706", dot="#DAD9D0",
             chip="#CFCEC5", soft=0.10, street="#E7E6DE")
BRAND = dict(bg="#0F151B", ink="#F3F1EA", ink2="#C9D1D8", mute="#8E9BA7",
             acc="#F2A541", edge="#222C36")

def save(svg, rel):
    path = OUT / "assets" / rel
    path.write_text(svg.render(), encoding="utf-8", newline="\n")
    return path


def chip(s, x, cy, label, fill=None, stroke=None, color="#000", fam="mono", wt=500, size=16,
         padx=14, h=36, fill_op=1.0):
    w = measure(label, fam, wt, size) + padx * 2
    f = f'fill="{fill}" fill-opacity="{fill_op}"' if fill else 'fill="none"'
    st = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ""
    s.add(f'<rect x="{x:g}" y="{cy - h / 2:g}" width="{w:.1f}" height="{h}" rx="{h / 2:g}" {f}{st}/>',
          s.text(x + padx, cy + size * 0.36, label, fam, wt, size, color))
    return w


# --------------------------------------------------------------------------- hero
def hero():
    W, X = 1280, 64
    B = BRAND
    summary = ("Full-stack AI systems, messy data turned into decisions, serverless apps on AWS "
               "and responsible AI in practice.")
    lines = wrap(summary, "sans", 400, 26, W - 2 * X - 120)
    assert len(lines) <= 2, lines
    H = 262 + len(lines) * 36 + 70
    s = Svg(W, H, "En Cheng Neo",
            "Diploma in Applied AI and Analytics student at Nanyang Polytechnic, Singapore. "
            + summary + " Open to 2027 internships in applied AI and data analytics.")
    s.add(f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="18" fill="{B["bg"]}" '
          f'stroke="{B["edge"]}" stroke-width="1.5"/>',
          s.text(X, 84, "Diploma in Applied AI & Analytics, Nanyang Polytechnic", "sans", 500, 21, B["ink2"]))
    assert measure("En Cheng Neo", "sg", 700, 96, -1.5) < W - 2 * X
    s.add(s.text(X - 3, 184, "En Cheng Neo", "sg", 700, 96, B["ink"], ls=-1.5))
    for i, ln in enumerate(lines):
        s.add(s.text(X, 246 + i * 36, ln, "sans", 400, 26, B["ink2"]))
    s.add(s.text(X, 246 + len(lines) * 36 + 22, "Open to 2027 internships in applied AI and data analytics.",
                 "sans", 500, 22, B["acc"]))
    save(s, "hero.svg")


# ------------------------------------------------------------------------- badges
ICONS = {
    "linkedin": '<rect x="2" y="3" width="20" height="18" rx="3"/><circle cx="8.5" cy="10" r="2.5"/>'
                '<path d="M4.8 17c.8-2 2-3 3.7-3s2.9 1 3.7 3M15 9h4M15 13h4"/>',
    "email": '<rect x="2" y="5" width="20" height="14" rx="2.5"/><path d="M3 7l9 6 9-6"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "code": '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M13.5 5l-3 14"/>',
}


def badge(fname, icon, label, title):
    B = BRAND
    h, size = 40, 15
    w = 16 + 20 + 10 + measure(label, "mono", 500, size) + 18
    s = Svg(round(w), h, title)
    s.add(f'<rect x=".75" y=".75" width="{w - 1.5:.1f}" height="{h - 1.5}" rx="{(h - 1.5) / 2}" '
          f'fill="#10161D" stroke="#2A3742" stroke-width="1.5"/>',
          f'<g transform="translate(16 10) scale(.8333)" fill="none" stroke="{B["acc"]}" stroke-width="2.2" '
          f'stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>',
          s.text(46, 25.5, label, "mono", 500, size, B["ink"]))
    save(s, fname)


# ---------------------------------------------------------------- section headers
SECTIONS = [("about", "About me"), ("toolkit", "Toolkit"),
            ("credentials", "Credentials"), ("now", "Right now")]


def header(T, slug, title):
    s = Svg(1200, 92, title)
    s.add(s.text(0, 74, title, "sg", 700, 38, T["ink"], ls=-0.5))
    save(s, f'{T["name"]}/h-{slug}.svg')


# --------------------------------------------------------------- stack icon grid
ICON_DIR = next((d for d in [Path(__file__).parent / "skill-icons/icons",
                 Path(__file__).parent / "dl/skill-icons/icons"] if d.exists()),
                Path(__file__).parent / "skill-icons/icons")   # MIT, (c) 2022 tandpfun
STACK = [("Python", "Python"), ("JavaScript", "JavaScript"), ("HTML", "HTML"), ("CSS", "CSS"),
         ("React", "React"), ("Vite", "Vite"), ("NodeJS", "Node.js"), ("ExpressJS", "Express"),
         ("Flask", "Flask"), ("TailwindCSS", "Tailwind"), ("PostgreSQL", "PostgreSQL"),
         ("Supabase", "Supabase"), ("MySQL", "MySQL"), ("AWS", "AWS"),
         ("GithubActions", "Actions"), ("Git", "Git")]


def icon_inner(name, theme, k):
    import re
    f = ICON_DIR / f"{name}-{theme}.svg"
    if not f.exists():
        f = ICON_DIR / f"{name}.svg"
    raw = f.read_text()
    inner = re.match(r"\s*<svg[^>]*>(.*)</svg>\s*$", raw, re.S).group(1)
    inner = re.sub(r'id="([^"]+)"', rf'id="s{k}-\1"', inner)
    inner = re.sub(r"url\(#([^)]+)\)", rf"url(#s{k}-\1)", inner)
    inner = re.sub(r'href="#([^"]+)"', rf'href="#s{k}-\1"', inner)
    return inner


def stack(T):
    W, cols, pad, icon = 1200, 8, 36, 64
    cw = (W - 2 * pad) / cols
    rowh = icon + 12 + 18 + 30
    H = pad + rowh * 2 - 30 + pad - 6
    s = Svg(W, int(H), "Languages, frameworks and platforms", ", ".join(l for _, l in STACK) + ".")
    s.add(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="{T["card"]}" '
          f'stroke="{T["border"]}" stroke-width="2"/>')
    theme = "Light" if T["name"] == "light" else "Dark"
    for k, (name, label) in enumerate(STACK):
        cx = pad + (k % cols) * cw + cw / 2
        y = pad + (k // cols) * rowh
        s.add(f'<svg x="{cx - icon / 2:.1f}" y="{y}" width="{icon}" height="{icon}" viewBox="0 0 256 256" fill="none">'
              + icon_inner(name, theme, k) + "</svg>",
              s.text(cx, y + icon + 26, label, "mono", 400, 15, T["ink2"], anchor="middle"))
    save(s, f'{T["name"]}/stack.svg')

# ------------------------------------------------------------------ toolkit card
PRACTICES = [
    ("Data & AI", ["pandas", "KNIME", "data wrangling", "forecasting", "computer vision",
                   "text-to-SQL", "LLM APIs & agents"]),
    ("Cloud", ["AWS Lambda", "API Gateway", "S3", "DynamoDB", "SAM", "Alibaba Cloud", "Railway", "Netlify"]),
    ("Responsible AI", ["accountability & transparency", "IT governance (COBIT)", "source-grounded AI output",
                        "privacy-first design"]),
]


def toolkit(T):
    W = 1200
    rows, y = [], 52
    LX, CX, R = 36, 252, W - 36
    for label, items in PRACTICES:
        lines, cur, x = [], [], CX
        for it in items:
            w = measure(it, "mono", 400, 16) + 28
            if x + w > R and cur:
                lines.append(cur)
                cur, x = [], CX
            cur.append(it)
            x += w + 8
        lines.append(cur)
        rows.append((label, lines, y))
        last_bottom = y + 5 + (len(lines) - 1) * 48 + 18
        y += len(lines) * 48 + 30
    H = last_bottom + 34
    s = Svg(W, int(H), "Toolkit: practices and platforms",
            " ".join(f"{l}: {', '.join(i)}." for l, i in PRACTICES))
    s.add(f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="{T["card"]}" '
          f'stroke="{T["border"]}" stroke-width="2"/>')
    for k, (label, lines, y0) in enumerate(rows):
        if k:
            s.add(f'<line x1="{LX}" y1="{y0 - 23}" x2="{R}" y2="{y0 - 23}" stroke="{T["border"]}" stroke-width="1.5"/>')
        s.add(s.text(LX, y0 + 11, label, "sans", 500, 18, T["ink"]))
        for j, ln in enumerate(lines):
            x = CX
            for it in ln:
                x += chip(s, x, y0 + 5 + j * 48, it, stroke=T["chip"], color=T["ink2"], wt=400) + 8
    save(s, f'{T["name"]}/toolkit.svg')


# -------------------------------------------------------------- credentials card
CREDS = [
    ("cert", "AWS · Foundational", "AWS Certified Cloud Practitioner"),
    ("cert", "Alibaba Cloud · Associate", "Certified Associate: Cloud Engineer"),
    ("cert", "AI Singapore", "AI4I Literacy in AI"),
    ("cert", "KNIME", "Basic Proficiency in KNIME Analytics Platform"),
]


def credentials(T):
    W, cols, gap, th = 1200, 2, 20, 156
    tw = (W - gap * (cols - 1)) / cols
    H = th * 2 + gap
    s = Svg(W, H, "Credentials",
            "Certifications: " + "; ".join(n for k, _, n in CREDS if k == "cert") + ".")
    for i, (kind, label, name) in enumerate(CREDS):
        x, y = (i % cols) * (tw + gap), (i // cols) * (th + gap)
        s.add(f'<rect x="{x + 1:.1f}" y="{y + 1}" width="{tw - 2:.1f}" height="{th - 2}" rx="15" '
              f'fill="{T["card"]}" stroke="{T["border"]}" stroke-width="2"/>')
        ix, iy = x + 28, y + 24
        s.add(f'<g transform="translate({ix:.1f} {iy})" fill="none" stroke="{T["accg"]}" stroke-width="2.2" '
              f'stroke-linejoin="round" stroke-linecap="round"><path d="M14 1l12 7v14l-12 7-12-7V8z"/>'
              f'<path d="M9 15l3.5 3.5L19.5 11"/></g>')
        s.add(s.text(x + 72, y + 45, label, "sans", 500, 17, T["mute"]))
        lines = wrap(name, "sg", 700, 23, tw - 56)
        assert len(lines) <= 2, lines
        for j, ln in enumerate(lines):
            s.add(s.text(x + 28, y + 96 + j * 30, ln, "sg", 700, 23, T["ink"], ls=-0.3))
    save(s, f'{T["name"]}/credentials.svg')


# --------------------------------------------------------------------------- footer
def footer():
    W, H = 1280, 96
    B = BRAND
    msg = "Thanks for stopping by. Open to 2027 internships in applied AI and data analytics."
    assert measure(msg, "sans", 400, 22) < W - 128
    s = Svg(W, H, "Thanks for stopping by",
            "Open to 2027 internships in applied AI and data analytics.")
    s.add(f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="18" fill="{B["bg"]}" '
          f'stroke="{B["edge"]}" stroke-width="1.5"/>',
          s.text(64, 56, msg, "sans", 400, 22, B["ink2"]))
    save(s, "footer.svg")


if __name__ == "__main__":
    hero()
    footer()
    badge("badge-linkedin.svg", "linkedin", "LinkedIn", "LinkedIn profile")
    badge("badge-email.svg", "email", "neoencheng.work@gmail.com", "Email")
    badge("badge-location.svg", "pin", "Singapore", "Based in Singapore")
    for T in (LIGHT, DARK):
        for slug, title in SECTIONS:
            header(T, slug, title)
        stack(T)
        toolkit(T)
        credentials(T)
    for f in sorted((OUT / "assets").rglob("*.svg")):
        print(f"{f.relative_to(OUT)}  {f.stat().st_size / 1024:.1f} KB")
