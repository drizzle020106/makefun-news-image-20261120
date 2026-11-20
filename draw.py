#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261120.

One image summing up the world's news of Friday 20 November 2026:
a dark-navy header naming the day, and a 2x3 grid of six stories, each
with a hand-drawn pictogram, a short title and one-line caption.
Run: python3 draw.py  (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (14, 30, 51)          # deep navy
CELL = (27, 50, 79)        # panel navy
CELL_EDGE = (46, 74, 107)  # panel outline
GOLD = (232, 184, 75)      # accent gold
WHITE = (255, 255, 255)
SUB = (185, 199, 217)      # light grey-blue
RED = (235, 94, 70)        # explosion red-orange

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_bars(d, x0, y0, s):
    """Rising bar chart with an arrow (IPO)."""
    bars = [(0.12, 0.45), (0.42, 0.68), (0.72, 0.92)]
    for fx, fh in bars:
        bx = x0 + fx * s
        by = y0 + s - fh * s
        d.rectangle([bx, by, bx + 0.2 * s, y0 + s], fill=GOLD)
    d.line([(x0 + 0.05 * s, y0 + 0.48 * s), (x0 + 0.5 * s, y0 + 0.22 * s),
            (x0 + 0.95 * s, y0 + 0.02 * s)], fill=WHITE, width=6)
    d.polygon([(x0 + 0.95 * s, y0 + 0.02 * s), (x0 + 0.8 * s, y0 + 0.02 * s),
               (x0 + 0.95 * s, y0 + 0.17 * s)], fill=WHITE)


def draw_scales(d, x0, y0, s):
    """Scales of justice."""
    cx = x0 + s / 2
    d.line([(cx, y0 + 0.08 * s), (cx, y0 + 0.92 * s)], fill=GOLD, width=6)
    d.line([(x0 + 0.1 * s, y0 + 0.28 * s), (x0 + 0.9 * s, y0 + 0.28 * s)],
           fill=GOLD, width=6)
    for px in (0.18, 0.82):
        px = x0 + px * s
        d.line([(px, y0 + 0.28 * s), (px, y0 + 0.55 * s)], fill=GOLD, width=4)
        d.polygon([(px - 0.16 * s, y0 + 0.55 * s), (px + 0.16 * s, y0 + 0.55 * s),
                   (px, y0 + 0.78 * s)], outline=GOLD, width=4)
    d.line([(x0 + 0.3 * s, y0 + 0.92 * s), (x0 + 0.7 * s, y0 + 0.92 * s)],
           fill=GOLD, width=6)


def draw_globe(d, x0, y0, s):
    """Globe with meridians (climate)."""
    cx, cy, r = x0 + s / 2, y0 + s / 2, s * 0.44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=5)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=GOLD, width=4)
    d.line([(cx - r, cy), (cx + r, cy)], fill=GOLD, width=4)
    d.arc([cx - r, cy - r * 0.5, cx + r, cy + r * 0.5], 200, 340, fill=GOLD, width=4)


def draw_dome(d, x0, y0, s):
    """Capitol dome with columns (senate)."""
    d.pieslice([x0 + 0.28 * s, y0 + 0.05 * s, x0 + 0.72 * s, y0 + 0.55 * s],
               180, 360, fill=GOLD)
    d.rectangle([x0 + 0.47 * s, y0, x0 + 0.53 * s, y0 + 0.08 * s], fill=GOLD)
    # band joining the dome to the columns (no gap)
    d.rectangle([x0 + 0.24 * s, y0 + 0.52 * s, x0 + 0.76 * s, y0 + 0.58 * s],
                fill=GOLD)
    for fx in (0.2, 0.38, 0.56, 0.74):
        d.rectangle([x0 + fx * s, y0 + 0.55 * s, x0 + (fx + 0.06) * s, y0 + 0.85 * s],
                    fill=GOLD)
    d.rectangle([x0 + 0.12 * s, y0 + 0.85 * s, x0 + 0.88 * s, y0 + 0.93 * s],
                fill=GOLD)


