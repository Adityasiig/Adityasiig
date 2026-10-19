"""Sumi-e theme: ink-wash artwork as the whole visual system.

Built from the reference painting itself rather than an imitation of
it. The source is stored rotated 90 degrees (portrait file, landscape
composition), so everything here rotates it first.

The palette is taken from the painting, not invented:
  ink    near-black, the storm
  paper  warm bone, the sky
  mist / stone / slate, the greys between them

Strictly monochrome. The painting is black ink on paper and the only
colour in it is the ribbon itself — so the ribbon stays the only colour
anywhere, and it lives in the artwork, never in the chrome. No red in
type, rules, badges or borders.

Outputs are PNG (the artwork is photographic) plus small SVG overlays
for type, so text stays crisp and selectable-looking at any width.

Run:  python3 sumi.py   ->  writes out/
"""
import os

# Vendored next to this script so the build does not depend on a path
# outside the repo.
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "source.png")

INK = "#0a0a0a"      # background
PAPER = "#e8e2d6"    # primary type, the warm bone of the sky
MIST = "#b9b1a3"     # secondary type
STONE = "#8a8378"    # tertiary type
SLATE = "#2a2724"    # rules, ghost numerals
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def load():
    from PIL import Image
    im = Image.open(SRC).convert("RGB")
    # Portrait file, landscape painting. +90 puts the bright sky up and
    # the ink storm below; -90 flips it and reads upside down.
    return im.rotate(90, expand=True)


def banner(art):
    """Wide hero crop with a dark gradient so overlaid type stays legible."""
    from PIL import Image, ImageEnhance
    W, H = 1600, 680
    a = art.copy()
    # Crop the dramatic third: ink storm left, open paper right.
    aw, ah = a.size
    box = (0, int(ah * 0.06), int(aw * 0.84), int(ah * 0.92))
    a = a.crop(box).resize((W, H), Image.LANCZOS)
    a = ImageEnhance.Contrast(a).enhance(1.12)

    # Scrim over the lower band, where the title sits. Built as a single
    # row and resized, which is far cheaper than a per-pixel loop.
    col = Image.new("L", (1, H))
    cp = col.load()
    for y in range(H):
        f = max(0.0, (y - H * 0.78) / (H * 0.22))
        cp[0, y] = int((f ** 1.5) * 150)
    scrim = col.resize((W, H))
    black = Image.new("RGB", (W, H), (7, 7, 7))
    return Image.composite(black, a, scrim)


def strip(art, h=150):
    """Thin ink band used as a section divider."""
    from PIL import Image
    W = 1600
    aw, ah = art.size
    a = art.crop((0, int(ah * 0.42), aw, int(ah * 0.60)))
    return a.resize((W, h), Image.LANCZOS)


def side(art, w=560, h=620):
    """Tall crop for the About section, framed beside the text."""
    from PIL import Image
    aw, ah = art.size
    # The region holding the rider and the ribbon.
    a = art.crop((int(aw * 0.30), int(ah * 0.05), int(aw * 0.72), ah))
    return a.resize((w, h), Image.LANCZOS)


# ---- SVG type overlays ------------------------------------------------

def txt(x, y, s, size=13, fill=PAPER, weight="400", ls=0, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" letter-spacing="{ls}" '
            f'text-anchor="{anchor}">{s}</text>')


def rule_svg(label, n):
    """Section header: index, kanji, label, hairline. Ink on black."""
    W, H = 1200, 92
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="{label}">',
         f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    s.append(txt(60, 60, n, 34, SLATE, "700"))
    s.append(f'<rect x="120" y="34" width="3" height="26" fill="{STONE}"/>')
    s.append(txt(142, 56, label, 19, PAPER, "700", 5))
    s.append(f'<rect x="60" y="78" width="{W-120}" height="1" fill="{SLATE}"/>')
    # A pale wash travelling the rule, like ink bleeding along paper.
    # Grey, not red: the ribbon belongs to the painting alone.
    s.append(f'<rect x="60" y="77" width="150" height="2" fill="{MIST}" opacity="0.5">'
             f'<animate attributeName="x" values="60;{W-210};60" dur="15s" '
             f'repeatCount="indefinite"/></rect>')
    s.append('</svg>')
    return "\n".join(s)


def title_svg():
    """Name block, burned into the banner.

    GitHub Markdown cannot layer an SVG over a PNG — no CSS, no
    positioning. So the type is composited into the image itself rather
    than shipped as a separate overlay that would just stack below it.
    """
    W, H = 1600, 150
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Aditya Singh — Telecom DevOps Engineer">',
         f'<rect width="{W}" height="{H}" fill="none"/>']
    # No kanji here: this block is rasterised, and the container has no
    # CJK font, so the glyph renders as a tofu box. Kanji lives only in
    # the README's Markdown text, where the browser resolves the font.
    s.append(f'<rect x="70" y="26" width="38" height="4" fill="{STONE}"/>')
    s.append(txt(70, 84, "ADITYA SINGH", 46, PAPER, "700", 3))
    s.append(txt(74, 112, "TELECOM DEVOPS &#183; SIP &#183; SOFTSWITCHES",
                 15, MIST, "700", 4))
    s.append(txt(74, 136, "I keep 82 production servers from going dark.",
                 13, STONE, "400", 0))
    s.append('</svg>')
    return "\n".join(s)


def compose_banner(art):
    """Render the title SVG and paste it into the banner's scrim band."""
    import io
    import cairosvg
    from PIL import Image
    base = banner(art).convert("RGBA")
    png = cairosvg.svg2png(bytestring=title_svg().encode(),
                           output_width=base.width)
    over = Image.open(io.BytesIO(png)).convert("RGBA")
    # Sit the block in the scrimmed lower band.
    # Paint a solid ink band first. The scrim alone is not enough: the
    # lower-left of this crop is bright paper, and pale type on it was
    # unreadable. A band guarantees contrast wherever the crop lands.
    from PIL import ImageDraw
    band_h = over.height + 6
    d = ImageDraw.Draw(base, "RGBA")
    d.rectangle([0, base.height - band_h, base.width, base.height],
                fill=(8, 8, 8, 244))
    base.alpha_composite(over, (0, base.height - over.height - 3))
    return base.convert("RGB")


def save(im, path):
    """Quantise to a 192-colour palette.

    The artwork is almost monochrome, so a palette costs nothing visually
    and takes the three images from ~2.1MB to a size that is reasonable to
    ship in a README.
    """
    from PIL import Image
    im.convert("RGB").quantize(colors=192, method=Image.MEDIANCUT).save(
        path, optimize=True)


os.makedirs("out", exist_ok=True)
art = load()
save(compose_banner(art), "out/sumi-banner.png")
save(strip(art), "out/sumi-strip.png")
save(side(art), "out/sumi-side.png")
for i, (k, label) in enumerate([
        ("arsenal", "THE ARSENAL"),
        ("built", "WHAT I BUILT"),
        ("proof", "THE PROOF"),
        ("way", "THE WAY")]):
    open(f"out/sumi-rule-{k}.svg", "w").write(rule_svg(label, f"0{i+1}"))
print("sumi ok")
