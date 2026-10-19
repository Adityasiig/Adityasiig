"""Dark egoist theme assets.

Loud typography, blood red on near-black, hard edges. The voice is
first-person and declarative — the design has to carry that or the words
just look like bragging on a default template.

Two rules carried over, both about correctness rather than taste:

  * Nothing depends on animation. Camo preserves SMIL, but Markdown
    previews and reduced-motion do not run it. Everything rests at its
    FINAL state; animation only dips away and returns. Never opacity="0"
    on content.
  * Coordinates set up front — an animated x with no initial value
    renders at 0 and clips off the left edge.
  * Never estimate text width (letter-spacing is not in any guess).
    Right-aligned text uses text-anchor="end".

Run:  python3 ego.py   ->  writes out/*.svg
"""
import os

W = 1200
BLOOD = "#c30010"
EMBER = "#ff2b1c"
BONE = "#f2f0ed"
ASH = "#8c8681"
SMOKE = "#4a4642"
EDGE = "#1a1715"
VOID = "#080706"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def txt(x, y, s, size=13, fill=BONE, weight="400", ls=0, anchor="start", op=None):
    o = f' opacity="{op}"' if op is not None else ""
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" letter-spacing="{ls}" '
            f'text-anchor="{anchor}"{o}>{s}</text>')


def head(h, label):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
            f'viewBox="0 0 {W} {h}" role="img" aria-label="{label}">',
            f'<rect width="{W}" height="{h}" fill="{VOID}"/>']


def banner():
    """The statement. Name huge, one claim under it, nothing decorative."""
    H = 340
    s = head(H, "Aditya Singh — I build the networks your calls run on")

    # Faint tally marks behind the type: 82 strokes, one per server.
    # Background texture, deliberately low contrast.
    for i in range(82):
        x = 60 + i * 13.3
        s.append(f'<rect x="{x:.1f}" y="40" width="2" height="26" fill="{EDGE}"/>')

    s.append(f'<rect x="60" y="96" width="74" height="4" fill="{BLOOD}">'
             f'<animate attributeName="width" values="0;74" dur="0.7s" fill="freeze"/>'
             f'</rect>')

    s.append(txt(60, 168, "ADITYA SINGH", 58, BONE, "700", 2))
    s.append(txt(60, 206, "I BUILD THE NETWORKS YOUR CALLS RUN ON.",
                 18, BLOOD, "700", 3))

    s.append(txt(60, 250, "Telecom DevOps. Softswitches, SIP, and the "
                          "analytics that prove it works.", 14, ASH))
    s.append(txt(60, 274, "82 production servers. They do not go down "
                          "because I do not let them.", 14, SMOKE))

    # Hard rule, full width at rest.
    s.append(f'<rect x="60" y="306" width="{W-120}" height="1" fill="{EDGE}"/>')
    s.append(f'<rect x="60" y="305" width="150" height="3" fill="{BLOOD}">'
             f'<animate attributeName="x" values="60;{W-210};60" dur="11s" '
             f'repeatCount="indefinite"/></rect>')

    s.append('</svg>')
    return "\n".join(s)


def rule(label, n):
    """Numbered section header. Big index, label, hard line."""
    H = 86
    s = head(H, label)
    s.append(txt(60, 56, n, 40, EDGE, "700", 0))
    s.append(f'<rect x="124" y="24" width="3" height="34" fill="{BLOOD}"/>')
    s.append(txt(144, 50, label, 20, BONE, "700", 4))
    s.append(f'<rect x="60" y="74" width="{W-120}" height="1" fill="{EDGE}"/>')
    s.append('</svg>')
    return "\n".join(s)


CREED = [
    ("I do not guess.", "Every claim here was measured before it was written."),
    ("I do not ship blind.", "If I have not run it, I do not say it works."),
    ("I do not hide failures.", "The broken parts get named, not buried."),
    ("I do not pad.", "Fewer moving parts beats a clever architecture."),
]


def creed():
    """Four lines of doctrine. The ego, stated plainly."""
    RH = 62
    H = 24 + RH * len(CREED)
    s = head(H, "How I work")
    for i, (claim, why) in enumerate(CREED):
        y = 24 + i * RH
        s.append(f'<rect x="60" y="{y}" width="{W-120}" height="{RH-10}" '
                 f'fill="{"#0c0a09" if i % 2 == 0 else VOID}"/>')
        s.append(f'<rect x="60" y="{y}" width="2" height="{RH-10}" fill="{BLOOD}"/>')
        s.append(txt(84, y + 24, claim, 17, BONE, "700", 0.5))
        s.append(txt(84, y + 44, why, 12.5, SMOKE))
        s.append(txt(W - 64, y + 32, f"0{i+1}", 22, EDGE, "700", 0, anchor="end"))
    s.append('</svg>')
    return "\n".join(s)


def closer():
    H = 150
    s = head(H, "Contact")
    s.append(f'<rect x="60" y="0" width="{W-120}" height="1" fill="{EDGE}"/>')
    s.append(txt(60, 58, "I AM NOT LOOKING FOR EASY WORK.", 24, BONE, "700", 2))
    s.append(txt(60, 90, "Bring me the routing nobody wants to touch.",
                 14, BLOOD, "700", 1))
    s.append(txt(60, 120, "adityaajaysingh0104@gmail.com", 13, ASH))
    s.append(f'<circle cx="{W-74}" cy="78" r="5" fill="{EMBER}">'
             f'<animate attributeName="opacity" values="1;0.15;1" dur="2.6s" '
             f'repeatCount="indefinite"/></circle>')
    s.append(txt(W - 90, 82, "OPEN", 12, ASH, "700", 2, anchor="end"))
    s.append('</svg>')
    return "\n".join(s)


os.makedirs("out", exist_ok=True)
open("out/ego-banner.svg", "w").write(banner())
open("out/ego-creed.svg", "w").write(creed())
open("out/ego-closer.svg", "w").write(closer())
for i, (k, l) in enumerate([("arsenal", "THE ARSENAL"), ("built", "WHAT I BUILT"),
                            ("proof", "THE PROOF"), ("creed", "HOW I WORK")]):
    open(f"out/ego-rule-{k}.svg", "w").write(rule(l, f"0{i+1}"))
print("ego ok")
