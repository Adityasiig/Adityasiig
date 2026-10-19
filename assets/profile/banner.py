"""Dithered banner for the profile header.

The reference profile uses a halftone/stipple engraving as its banner.
This draws the same idea from the work itself rather than borrowing an
image: a SIP call flowing left to right, rendered as 1-bit stipple.

Pure black and white, no greys — the dithering carries the tone, which
is what gives it the engraved look at any zoom level.

Run:  python3 banner.py   ->  writes out/banner.png
"""
import math
import os
import random

W, H = 1600, 380
SS = 2                      # supersample, then threshold-dither down

random.seed(7)              # deterministic: the banner must not change
                            # on every regeneration


def field(x, y):
    """Greyscale source, 0 (black) .. 1 (white), in final-image coords."""
    v = 0.0

    # Horizontal signal path with a soft falloff around it.
    path_y = H * 0.5 + math.sin(x / 150.0) * 26
    d = abs(y - path_y)
    v += math.exp(-(d * d) / 260.0) * 0.72

    # Packet pulses travelling the path: brighter blooms at intervals.
    for px in range(120, W, 190):
        dx, dy = x - px, y - path_y
        r = math.sqrt(dx * dx + dy * dy)
        v += math.exp(-(r * r) / 700.0) * 0.8

    # Waveform envelope above and below, so the band reads as audio.
    env = (math.sin(x / 38.0) + math.sin(x / 97.0 + 1.1)) * 0.5
    band = abs(y - path_y) - 40 - env * 30
    if -7 < band < 7:
        v += (1 - abs(band) / 7.0) * 0.5

    # Vignette: fade the far edges so it sits on black cleanly.
    edge = min(x, W - x) / 260.0
    v *= min(1.0, edge)
    v *= min(1.0, min(y, H - y) / 90.0)

    return max(0.0, min(0.82, v))


def build():
    from PIL import Image
    big = Image.new("L", (W * SS // 2, H * SS // 2), 0)
    px = big.load()
    bw, bh = big.size
    for yy in range(bh):
        for xx in range(bw):
            v = field(xx * 2.0 / SS, yy * 2.0 / SS)
            px[xx, yy] = int(v * 255)

    # Stipple: ordered-ish threshold with jitter. Plain Floyd-Steinberg
    # looks like a photo; jittered thresholding looks engraved, which is
    # the reference's texture.
    out = Image.new("1", big.size)
    o = out.load()
    for yy in range(bh):
        for xx in range(bw):
            t = (((xx * 7 + yy * 13) % 17) / 17.0) * 0.75 + random.random() * 0.25
            o[xx, yy] = 1 if px[xx, yy] / 255.0 > t else 0

    out = out.convert("L").resize((W, H), Image.LANCZOS)
    # Re-threshold after downscale to keep it 1-bit crisp rather than grey.
    out = out.point(lambda p: 255 if p > 118 else 0).convert("1")
    return out


os.makedirs("out", exist_ok=True)
build().save("out/banner.png", optimize=True)
print("banner ok")
