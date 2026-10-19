# Profile assets

`banner.png` — generated 1-bit stipple banner. Regenerate with:

```sh
python3 banner.py   # writes out/banner.png, then copy up a level
```

It draws a SIP call flowing left to right (signal path, packet blooms,
waveform envelope) and dithers it to pure black and white. The seed is
fixed, so regenerating produces the same image.

## Third-party widgets

The profile README uses external services for stats, badges and icons.
They are **not** pinned or vendored, so they can break without notice.
Each was verified live before use:

| Service | Used for | Status when added |
| --- | --- | --- |
| `img.shields.io` | badges | 200 |
| `skillicons.dev` | tech-stack icons | 200 |
| `github-readme-stats.vercel.app` | repo pin cards only | 200 |
| `komarev.com` | profile-view counter | 200 |

**Avoid these two** — both are over quota and return HTTP 402, which
renders as a broken image:

- `github-readme-activity-graph.vercel.app`
- `github-profile-trophy.vercel.app`

## No contribution stats

The stats card, streak card, top-languages card and contribution chart
were all removed on purpose. If you add them back, note that
`ghchart.rshah.org` is the working chart host — the activity-graph
service above is dead.

## Constraints

GitHub proxies every image through camo, which strips scripts, external
references and web fonts. Inline SVG assets must therefore be
self-contained, carry an opaque background (or they break on the light
theme), and never depend on animation to be legible — an element that
starts at `opacity="0"` is invisible wherever SMIL does not run.
