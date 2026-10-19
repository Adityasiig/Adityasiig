"""The body panels: NOW, WORK, STACK, LAB.

Everything here follows the same two rules the hero does, and both are
load-bearing rather than stylistic:

  * Nothing may depend on animation to be legible. GitHub's camo proxy
    preserves SMIL, but Markdown previews, RSS readers and reduced-motion
    settings do not run it. So anything animated is drawn at its FINAL
    state and the animation only dips away and returns. Never opacity="0".
  * Every coordinate is set up front. An animated x with no initial value
    renders at 0 and clips off the left edge.

Run:  python3 body.py   ->  writes out/panel-*.svg
"""
import math
import os

W = 1200
RED, WHITE, GREY, GREY2, LINE = "#d71921", "#ffffff", "#8f8f8f", "#5c5c5c", "#242424"
DIM, CARD = "#141414", "#0b0b0b"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def head(h, label):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
        f'viewBox="0 0 {W} {h}" role="img" aria-label="{label}">',
        f'<rect width="{W}" height="{h}" fill="#000000"/>',
    ]


def card(x, y, w, h, fill=CARD, stroke=LINE):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>')


def txt(x, y, s, size=13, fill=WHITE, weight="400", ls=0, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" letter-spacing="{ls}" '
            f'text-anchor="{anchor}">{s}</text>')


def reveal(delay):
    """Hide-then-reveal. Final state is visible, so a frozen frame is correct."""
    return (f'<animate attributeName="opacity" values="0;0;1" '
            f'keyTimes="0;0.92;1" dur="{delay:.2f}s" fill="freeze"/>')


# ---------------------------------------------------------------- NOW