def draw_blast(d, x0, y0, s):
    """Starburst explosion over rooftops (missile strike)."""
    cx, cy = x0 + s / 2, y0 + s * 0.38
    pts = []
    import math
    for i in range(16):
        ang = math.pi * i / 8
        r = s * 0.42 if i % 2 == 0 else s * 0.2
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=RED)
    d.ellipse([cx - s * 0.13, cy - s * 0.13, cx + s * 0.13, cy + s * 0.13],
              fill=GOLD)
    d.rectangle([x0 + 0.08 * s, y0 + 0.78 * s, x0 + 0.3 * s, y0 + 0.95 * s],
                fill=WHITE)
    d.rectangle([x0 + 0.38 * s, y0 + 0.7 * s, x0 + 0.62 * s, y0 + 0.95 * s],
                fill=WHITE)
    d.rectangle([x0 + 0.7 * s, y0 + 0.8 * s, x0 + 0.92 * s, y0 + 0.95 * s],
                fill=WHITE)


def draw_tent(d, x0, y0, s):
    """Tent with a flag (Gaza shelter)."""
    d.polygon([(x0 + 0.5 * s, y0 + 0.15 * s), (x0 + 0.08 * s, y0 + 0.85 * s),
               (x0 + 0.92 * s, y0 + 0.85 * s)], outline=GOLD, width=6)
    d.line([(x0 + 0.5 * s, y0 + 0.15 * s), (x0 + 0.5 * s, y0 + 0.85 * s)],
           fill=GOLD, width=4)
    d.line([(x0 + 0.5 * s, y0 + 0.15 * s), (x0 + 0.5 * s, y0 - 0.02 * s)],
           fill=GOLD, width=4)
    d.polygon([(x0 + 0.5 * s, y0 - 0.02 * s), (x0 + 0.78 * s, y0 + 0.08 * s),
               (x0 + 0.5 * s, y0 + 0.16 * s)], fill=RED)


STORIES = [
    ("ANTHROPIC'S $81BN IPO",
     "Shares open 34% up; valued near $2tn", draw_bars),
    ("MYANMAR GUILTY OF GENOCIDE",
     "UN court rules on the Rohingya", draw_scales),
    ("COP31 DROPS FOSSIL FUELS",
     "Final-day draft has no phase-out", draw_globe),
    ("SENATE REJECTS IRAN CURB",
     "War-powers bid fails 48\u201351", draw_dome),
    ("MISSILES HIT KYIV",
     "Overnight strikes set city ablaze", draw_blast),
    ("65,000 TENTS WAIT FOR GAZA",
     "Winter shelter stuck at the border", draw_tent),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header
    title_f = font(BOLD, 92)
    date_f = font(BOLD, 44)
    d.text((W // 2, 78), "WORLD NEWS", font=title_f, fill=WHITE, anchor="ma")
    d.text((W // 2, 172), "Friday 20 November 2026", font=date_f, fill=GOLD,
           anchor="ma")
    d.line([(120, 232), (W - 120, 232)], fill=GOLD, width=4)

    # Grid: 2 cols x 3 rows
    margin, gap_x, gap_y = 32, 24, 20
    top = 258
    cw = (W - 2 * margin - gap_x) // 2
    ch = (H - top - 34 - 2 * gap_y) // 3
    head_f = font(BOLD, 33)
    sub_f = font(REG, 24)

    for i, (head, sub, icon) in enumerate(STORIES):
        row, col = divmod(i, 2)
        x = margin + col * (cw + gap_x)
        y = top + row * (ch + gap_y)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=18, fill=CELL,
                            outline=CELL_EDGE, width=2)
        # pictogram in a square at the left
        isz = 104
        ix = x + 22
        iy = y + (ch - isz) // 2
        icon(d, ix, iy, isz)
        # text to the right of the pictogram
        tx = x + 22 + isz + 18
        tw = x + cw - 20 - tx
        lines = wrap(d, head, head_f, tw)
        ly = y + (ch - (len(lines) * 40 + 8 + 2 * 30)) // 2
        for ln in lines:
            d.text((tx, ly), ln, font=head_f, fill=WHITE)
            ly += 40
        ly += 8
        for ln in wrap(d, sub, sub_f, tw):
            d.text((tx, ly), ln, font=sub_f, fill=SUB)
            ly += 30

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
