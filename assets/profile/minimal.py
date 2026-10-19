"""Minimal profile assets: one quiet header, one hairline divider.

The console version said everything at once — meters, grids, blinking
lamps. This says one thing: the name, what I do, and a single line.

Rules kept from the console build, because they are about correctness
rather than style:

  * Nothing depends on animation. Camo preserves SMIL, but Markdown
    previews and reduced-motion do not run it. Everything is drawn at
    its final state; animation only dips away and returns.
  * Coordinates set up front — an animated x with no initial value
    renders at 0 and clips off the left edge.

Run:  python3 minimal.py   ->  writes out/*.svg
"""
import os

W = 1200
INK, MUTE, FAINT, RULE = "#e8e8e8", "#8a8a8a", "#5a5a5a", "#1e1e1e"
ACCENT = "#d71921"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def txt(x, y, s, size=13, fill=INK, weight="400", ls=0, anchor="start", op=None):
    o = f' opacity="{op}"' if op is not None else ""
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" letter-spacing="{ls}" '
            f'text-anchor="{anchor}"{o}>{s}</text>')


def header():
    """Name, role, one accent mark. Nothing else."""
    H = 260
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Aditya Singh — Telecom DevOps and Security Engineer">',
         f'<rect width="{W}" height="{H}" fill="#000000"/>']

    # A single short accent rule above the name. It draws itself in, but
    # rests at full width so a still frame is the finished picture.
    s.append(f'<rect x="80" y="86" width="34" height="2" fill="{ACCENT}">'
             f'<animate attributeName="width" values="0;34" dur="0.8s" fill="freeze"/>'
             f'</rect>')

    s.append(txt(80, 140, "Aditya Singh", 40, INK, "500", -0.5))
    s.append(txt(80, 174, "Telecom DevOps &#183; Security Engineering",
                 15, MUTE, "400", 0.5))

    # One quiet line of substance, right where the eye lands next.
    s.append(txt(80, 212, "SIP routing, softswitches, and the analytics "
                          "that say whether any of it works.", 13.5, FAINT))

    # Slow breathing dot — the only motion on the page.
    s.append(f'<circle cx="{W-82}" cy="135" r="3.5" fill="{ACCENT}">'
             f'<animate attributeName="opacity" values="1;0.2;1" dur="3.4s" '
             f'repeatCount="indefinite"/></circle>')
    s.append(txt(W - 96, 139, "available", 12, FAINT, "400", 0.5, anchor="end"))

    s.append('</svg>')
    return "\n".join(s)


def divider():
    """A hairline. One accent tick that drifts across it, slowly."""
    H = 28
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" aria-label="">',
         f'<rect width="{W}" height="{H}" fill="#000000"/>',
         f'<rect x="80" y="14" width="{W-160}" height="1" fill="{RULE}"/>']
    s.append(f'<rect x="80" y="13" width="48" height="3" fill="{ACCENT}" opacity="0.85">'
             f'<animate attributeName="x" values="80;{W-128};80" dur="14s" '
             f'repeatCount="indefinite"/></rect>')
    s.append('</svg>')
    return "\n".join(s)


os.makedirs('out', exist_ok=True)
open('out/head.svg', 'w').write(header())
open('out/divider.svg', 'w').write(divider())
print("minimal ok")
