"""Generate every SVG asset for EnChengg's GitHub profile README."""
import math
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
BRAND = dict(bg="#0F151B", grid="#1A232C", ink="#F3F1EA", ink2="#C9D1D8", mute="#8E9BA7",
             acc="#F2A541", dot="#273340", chipb="#33424F", edge="#222C36")

MOTION = ("@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
          "@keyframes ping{0%{transform:scale(1);opacity:.75}100%{transform:scale(3.2);opacity:0}}"
          ".ping{opacity:0;transform-box:fill-box;transform-origin:center;"
          "animation:ping 2.4s ease-out infinite}")


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


def ping_dot(s, cx, cy, r, color, delay=0):
    s.add(f'<circle class="ping" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" '
          f'stroke-width="2" style="animation-delay:{delay}s"/>',
          f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>')


# --------------------------------------------------------------------------- hero
HEIGHTS = [1, 2, 1, 2, 3, 2, 4, 3, 5, 6, 6, 8]


def dot_columns(s, x0, base, step, r, heights, top_color, rest_color, delay0=0.25):
    tops = []
    for i, n in enumerate(heights):
        x = x0 + i * step
        dots = []
        for k in range(n):
            y = base - k * step
            c = top_color if k == n - 1 else rest_color
            dots.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>')
        s.add(f'<g class="col" style="animation-delay:{delay0 + i * 0.06:.2f}s">' + "".join(dots) + "</g>")
        tops.append((x, base - (n - 1) * step))
    return tops


def hero():
    W, H = 1280, 440
    B = BRAND
    s = Svg(W, H, "En Cheng Neo",
            "Diploma in Applied AI and Analytics student at Nanyang Polytechnic, Singapore. "
            "Building full-stack AI systems, turning messy data into decisions, deploying serverless "
            "apps on AWS and putting responsible AI into practice. Open to 2027 internships.")
    s.defs.append(f'<clipPath id="cl"><rect width="{W}" height="{H}" rx="22"/></clipPath>'
                  f'<pattern id="gr" width="40" height="40" patternUnits="userSpaceOnUse">'
                  f'<path d="M40 0H0V40" fill="none" stroke="{B["grid"]}" stroke-width="1"/></pattern>'
                  '<linearGradient id="fadeg" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity=".25"/>'
                  '<stop offset="1" stop-color="#fff"/></linearGradient>'
                  f'<mask id="gm"><rect width="{W}" height="{H}" fill="url(#fadeg)"/></mask>'
                  '<radialGradient id="glow" cx=".82" cy=".72" r=".55">'
                  f'<stop offset="0" stop-color="{B["acc"]}" stop-opacity=".16"/>'
                  f'<stop offset="1" stop-color="{B["acc"]}" stop-opacity="0"/></radialGradient>'
                  '<linearGradient id="area" x1="0" x2="0" y1="0" y2="1">'
                  f'<stop offset="0" stop-color="{B["acc"]}" stop-opacity=".22"/>'
                  f'<stop offset="1" stop-color="{B["acc"]}" stop-opacity="0"/></linearGradient>')
    s.add('<g clip-path="url(#cl)">',
          f'<rect width="{W}" height="{H}" fill="{B["bg"]}"/>',
          f'<rect width="{W}" height="{H}" fill="url(#gr)" mask="url(#gm)"/>',
          f'<rect width="{W}" height="{H}" fill="url(#glow)"/>', "</g>",
          f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="21.5" fill="none" stroke="{B["edge"]}" stroke-width="1.5"/>')

    X = 72
    label = "DIPLOMA IN APPLIED AI & ANALYTICS · NANYANG POLYTECHNIC"
    s.add(f'<rect x="{X}" y="83" width="12" height="12" fill="{B["acc"]}"/>',
          s.text(X + 26, 95, label, "mono", 500, 16, B["acc"], ls=2.4))
    name_size = 112
    assert measure("En Cheng Neo", "sg", 700, name_size, -2.2) < 720
    s.add(s.text(X - 4, 206, "En Cheng Neo", "sg", 700, name_size, B["ink"], ls=-2.2))

    # typing line (SMIL, so it also runs inside GitHub's <img>)
    size, cw, base = 28, 16.8, 270
    x0 = X + 2 * cw
    phrases = ["building full-stack AI systems", "turning messy data into decisions",
               "deploying serverless apps on AWS", "putting responsible AI into practice"]
    D, tt, hold, dt = 5.0, 1.6, 2.5, 0.55
    T = D * len(phrases)
    s.add(s.text(X, base, ">", "mono", 500, size, B["acc"]))
    cursor = [(0.0, 0.0)]
    for i, p in enumerate(phrases):
        n, st = len(p), i * D
        ev = [(0.0, 0.0)] if st > 0 else []
        ev += [(st + k * tt / n, k * cw) for k in range(1, n + 1)]
        ev += [(st + tt + hold + k * dt / n, (n - k) * cw) for k in range(1, n + 1)]
        if st == 0:
            ev = [(0.0, 0.0)] + ev
        cursor += [e for e in ev if e[0] > 0]
        kt = ";".join(f"{t / T:.4f}" for t, _ in ev)
        vals = ";".join(f"{w:.1f}" for _, w in ev)
        s.defs.append(f'<clipPath id="tp{i}"><rect x="{x0}" y="{base - 30}" width="0" height="42">'
                      f'<animate attributeName="width" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
                      f'keyTimes="{kt}" values="{vals}"/></rect></clipPath>')
        s.add(s.text(x0, base, p, "mono", 400, size, B["ink2"], extra=f' clip-path="url(#tp{i})"'))
        assert x0 + n * cw < 760, p
    cursor.sort()
    kt = ";".join(f"{t / T:.4f}" for t, _ in cursor)
    vals = ";".join(f"{x0 + 4 + w:.1f}" for _, w in cursor)
    s.add(f'<rect class="blink" x="{x0 + 4}" y="{base - 24}" width="13" height="30" fill="{B["acc"]}">'
          f'<animate attributeName="x" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
          f'keyTimes="{kt}" values="{vals}"/></rect>')

    # skill chips
    x = X
    for c in ["Python", "React", "Node.js", "AWS", "Responsible AI"]:
        x += chip(s, x, 352, c, stroke=B["chipb"], color=B["ink2"], size=16, h=38) + 10

    # status pill, top right
    st_label = "OPEN TO 2027 INTERNSHIPS"
    pw = measure(st_label, "mono", 500, 14, 1.6) + 54
    px = 1208 - pw
    s.add(f'<rect x="{px:.1f}" y="66" width="{pw:.1f}" height="36" rx="18" fill="{B["acc"]}" '
          f'fill-opacity=".1" stroke="{B["acc"]}" stroke-opacity=".55" stroke-width="1.5"/>',
          f'<circle class="pulse" cx="{px + 22:.1f}" cy="84" r="5" fill="{B["acc"]}"/>',
          s.text(px + 38, 89, st_label, "mono", 500, 14, B["acc"], ls=1.6))

    # rising dot columns + trend line
    tops = dot_columns(s, 840, 374, 32, 6, HEIGHTS, B["acc"], B["dot"])
    pts = " ".join(f"{x},{y}" for x, y in tops)
    L = sum(math.dist(tops[i], tops[i + 1]) for i in range(len(tops) - 1))
    area = f"M{tops[0][0]},{tops[0][1]} " + " ".join(f"L{x},{y}" for x, y in tops[1:]) + \
        f" L{tops[-1][0]},388 L{tops[0][0]},388Z"
    s.add(f'<path class="area" d="{area}" fill="url(#area)"/>',
          f'<polyline class="tr" points="{pts}" fill="none" stroke="{B["acc"]}" stroke-width="3" '
          f'stroke-linejoin="round" stroke-linecap="round"/>')
    ex, ey = tops[-1]
    ping_dot(s, ex, ey, 9, B["acc"], delay=2.6)
    s.add(s.text(ex, ey - 24, "now", "mono", 500, 14, B["acc"], anchor="middle"))
    s.add(f'<line x1="826" y1="396" x2="1208" y2="396" stroke="{B["chipb"]}" stroke-width="1.5"/>')

    s.css.append(MOTION + (
        ".col{animation:rise .55s cubic-bezier(.2,.7,.2,1) both}"
        "@keyframes rise{from{opacity:0;transform:translateY(16px)}}"
        f".tr{{stroke-dasharray:{L:.1f};animation:draw 1.6s ease-out 1s both}}"
        f"@keyframes draw{{from{{stroke-dashoffset:{L:.1f}}}to{{stroke-dashoffset:0}}}}"
        ".area{animation:fade 1s ease-out 2.2s both}@keyframes fade{from{opacity:0}}"
        ".blink{animation:blink 1.05s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
        ".pulse{animation:pulse 2s ease-in-out infinite}@keyframes pulse{50%{opacity:.3}}"))
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
SECTIONS = [("about", "01", "About me"), ("toolkit", "02", "Toolkit"),
            ("credentials", "03", "Credentials"), ("now", "04", "Right now")]


def header(T, slug, num, title):
    W, H = 1200, 92
    s = Svg(W, H, f"{num} {title}")
    s.add(s.text(0, 62, num, "mono", 500, 22, T["acc"], ls=1),
          s.text(46, 64, title, "sg", 700, 40, T["ink"], ls=-0.6))
    end = 46 + measure(title, "sg", 700, 40, -0.6) + 28
    s.add(f'<line x1="{end:.1f}" y1="50" x2="1180" y2="50" stroke="{T["border"]}" stroke-width="2"/>',
          f'<circle cx="1188" cy="50" r="6" fill="{T["accg"]}"/>')
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
    ("DATA & AI", ["pandas", "KNIME", "data wrangling", "forecasting", "computer vision",
                   "text-to-SQL", "LLM APIs & agents"]),
    ("CLOUD", ["AWS Lambda", "API Gateway", "S3", "DynamoDB", "SAM", "Alibaba Cloud", "Railway", "Netlify"]),
    ("RESPONSIBLE AI", ["accountability & transparency", "IT governance (COBIT)", "source-grounded AI output",
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
        s.add(f'<rect x="{LX}" y="{y0 - 1}" width="10" height="10" fill="{T["accg"]}"/>',
              s.text(LX + 22, y0 + 10, label, "mono", 500, 15, T["acc"], ls=1.5))
        for j, ln in enumerate(lines):
            x = CX
            for it in ln:
                x += chip(s, x, y0 + 5 + j * 48, it, stroke=T["chip"], color=T["ink2"], wt=400) + 8
    save(s, f'{T["name"]}/toolkit.svg')


# -------------------------------------------------------------- credentials card
CREDS = [
    ("cert", "AWS · FOUNDATIONAL", "AWS Certified Cloud Practitioner"),
    ("cert", "ALIBABA CLOUD · ASSOCIATE", "Certified Associate: Cloud Engineer"),
    ("cert", "AI SINGAPORE", "AI4I Literacy in AI"),
    ("cert", "KNIME", "Basic Proficiency in KNIME Analytics Platform"),
    ("medal", "NYP · DISTINCTION", "Data Wrangling"),
    ("medal", "NYP · DISTINCTION", "Cybersecurity Technologies & Ethics"),
]


def credentials(T):
    W, cols, gap, th = 1200, 3, 20, 156
    tw = (W - gap * (cols - 1)) / cols
    H = th * 2 + gap
    s = Svg(W, H, "Credentials",
            "Certifications: " + "; ".join(n for k, _, n in CREDS if k == "cert") +
            ". Distinctions at Nanyang Polytechnic: Data Wrangling; Cybersecurity Technologies and Ethics.")
    for i, (kind, label, name) in enumerate(CREDS):
        x, y = (i % cols) * (tw + gap), (i // cols) * (th + gap)
        s.add(f'<rect x="{x + 1:.1f}" y="{y + 1}" width="{tw - 2:.1f}" height="{th - 2}" rx="15" '
              f'fill="{T["card"]}" stroke="{T["border"]}" stroke-width="2"/>')
        ix, iy = x + 28, y + 24
        if kind == "cert":
            s.add(f'<g transform="translate({ix:.1f} {iy})" fill="none" stroke="{T["accg"]}" stroke-width="2.2" '
                  f'stroke-linejoin="round" stroke-linecap="round"><path d="M14 1l12 7v14l-12 7-12-7V8z"/>'
                  f'<path d="M9 15l3.5 3.5L19.5 11"/></g>')
        else:
            s.add(f'<g transform="translate({ix:.1f} {iy})" fill="none" stroke="{T["accg"]}" stroke-width="2.2" '
                  f'stroke-linejoin="round" stroke-linecap="round"><circle cx="14" cy="11" r="9"/>'
                  f'<path d="M9 18.5L6 29l8-4 8 4-3-10.5"/><path d="M14 6.5l1.4 2.8 3 .4-2.2 2.1.5 3-2.7-1.4-2.7 1.4.5-3-2.2-2.1 3-.4z" stroke-width="1.4"/></g>')
        s.add(s.text(x + 72, y + 44, label, "mono", 500, 14, T["acc"], ls=1.4))
        lines = wrap(name, "sg", 700, 23, tw - 56)
        assert len(lines) <= 2, lines
        for j, ln in enumerate(lines):
            s.add(s.text(x + 28, y + 96 + j * 30, ln, "sg", 700, 23, T["ink"], ls=-0.3))
    save(s, f'{T["name"]}/credentials.svg')


# --------------------------------------------------------------------------- footer
def footer():
    W, H = 1280, 250
    B = BRAND
    s = Svg(W, H, "Thanks for stopping by",
            "Open to 2027 internships in applied AI and data analytics.")
    s.defs.append(f'<clipPath id="cl"><rect width="{W}" height="{H}" rx="22"/></clipPath>'
                  f'<pattern id="gr" width="40" height="40" patternUnits="userSpaceOnUse">'
                  f'<path d="M40 0H0V40" fill="none" stroke="{B["grid"]}" stroke-width="1"/></pattern>'
                  '<radialGradient id="glow" cx=".85" cy=".8" r=".6">'
                  f'<stop offset="0" stop-color="{B["acc"]}" stop-opacity=".14"/>'
                  f'<stop offset="1" stop-color="{B["acc"]}" stop-opacity="0"/></radialGradient>')
    s.add('<g clip-path="url(#cl)">', f'<rect width="{W}" height="{H}" fill="{B["bg"]}"/>',
          f'<rect width="{W}" height="{H}" fill="url(#gr)" opacity=".7"/>',
          f'<rect width="{W}" height="{H}" fill="url(#glow)"/></g>',
          f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="21.5" fill="none" stroke="{B["edge"]}" stroke-width="1.5"/>')
    s.add(f'<rect x="72" y="70" width="10" height="10" fill="{B["acc"]}"/>',
          s.text(94, 80, "THANKS FOR STOPPING BY", "mono", 500, 15, B["acc"], ls=2.2),
          s.text(68, 144, "Let's build something useful.", "sg", 700, 52, B["ink"], ls=-1.2),
          s.text(72, 190, "Open to 2027 internships in applied AI and data analytics.", "sans", 400, 22, B["ink2"]))
    tops = dot_columns(s, 1000, 196, 24, 4.5, [1, 2, 2, 3, 4, 4, 5, 6], B["acc"], B["dot"], delay0=0.1)
    L = sum(math.dist(tops[i], tops[i + 1]) for i in range(len(tops) - 1))
    s.add(f'<polyline class="tr" points="{" ".join(f"{x},{y}" for x, y in tops)}" fill="none" '
          f'stroke="{B["acc"]}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>')
    ex, ey = tops[-1]
    ping_dot(s, ex, ey, 6.5, B["acc"], delay=1.6)
    s.css.append(MOTION + ".col{animation:rise .5s ease-out both}"
                 "@keyframes rise{from{opacity:0;transform:translateY(12px)}}"
                 f".tr{{stroke-dasharray:{L:.1f};animation:draw 1.2s ease-out .7s both}}"
                 f"@keyframes draw{{from{{stroke-dashoffset:{L:.1f}}}to{{stroke-dashoffset:0}}}}")
    save(s, "footer.svg")


if __name__ == "__main__":
    hero()
    footer()
    badge("badge-linkedin.svg", "linkedin", "LinkedIn", "LinkedIn profile")
    badge("badge-email.svg", "email", "neoencheng.work@gmail.com", "Email")
    badge("badge-location.svg", "pin", "Singapore", "Based in Singapore")
    for T in (LIGHT, DARK):
        for slug, num, title in SECTIONS:
            header(T, slug, num, title)
        stack(T)
        toolkit(T)
        credentials(T)
    for f in sorted((OUT / "assets").rglob("*.svg")):
        print(f"{f.relative_to(OUT)}  {f.stat().st_size / 1024:.1f} KB")
