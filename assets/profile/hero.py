"""Animated hero: a live SIP/telecom console.

Dense on purpose. SMIL animation survives GitHub's camo proxy intact
(verified), so the panel actually moves: a scan sweep, SIP messages
travelling the signalling path, live-looking meters, blinking status.
"""
W, H = 1200, 420
RED, WHITE, GREY, GREY2, LINE = "#d71921", "#ffffff", "#8f8f8f", "#5c5c5c", "#242424"
PANEL, PANEL2 = "#0c0c0c", "#141414"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
s = []
A = s.append

A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
  f'role="img" aria-label="Aditya Singh — Security Engineer and Telecom DevOps Engineer. '
  f'Animated SIP signalling console.">')
A('<defs>')
A(f'<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">'
  f'<path d="M24 0H0V24" fill="none" stroke="{WHITE}" stroke-opacity="0.04"/></pattern>')
A(f'<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">'
  f'<stop offset="0" stop-color="{RED}" stop-opacity="0"/>'
  f'<stop offset="0.5" stop-color="{RED}" stop-opacity="0.5"/>'
  f'<stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>')
A('<clipPath id="clip"><rect x="1" y="1" width="%d" height="%d" rx="16"/></clipPath>' % (W-2, H-2))
A('</defs>')

A(f'<rect width="{W}" height="{H}" fill="#000000"/>')
A(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="{PANEL}" stroke="{LINE}"/>')
A('<g clip-path="url(#clip)">')
A(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')

# scanning sweep across the whole panel
A(f'<rect x="-300" y="0" width="300" height="{H}" fill="url(#sweep)">'
  f'<animate attributeName="x" values="-300;{W}" dur="6s" repeatCount="indefinite"/></rect>')

# ── title bar ────────────────────────────────────────────────────────
A(f'<rect x="1" y="1" width="{W-2}" height="40" fill="{PANEL2}"/>')
A(f'<line x1="1" y1="41" x2="{W-1}" y2="41" stroke="{LINE}"/>')
for i, c in enumerate([RED, "#3a3a3a", "#3a3a3a"]):
    A(f'<circle cx="{26+i*18}" cy="21" r="5" fill="{c}"/>')
A(f'<text x="96" y="26" font-family="{MONO}" font-size="12" fill="{GREY2}" '
  f'letter-spacing="1.5">adityasiig@core-01 — opensips · freeswitch · 82 nodes</text>')
# live clock-ish blinking cursor
A(f'<rect x="{W-150}" y="14" width="8" height="14" fill="{RED}">'
  f'<animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/></rect>')
A(f'<text x="{W-132}" y="26" font-family="{MONO}" font-size="12" fill="{GREY2}">LIVE</text>')

# ── name, typed in ───────────────────────────────────────────────────
NAME = "ADITYA SINGH"
A(f'<text x="40" y="112" font-family="{MONO}" font-size="54" font-weight="700" '
  f'fill="{WHITE}" letter-spacing="-1">')
for i, ch in enumerate(NAME):
    d = 0.10 * i
    # Starts fully visible. The animation dips it and brings it back,
    # so the type-on reads as motion without the name ever depending
    # on animation to exist: with SMIL disabled this is just the name.
    A(f'<tspan>{ch if ch != " " else "&#160;"}'
      f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;0.99;1" '
      f'dur="{d + 0.05:.2f}s" fill="freeze"/></tspan>')
A('</text>')
A(f'<rect x="40" y="126" width="330" height="3" fill="{RED}">'
  f'<animate attributeName="width" values="0;0;330" keyTimes="0;0.65;1" '
  f'dur="2.0s" fill="freeze"/></rect>')
A(f'<text x="40" y="156" font-family="{MONO}" font-size="14" fill="{GREY}" letter-spacing="2">'
  f'SECURITY ENGINEER &#183; TELECOM DEVOPS ENGINEER'
  f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;0.8;1" '
  f'dur="2.2s" fill="freeze"/></text>')

# ── SIP ladder: signalling actually travelling ───────────────────────
LX, LY = 40, 206
NODES = [("UAC", 0), ("OpenSIPS", 190), ("FreeSWITCH", 380), ("CARRIER", 570)]
for label, dx in NODES:
    A(f'<rect x="{LX+dx}" y="{LY}" width="118" height="26" rx="4" fill="#000" stroke="{LINE}"/>')
    A(f'<text x="{LX+dx+59}" y="{LY+17}" text-anchor="middle" font-family="{MONO}" '
      f'font-size="10" fill="{GREY}" letter-spacing="1">{label}</text>')
    if dx:
        A(f'<line x1="{LX+dx-72}" y1="{LY+13}" x2="{LX+dx}" y2="{LY+13}" stroke="{LINE}"/>')

MSGS = [("INVITE", 0.0), ("100", 0.6), ("183", 1.2), ("200 OK", 1.8), ("ACK", 2.4)]
for i, (m, t) in enumerate(MSGS):
    # Loops forever, so a static render catching mid-flight is correct;
    # the first message is visible at rest so the ladder never reads empty.
    A(f'<g opacity="{1 if i == 0 else 0}">'
      f'<animate attributeName="opacity" values="0;1;1;0" dur="3.2s" '
      f'begin="{t}s" repeatCount="indefinite"/>'
      # x is set up front: without it the label renders at 0 and is
      # clipped off the left edge in any static render.
      f'<text x="{LX+10}" y="{LY-8}" font-family="{MONO}" font-size="10" '
      f'fill="{RED if m=="200 OK" else WHITE}">'
      f'<animate attributeName="x" values="{LX+10};{LX+600}" dur="3.2s" '
      f'begin="{t}s" repeatCount="indefinite"/>{m}</text></g>')

# ── throughput meter ─────────────────────────────────────────────────
MX, MY = 740, 196
A(f'<rect x="{MX}" y="{MY}" width="420" height="92" rx="8" fill="#000" stroke="{LINE}"/>')
A(f'<text x="{MX+14}" y="{MY+20}" font-family="{MONO}" font-size="10" fill="{GREY2}" '
  f'letter-spacing="2">CDR THROUGHPUT &#183; 24H</text>')
import math
for i in range(38):
    base = 14 + abs(math.sin(i * 0.55)) * 44
    peak = base * 1.35
    col = RED if i % 11 == 5 else "#3a3a3a"
    A(f'<rect x="{MX+14+i*10.6:.1f}" y="{MY+78-base:.1f}" width="6" height="{base:.1f}" rx="1" fill="{col}">'
      f'<animate attributeName="height" values="{base:.0f};{peak:.0f};{base:.0f}" '
      f'dur="{2.4+(i%7)*0.3:.1f}s" repeatCount="indefinite"/>'
      f'<animate attributeName="y" values="{MY+78-base:.0f};{MY+78-peak:.0f};{MY+78-base:.0f}" '
      f'dur="{2.4+(i%7)*0.3:.1f}s" repeatCount="indefinite"/></rect>')

# ── stat strip ───────────────────────────────────────────────────────
SY = 318
STATS = [("82+", "SERVER FLEET"), ("SIP/RTP", "SIGNALLING"),
         ("ClickHouse", "CDR ANALYTICS"), ("OWASP", "SECURITY TESTING")]
x = 40
for big, small in STATS:
    A(f'<rect x="{x}" y="{SY}" width="268" height="62" rx="8" fill="#000" stroke="{LINE}"/>')
    A(f'<rect x="{x}" y="{SY}" width="3" height="62" rx="1.5" fill="{RED}"/>')
    A(f'<text x="{x+18}" y="{SY+28}" font-family="{MONO}" font-size="18" fill="{WHITE}">{big}</text>')
    A(f'<text x="{x+18}" y="{SY+47}" font-family="{MONO}" font-size="9" fill="{GREY2}" '
      f'letter-spacing="2">{small}</text>')
    x += 280

A('</g>')
A('</svg>')
open('hero.svg', 'w').write("\n".join(s))
print("hero ok", len("\n".join(s)) // 1024, "KB")
