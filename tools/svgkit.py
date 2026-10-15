"""Tiny SVG toolkit: measured text, wrapping, and per-file subsetted, embedded fonts.

GitHub shows README images through <img>, which cannot fetch web fonts, so every
SVG carries its own WOFF2 subset (only the glyphs it uses) as a data URI.
"""
import base64
import io
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont

_HERE = Path(__file__).parent
FD = next((d for d in [_HERE / "node_modules/@fontsource", _HERE / "fonts/node_modules/@fontsource"] if d.exists()),
          _HERE / "node_modules/@fontsource")
FONT_FILES = {
    ("sg", 500): FD / "space-grotesk/files/space-grotesk-latin-500-normal.woff2",
    ("sg", 700): FD / "space-grotesk/files/space-grotesk-latin-700-normal.woff2",
    ("sans", 400): FD / "ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2",
    ("sans", 500): FD / "ibm-plex-sans/files/ibm-plex-sans-latin-500-normal.woff2",
    ("mono", 400): FD / "ibm-plex-mono/files/ibm-plex-mono-latin-400-normal.woff2",
    ("mono", 500): FD / "ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2",
}
FALLBACK = {
    "sg": "'Space Grotesk','Segoe UI',Helvetica,Arial,sans-serif",
    "sans": "'IBM Plex Sans','Segoe UI',Helvetica,Arial,sans-serif",
    "mono": "'IBM Plex Mono',ui-monospace,Menlo,Consolas,monospace",
}

_metrics = {}


def _font(key):
    if key not in _metrics:
        f = TTFont(FONT_FILES[key])
        _metrics[key] = (f.getBestCmap(), f["hmtx"].metrics, f["head"].unitsPerEm)
    return _metrics[key]


def measure(s, fam, wt, size, ls=0.0):
    cmap, hmtx, upm = _font((fam, wt))
    total = 0
    for ch in s:
        g = cmap.get(ord(ch))
        if g is None:
            raise ValueError(f"glyph {ch!r} missing from {fam} {wt}")
        total += hmtx[g][0]
    return total / upm * size + ls * len(s)


def wrap(text, fam, wt, size, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if measure(trial, fam, wt, size) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fid(fam, wt):
    return f"ecn-{fam}-{wt}"


class Svg:
    def __init__(self, w, h, title, desc=""):
        self.w, self.h, self.title, self.desc = w, h, title, desc
        self.parts, self.defs, self.css = [], [], []
        self.used = {}

    def add(self, *parts):
        self.parts.extend(parts)

    def text(self, x, y, s, fam, wt, size, fill, anchor="start", ls=0.0, extra=""):
        self.used.setdefault((fam, wt), set()).update(s)
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        l = f' letter-spacing="{ls:g}"' if ls else ""
        return (f'<text x="{x:g}" y="{y:g}" font-family="{fid(fam, wt)},{FALLBACK[fam]}" '
                f'font-size="{size:g}" fill="{fill}"{a}{l}{extra}>{escape(s)}</text>')

    def _fontface(self):
        out = []
        for (fam, wt), chars in sorted(self.used.items()):
            opts = subset.Options()
            opts.flavor = "woff2"
            opts.layout_features = ["kern", "liga"]
            opts.name_IDs = []
            opts.notdef_outline = True
            f = TTFont(FONT_FILES[(fam, wt)], recalcTimestamp=False)
            sub = subset.Subsetter(opts)
            sub.populate(text="".join(chars) + " ")
            sub.subset(f)
            buf = io.BytesIO()
            f["head"].modified = f["head"].created  # deterministic output
            f.flavor = "woff2"
            f.save(buf)
            b64 = base64.b64encode(buf.getvalue()).decode()
            out.append(f"@font-face{{font-family:{fid(fam, wt)};"
                       f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
        return "".join(out)

    def render(self):
        style = self._fontface() + "".join(self.css)
        defs = "".join(self.defs)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="t d">'
                f'<title id="t">{escape(self.title)}</title><desc id="d">{escape(self.desc)}</desc>'
                f'<style>{style}</style><defs>{defs}</defs>' + "".join(self.parts) + "</svg>")
