"""Section rules and a signal strip, matching the hero."""
RED, WHITE, GREY, GREY2, LINE = "#d71921", "#ffffff", "#8f8f8f", "#5c5c5c", "#242424"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

def rule(label, idx):
    W, H = 1200, 52
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}" role="img" aria-label="{label}">']
    s.append(f'<rect width="{W}" height="{H}" fill="#000000"/>')
    s.append(f'<rect x="0" y="18" width="4" height="18" fill="{RED}"/>')
    s.append(f'<text x="18" y="33" font-family="{MONO}" font-size="15" font-weight="700" '
             f'fill="{WHITE}" letter-spacing="4">{label}</text>')
    lx = 30 + len(label)*13
    # The rule draws itself in, then stays. Full width at rest so it is
    # never missing when animation is off.
    s.append(f'<rect x="{lx}" y="26" width="{W-lx-30}" height="1" fill="{LINE}">'
             f'<animate attributeName="width" values="0;0;{W-lx-30}" keyTimes="0;0.2;1" '
             f'dur="1.4s" fill="freeze"/></rect>')
    # travelling pip along the rule
    s.append(f'<circle cy="26.5" r="3" fill="{RED}" cx="{W-28}">'
             f'<animate attributeName="cx" values="{lx};{W-28}" dur="4s" '
             f'begin="{idx*0.3}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0;1;1;0" dur="4s" '
             f'begin="{idx*0.3}s" repeatCount="indefinite"/></circle>')
    s.append(f'<circle cx="{W-14}" cy="26.5" r="3.5" fill="{RED}"/>')
    s.append('</svg>')
    return "\n".join(s)

def strip():
    """A live signal bar: reads as traffic, sits under the links."""
    W, H = 1200, 46
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
       f'viewBox="0 0 {W} {H}" role="img" aria-label="Live traffic">']
    s.append(f'<rect width="{W}" height="{H}" fill="#000000"/>')
    import math
    n=96; bw=(W-40)/n
    for i in range(n):
        h=5+abs(math.sin(i*0.33))*22
        col = RED if i%16==7 else "#2a2a2a"
        s.append(f'<rect x="{20+i*bw:.1f}" y="{(H-h)/2:.1f}" width="{bw*0.55:.1f}" '
                 f'height="{h:.1f}" rx="1" fill="{col}">'
                 f'<animate attributeName="height" values="{h:.0f};{h*1.6:.0f};{h:.0f}" '
                 f'dur="{1.8+(i%9)*0.22:.1f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y" values="{(H-h)/2:.0f};{(H-h*1.6)/2:.0f};{(H-h)/2:.0f}" '
                 f'dur="{1.8+(i%9)*0.22:.1f}s" repeatCount="indefinite"/></rect>')
    s.append('</svg>')
    return "\n".join(s)

import os
os.makedirs('out',exist_ok=True)
for i,(k,l) in enumerate([('now','NOW'),('work','SELECTED WORK'),
                          ('stack','STACK'),('lab','LAB')]):
    open(f'out/rule-{k}.svg','w').write(rule(l,i))
open('out/strip.svg','w').write(strip())
print("parts ok")