def panel_now():
    """Live operations board: fleet grid, running counters, status lamps."""
    H = 318
    s = head(H, "Now — live operations")

    s.append(card(0, 0, W, H, "#070707"))
    s.append(f'<rect x="0" y="0" width="3" height="{H}" fill="{RED}"/>')
    s.append(txt(24, 34, "NOW", 15, WHITE, "700", 5))
    s.append(txt(80, 34, "// live", 12, GREY2))

    # Blinking status lamp, right-aligned. The label is anchored at the
    # end rather than positioned by estimated width: letter-spacing is
    # not in any width guess I can make here, and at 2px over 11 glyphs
    # it was enough to push the text off the panel.
    s.append(txt(W - 28, 34, "OPERATIONAL", 11, GREY, "700", 2, anchor="end"))
    s.append(f'<circle cx="{W-152}" cy="29.5" r="4" fill="{RED}">'
             f'<animate attributeName="opacity" values="1;0.25;1" dur="1.6s" '
             f'repeatCount="indefinite"/></circle>')

    # ---- fleet grid: 82 nodes, each breathing on its own cycle
    gx, gy = 24, 62
    s.append(txt(gx, gy, "FLEET", 11, GREY2, "700", 3))
    s.append(txt(gx + 70, gy, "82 production servers", 11, GREY))
    # 28 wide, so 82 nodes fill three full-ish rows under the label
    # instead of two thin ones with a dead band beneath them.
    cols, cell = 28, 13
    for i in range(82):
        cx = gx + (i % cols) * cell
        cy = gy + 14 + (i // cols) * cell
        # a few amber-ish nodes so it reads as a real fleet, not a logo
        col = RED if i % 17 == 5 else "#1f1f1f"
        s.append(f'<rect x="{cx}" y="{cy}" width="8" height="8" rx="1" fill="{col}">'
                 f'<animate attributeName="opacity" values="1;0.35;1" '
                 f'dur="{2.0 + (i % 11) * 0.31:.2f}s" '
                 f'begin="{(i % 7) * 0.2:.1f}s" repeatCount="indefinite"/></rect>')

    # ---- counters
    ROWS = [
        ("ROLE", "Telecom DevOps Engineer", "Crown IT Solution"),
        ("SIGNAL", "SIP routing · softswitch deploys", "OpenSIPS · FreeSWITCH"),
        ("DATA", "CDR ingestion · margin analytics", "ClickHouse · DuckDB"),
        ("SECURE", "authorized web / API / VoIP testing", "OWASP · Burp · Nmap"),
    ]
    ry = 142
    for i, (k, v, tail) in enumerate(ROWS):
        y = ry + i * 30
        s.append(f'<g>{reveal(0.5 + i * 0.18)}')
        s.append(f'<rect x="24" y="{y - 13}" width="2" height="16" fill="{RED}"/>')
        s.append(txt(38, y, k, 11, GREY2, "700", 2))
        s.append(txt(120, y, v, 13, WHITE))
        s.append(txt(W - 28, y, tail, 11, GREY, anchor="end"))
        s.append('</g>')

    # ---- throughput sparkline along the bottom
    sy, sh = 268, 34
    s.append(txt(24, sy - 6, "CALL VOLUME · 24H", 10, GREY2, "700", 2))
    n = 110
    bw = (W - 48) / n
    for i in range(n):
        v = (math.sin(i * 0.17) + math.sin(i * 0.41 + 1.3)) * 0.5
        h = 3 + (v + 1) * 0.5 * (sh - 4)
        col = RED if v > 0.72 else "#242424"
        s.append(f'<rect x="{24 + i * bw:.1f}" y="{sy + sh - h:.1f}" '
                 f'width="{bw * 0.6:.1f}" height="{h:.1f}" fill="{col}">'
                 f'<animate attributeName="height" '
                 f'values="{h:.0f};{min(h * 1.5, sh):.0f};{h:.0f}" '
                 f'dur="{2.2 + (i % 8) * 0.3:.1f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y" '
                 f'values="{sy + sh - h:.0f};{sy + sh - min(h * 1.5, sh):.0f};{sy + sh - h:.0f}" '
                 f'dur="{2.2 + (i % 8) * 0.3:.1f}s" repeatCount="indefinite"/></rect>')

    s.append('</svg>')
    return "\n".join(s)


# ---------------------------------------------------------------- WORK

PROJECTS = [
    ("MyCDR / CDR DIRECT", "CDR ingestion and analytics for NPANXX traffic,",
     "trunks, quality, revenue, cost and margin.",
     ["Python", "Flask", "DuckDB", "Docker"], "INGEST", 0.86),
    ("EASEDIAL PORTAL", "Carrier portal with tenant-scoped access, KPIs,",
     "CDR diagnostics, rates, invoices and exports.",
     ["TypeScript", "Next.js", "REST"], "LIVE", 0.93),
    ("ROUTEFORGE LCR2", "Rate-deck tooling for NPANXX pricing and",
     "second-lowest-cost routing.",
     ["TypeScript", "NPANXX", "LCR"], "ROUTING", 0.74),
    ("HEALTH TRACKER", "Nutrition, hydration and body metrics with",
     "analytics and AI-assisted coaching.",
     ["Next.js", "TypeScript", "Supabase"], "LIVE", 0.81),
]


def panel_work():
    """Four project cards as instrument panels, each with its own meter."""
    CW, CH = 582, 176
    H = 60 + CH * 2 + 16
    s = head(H, "Selected work")

    s.append(f'<rect x="0" y="0" width="3" height="{H}" fill="{RED}"/>')
    s.append(txt(24, 34, "SELECTED WORK", 15, WHITE, "700", 5))
    s.append(f'<rect x="230" y="28" width="{W-258}" height="1" fill="{LINE}"/>')

    for i, (name, l1, l2, tags, badge, fill) in enumerate(PROJECTS):
        x = 24 + (i % 2) * (CW + 12)
        y = 60 + (i // 2) * (CH + 16)
        s.append(f'<g>{reveal(0.4 + i * 0.2)}')
        s.append(card(x, y, CW, CH))
        # red spine + badge
        s.append(f'<rect x="{x}" y="{y}" width="3" height="{CH}" fill="{RED}"/>')
        s.append(txt(x + 22, y + 34, name, 15, WHITE, "700", 1))

        bw_ = len(badge) * 7 + 16
        s.append(f'<rect x="{x+CW-bw_-18}" y="{y+18}" width="{bw_}" height="19" '
                 f'rx="2" fill="#1a0507" stroke="{RED}" stroke-width="1"/>')
        s.append(txt(x + CW - bw_ / 2 - 18, y + 32, badge, 10, RED, "700", 1,
                     anchor="middle"))

        s.append(txt(x + 22, y + 62, l1, 12.5, GREY))
        s.append(txt(x + 22, y + 80, l2, 12.5, GREY))

        # meter — fills on load, stays full
        my = y + 104
        s.append(f'<rect x="{x+22}" y="{my}" width="{CW-44}" height="4" rx="2" fill="#1a1a1a"/>')
        s.append(f'<rect x="{x+22}" y="{my}" width="{(CW-44)*fill:.0f}" height="4" rx="2" fill="{RED}">'
                 f'<animate attributeName="width" values="0;{(CW-44)*fill:.0f}" '
                 f'dur="1.6s" begin="{0.3+i*0.2:.1f}s" fill="freeze"/></rect>')

        # tag chips
        tx = x + 22
        for t in tags:
            cw_ = len(t) * 7 + 16
            s.append(f'<rect x="{tx}" y="{y+124}" width="{cw_}" height="22" rx="2" '
                     f'fill="{DIM}" stroke="#262626" stroke-width="1"/>')
            s.append(txt(tx + cw_ / 2, y + 139, t, 11, GREY, anchor="middle"))
            tx += cw_ + 7
        s.append('</g>')

    s.append('</svg>')
    return "\n".join(s)


# ---------------------------------------------------------------- STACK

STACK = [
    ("TELECOM", ["OpenSIPS", "FreeSWITCH", "VOS3000", "SIP", "RTP", "LCR", "CDR"], 0.95),
    ("INFRA", ["Linux", "Docker", "Coolify", "Caddy", "Cloudflare"], 0.88),
    ("BACKEND", ["Python", "FastAPI", "Flask", "PostgreSQL", "ClickHouse", "DuckDB"], 0.9),
    ("FRONTEND", ["TypeScript", "Next.js", "React"], 0.72),
    ("OBSERVE", ["Grafana", "ClickHouse", "fleet probes", "health checks"], 0.8),
    ("SECURITY", ["Nmap", "Burp Suite", "Ghidra", "gdb", "API / VoIP"], 0.78),
]


def panel_stack():
    """Each row is a channel on a mixing desk: label, chips, level."""
    RH = 44
    H = 60 + RH * len(STACK) + 10
    s = head(H, "Stack")

    s.append(f'<rect x="0" y="0" width="3" height="{H}" fill="{RED}"/>')
    s.append(txt(24, 34, "STACK", 15, WHITE, "700", 5))
    s.append(f'<rect x="120" y="28" width="{W-148}" height="1" fill="{LINE}"/>')

    for i, (cat, items, lvl) in enumerate(STACK):
        y = 60 + i * RH
        s.append(f'<g>{reveal(0.35 + i * 0.12)}')
        s.append(f'<rect x="24" y="{y}" width="{W-48}" height="{RH-6}" rx="2" '
                 f'fill="{"#0a0a0a" if i % 2 == 0 else "#060606"}"/>')
        s.append(f'<rect x="24" y="{y}" width="2" height="{RH-6}" fill="{RED}"/>')
        s.append(txt(40, y + 24, cat, 11, RED, "700", 2))

        tx = 140
        for t in items:
            cw_ = len(t) * 7 + 16
            s.append(f'<rect x="{tx}" y="{y+7}" width="{cw_}" height="23" rx="2" '
                     f'fill="{DIM}" stroke="#262626" stroke-width="1"/>')
            s.append(txt(tx + cw_ / 2, y + 23, t, 11.5, "#c9c9c9", anchor="middle"))
            tx += cw_ + 7

        # level meter on the right — 12 segments, lit to lvl
        mx = W - 24 - 12 * 11
        lit = round(lvl * 12)
        for k in range(12):
            on = k < lit
            s.append(f'<rect x="{mx+k*11}" y="{y+12}" width="7" height="14" '
                     f'fill="{RED if on else "#1c1c1c"}">'
                     + (f'<animate attributeName="opacity" values="1;0.3;1" '
                        f'dur="{1.4+(k%4)*0.3:.1f}s" begin="{k*0.08:.2f}s" '
                        f'repeatCount="indefinite"/>' if on and k >= lit - 3 else '')
                     + '</rect>')
        s.append('</g>')

    s.append('</svg>')
    return "\n".join(s)


# ---------------------------------------------------------------- LAB

def panel_lab():
    """The Glyph Matrix story, told on an actual simulated 13x13 panel."""
    H = 316
    s = head(H, "Lab")

    s.append(f'<rect x="0" y="0" width="3" height="{H}" fill="{RED}"/>')
    s.append(txt(24, 34, "LAB", 15, WHITE, "700", 5))
    s.append(txt(80, 34, "// things built to find out whether they would work",
                 12, GREY2))
    s.append(f'<rect x="520" y="28" width="{W-548}" height="1" fill="{LINE}"/>')

    # --- live 13x13 matrix, left. Diamond fronts expanding, which is
    #     literally what the Bloom toy draws on the phone.
    mx, my, cell = 32, 62, 15
    s.append(f'<rect x="{mx-10}" y="{my-10}" width="{13*cell+20}" '
             f'height="{13*cell+20}" rx="4" fill="#0a0a0a" stroke="{LINE}"/>')
    for r in range(13):
        for c in range(13):
            d = abs(r - 6) + abs(c - 6)          # L1 distance == diamond radius
            x = mx + c * cell
            y = my + r * cell
            # at rest: the mid-radius ring is lit, so a frozen frame still
            # reads as a glyph panel rather than an empty grid
            # Only the ring is lit. Two rings at once read as mud at this
            # scale, which is the same lesson the toys themselves taught:
            # a 13x13 panel has no room for a second brightness telling
            # a second story.
            rest = RED if d == 4 else "#141414"
            s.append(f'<rect x="{x}" y="{y}" width="{cell-4}" height="{cell-4}" rx="1" '
                     f'fill="{rest}">'
                     f'<animate attributeName="fill" '
                     f'values="#1a1a1a;{RED};#1a1a1a;#1a1a1a" '
                     f'keyTimes="0;0.12;0.3;1" dur="2.6s" '
                     f'begin="{d*0.14:.2f}s" repeatCount="indefinite"/></rect>')
    s.append(txt(mx - 10, my + 13 * cell + 28, "13 × 13 · 169 px · 5 levels",
                 11, GREY2, "700", 1))

    # --- the geometry story, right
    tx0 = 280
    s.append(f'<g>{reveal(0.5)}')
    s.append(txt(tx0, 82, "GLYPH TOYS", 14, WHITE, "700", 2))
    s.append(txt(tx0 + 130, 82, "Nothing Phone (4a) Pro · 12 toys", 11, GREY2))
    for i, line in enumerate([
        "A circle of radius r on a 13×13 grid lands on 8, 12, 16, 32, 28, 40",
        "pixels. Not even monotonic — so rings cannot be evenly spaced and a",
        "rotating arm staircases. A diamond is exactly 4r at every radius,",
        "which makes it the honest substitute. Every design is built from",
        "what the grid renders exactly: rows, columns, blocks, symmetry.",
    ]):
        s.append(txt(tx0, 108 + i * 19, line, 12.5, GREY))
    s.append('</g>')

    # the measured numbers as a tiny bar chart — the actual punchline
    cx0, cy0 = tx0, 224
    s.append(txt(cx0, cy0 - 8, "PIXELS ON A CIRCLE OF RADIUS r", 10, GREY2, "700", 2))
    for i, v in enumerate([8, 12, 16, 32, 28, 40]):
        bh = v * 1.15
        x = cx0 + i * 46
        s.append(f'<rect x="{x}" y="{cy0 + 46 - bh:.0f}" width="26" height="{bh:.0f}" '
                 f'fill="{RED if v in (32, 28) else "#2a2a2a"}">'
                 f'<animate attributeName="height" values="0;{bh:.0f}" dur="0.9s" '
                 f'begin="{0.6+i*0.1:.1f}s" fill="freeze"/>'
                 f'<animate attributeName="y" values="{cy0+46:.0f};{cy0+46-bh:.0f}" '
                 f'dur="0.9s" begin="{0.6+i*0.1:.1f}s" fill="freeze"/></rect>')
        s.append(txt(x + 13, cy0 + 60, str(v), 10, GREY, anchor="middle"))
    s.append(txt(cx0 + 290, cy0 + 24, "↑ 32 then 28. that is the whole problem.",
                 11, RED))

    # other lab entries
    ox = 760
    for i, (t, d) in enumerate([
        ("ZERO TRUST NETWORK ACCESS", "post-quantum crypto · live trust scoring"),
        ("WEBVULNSCANNER", "recon · WAF detection · HTML reporting"),
        ("GOTHAM / TERMINAL", "two portfolios, opposite directions"),
    ]):
        y = 96 + i * 46
        s.append(f'<g>{reveal(0.7 + i * 0.15)}')
        s.append(f'<rect x="{ox}" y="{y-16}" width="{W-ox-24}" height="36" rx="2" '
                 f'fill="#0a0a0a" stroke="{LINE}"/>')
        s.append(f'<rect x="{ox}" y="{y-16}" width="2" height="36" fill="{RED}"/>')
        s.append(txt(ox + 14, y - 1, t, 11.5, WHITE, "700", 1))
        s.append(txt(ox + 14, y + 14, d, 10.5, GREY2))
        s.append('</g>')

    s.append('</svg>')
    return "\n".join(s)


os.makedirs('out', exist_ok=True)
for name, fn in [("now", panel_now), ("work", panel_work),
                 ("stack", panel_stack), ("lab", panel_lab)]:
    open(f'out/panel-{name}.svg', 'w').write(fn())
print("body ok")
