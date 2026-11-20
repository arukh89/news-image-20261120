#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news poster from code.

Every shape and letter is drawn with Pillow primitives; no photograph or
downloaded artwork is used. Run: python3 render.py  (rewrites entry.png).
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette: newsprint cream, ink navy, signal red, teal, green, blue ---
CREAM = (246, 241, 227)
PAPER = (255, 252, 244)
INK = (20, 38, 63)
INK_SOFT = (52, 68, 92)
RED = (178, 44, 36)
RED_SOFT = (226, 93, 78)
TEAL = (15, 118, 110)
GREEN = (46, 125, 50)
BLUE = (30, 90, 168)
GOLD = (176, 124, 22)
GREY_LINE = (196, 188, 168)
LIGHT_BLUE = (214, 231, 245)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(d, text, f, max_w):
    """Greedy word wrap measured with the real font."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, fill, max_w, leading=None):
    """Draw wrapped paragraph; return y just below the last line."""
    leading = leading or int(f.size * 1.28)
    for line in wrap(d, text, f, max_w):
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def kicker(d, x, y, text, color=RED):
    d.text((x, y), text, font=SANS_B(13), fill=color)
    return y + 20


def card(d, box, fill=PAPER, outline=GREY_LINE, width=2):
    d.rounded_rectangle(box, radius=10, fill=fill, outline=outline, width=width)


def spiral(d, cx, cy, r, color, width=7):
    """Cyclone: concentric broken arcs that tighten toward the eye."""
    for i, (rr, a0, a1) in enumerate(
        [(r, 20, 300), (r * 0.74, 140, 40), (r * 0.5, 260, 160), (r * 0.28, 60, 320)]
    ):
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], a0, a1, fill=color,
              width=max(3, width - i))
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=CREAM, outline=color, width=3)


def rain(d, x0, y0, n, color, length=26, gap=30):
    for i in range(n):
        x = x0 + i * gap
        d.line([(x, y0), (x - 9, y0 + length)], fill=color, width=4)


def globe(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    d.ellipse([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45], outline=color, width=3)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=color, width=3)
    d.arc([cx - r, cy - r, cx + r, cy + r], 300, 60, fill=color, width=3)


def cricket(d, x, y):
    """Three stumps, bails and a red ball (compact, ~46 px tall)."""
    for i in range(3):
        sx = x + i * 13
        d.rectangle([sx, y, sx + 7, y + 46], fill=(176, 124, 22))
    d.rectangle([x + 1, y - 5, x + 11, y - 1], fill=(176, 124, 22))
    d.rectangle([x + 20, y - 5, x + 30, y - 1], fill=(176, 124, 22))
    d.ellipse([x + 46, y + 6, x + 70, y + 30], fill=RED, outline=(120, 20, 16), width=2)
    d.arc([x + 46, y + 6, x + 70, y + 30], 40, 200, fill=(255, 255, 255), width=2)


def children(d, x, y, s=0.6):
    """Three simple figures holding hands (compact, ~40 px tall)."""
    cols = [(30, 90, 168), (178, 44, 36), (15, 118, 110)]
    head = int(26 * s)
    body_h = int(32 * s)
    step = int(46 * s)
    for i, c in enumerate(cols):
        fx = x + i * step
        d.ellipse([fx, y, fx + head, y + head], fill=c)
        d.rounded_rectangle([fx - 1, y + head + 4, fx + head + 1,
                             y + head + 4 + body_h], radius=8, fill=c)


def skyline(d, x, y, w, h, color):
    """Shenzhen-style towers of varied heights."""
    towers = [(0, 0.55), (0.18, 0.9), (0.38, 0.7), (0.56, 1.0), (0.76, 0.62)]
    for fx, fh in towers:
        tw = w * 0.14
        tx = x + w * fx
        th = h * fh
        d.rectangle([tx, y + h - th, tx + tw, y + h], fill=color)
        for wy in range(3):
            d.rectangle([tx + 3, y + h - th + 6 + wy * 12, tx + tw - 3,
                         y + h - th + 12 + wy * 12], fill=CREAM)


def bars(d, x, y, w, h, color):
    """Rising bar chart."""
    vals = [0.35, 0.5, 0.42, 0.68, 0.85, 1.0]
    bw = w / (len(vals) * 1.5)
    for i, v in enumerate(vals):
        bx = x + i * (bw * 1.5)
        bh = h * v
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=color)
    d.line([(x - 4, y + h), (x + w, y + h)], fill=INK, width=2)


def world_map(d, x, y, w, h):
    """Schematic continents as soft blobs; dots mark the day's places."""
    blobs = [
        # (points, colour) — rough equirectangular shapes
        ([(18, 22), (52, 8), (86, 14), (92, 40), (66, 52), (40, 58), (14, 44)],
         (196, 214, 190)),  # N America
        ([(58, 74), (84, 70), (96, 96), (78, 122), (62, 100)], (196, 214, 190)),
        ([(128, 34), (152, 26), (172, 44), (160, 78), (138, 66)], (196, 214, 190)),
        ([(176, 30), (206, 18), (232, 30), (226, 62), (200, 74), (182, 56)],
         (196, 214, 190)),  # Eurasia
        ([(222, 96), (244, 92), (252, 112), (234, 122)], (196, 214, 190)),  # Oceania
    ]
    sx, sy = w / 270.0, h / 132.0
    for pts, col in blobs:
        d.polygon([(x + px * sx, y + py * sy) for px, py in pts], fill=col)
    # story dots: (lon-ish, lat-ish, label) in the same 270x132 frame
    dots = [
        (208, 62, "ODISHA"), (172, 40, "ANTALYA"), (252, 112, "WELLINGTON"),
        (224, 52, "SHENZHEN"), (52, 38, "NEW YORK"), (222, 76, "KUALA LUMPUR"),
    ]
    for px, py, label in dots:
        dx, dy = x + px * sx, y + py * sy
        d.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=RED, outline=(255, 255, 255),
                  width=2)
        f = SANS_B(10)
        lw = d.textlength(label, font=f)
        lx = dx + 8
        if lx + lw > x + w - 4:  # near the right edge: label to the left
            lx = dx - 8 - lw
        d.text((lx, dy - 7), label, font=f, fill=INK)


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=6)

    # ---------- header ----------
    d.rectangle([6, 6, W - 6, 148], fill=INK)
    d.text((28, 22), "THE WORLD IN ONE PICTURE", font=SANS_B(15), fill=(232, 213, 150))
    d.text((28, 44), "FRIDAY 20 NOVEMBER 2026", font=SERIF_B(52), fill=(255, 252, 244))
    d.text((28, 108), "Cyclone Akvan hits Odisha  ·  COP31 closes  ·  Cricket in Wellington",
           font=SANS(19), fill=(200, 212, 226))
    d.text((W - 28 - 210, 108), "SIX STORIES, ONE DAY", font=SANS_B(14),
           fill=(232, 213, 150))

    # ---------- lead: Cyclone Akvan ----------
    card(d, [20, 162, W - 20, 412])
    d.rectangle([20, 162, 34, 412], fill=RED)
    spiral(d, 150, 292, 78, RED)
    rain(d, 70, 356, 5, (90, 140, 190))
    x = 268
    y = kicker(d, x, 178, "INDIA  ·  BAY OF BENGAL", RED)
    d.text((x, y), "CYCLONE AKVAN MAKES LANDFALL", font=SERIF_B(34), fill=INK)
    y = para(d, x, y + 50,
             "Severe Cyclonic Storm Akvan crosses the coast near Gopalpur, "
             "Odisha, around noon today (06:30 UTC), with winds of 90–100 km/h, "
             "gusting to 110.",
             SANS(19), INK, 700)
    y = para(d, x, y + 6,
             "More than 300,000 people moved to shelters; 423 rescue teams "
             "deployed; 69 trains cancelled.",
             SANS_B(19), INK, 700)
    d.text((x, y + 8), "20–30 cm of rain · 0.5–1 m storm surge · red warnings in 6 districts",
           font=SANS(16), fill=INK_SOFT)

    # ---------- middle row: three panels ----------
    panels = [
        # (x0, x1, kicker, colour, headline, body, art)
        (20, 348, "CLIMATE  ·  ANTALYA, TÜRKIYE", TEAL, "COP31 CLOSES TODAY",
         "Nearly 200 countries face a deadline for a final text. Fossil fuels "
         "and adaptation money are still unresolved.",
         "globe"),
        (360, 688, "SPORT  ·  WELLINGTON", GREEN, "NZ 317–6 AT LUNCH, DAY 2",
         "Glenn Phillips 118 and Henry Nicholls 146* lift New Zealand from "
         "70–5 on day one against India.",
         "cricket"),
        (700, 1004, "UNICEF  ·  WORLDWIDE", BLUE, "WORLD CHILDREN'S DAY",
         "“My day. My rights. My future.” 37 years since the Convention on the "
         "Rights of the Child.",
         "children"),
    ]
    for x0, x1, kick, col, head, body, art in panels:
        card(d, [x0, 426, x1, 634])
        d.rectangle([x0, 426, x1, 434], fill=col)
        y = kicker(d, x0 + 16, 442, kick, col)
        yy = y
        for line in wrap(d, head, SERIF_B(22), x1 - x0 - 32):
            d.text((x0 + 16, yy), line, font=SERIF_B(22), fill=INK)
            yy += 27
        para(d, x0 + 16, yy + 4, body, SANS(15), INK, x1 - x0 - 32)
        ax, ay = x0 + 16, 634 - 52
        if art == "globe":
            globe(d, ax + 30, ay + 22, 22, col)
            d.text((ax + 66, ay + 12), "9–20 NOV", font=SANS_B(14), fill=col)
        elif art == "cricket":
            cricket(d, ax + 4, ay + 2)
            d.text((ax + 96, ay + 12), "216-RUN STAND", font=SANS_B(13), fill=col)
        else:
            children(d, ax + 4, ay + 6, 0.6)
            d.text((ax + 108, ay + 12), "37 YEARS", font=SANS_B(14), fill=col)

    # ---------- lower row: two panels + map ----------
    card(d, [20, 650, 348, 826])
    d.rectangle([20, 650, 348, 658], fill=GOLD)
    y = kicker(d, 36, 666, "DIPLOMACY  ·  SHENZHEN", GOLD)
    d.text((36, y), "PRABOWO MEETS", font=SERIF_B(24), fill=INK)
    d.text((36, y + 29), "XI TODAY", font=SERIF_B(24), fill=INK)
    para(d, 36, y + 66,
         "Prabowo holds a bilateral with China's Xi Jinping after the APEC summit.",
         SANS(14), INK, 296)
    d.line([(36, 806), (332, 806)], fill=GREY_LINE, width=1)
    d.text((36, 812), "INDONESIA–CHINA BUSINESS FORUM, TODAY", font=SANS_B(11),
           fill=GOLD)

    card(d, [360, 650, 664, 826])
    d.rectangle([360, 650, 664, 658], fill=INK)
    y = kicker(d, 376, 666, "BUSINESS  ·  NEW YORK", INK)
    d.text((376, y), "ANTHROPIC IPO", font=SERIF_B(24), fill=INK)
    d.text((376, y + 29), "DUE TO CLOSE", font=SERIF_B(24), fill=INK)
    para(d, 376, y + 66,
         "Priced at $83, about $1.5 trillion fully diluted. The largest IPO on record.",
         SANS(14), INK, 272)
    d.line([(376, 806), (648, 806)], fill=GREY_LINE, width=1)
    d.text((376, 812), "STOCK TRADES AS ANT  ·  $83 A SHARE", font=SANS_B(11),
           fill=INK)

    card(d, [676, 650, 1004, 826], fill=LIGHT_BLUE)
    d.text((692, 664), "WHERE TODAY HAPPENED", font=SANS_B(13), fill=INK)
    world_map(d, 692, 686, 296, 126)

    # ---------- numbers band ----------
    d.rectangle([20, 842, W - 20, 884], fill=INK)
    nums = [("300,000+", "EVACUATED IN ODISHA"), ("90–100 km/h", "AKVAN WINDS"),
            ("317–6", "NZ AT LUNCH, DAY 2"), ("~200", "NATIONS AT COP31")]
    nx = 36
    for val, lab in nums:
        d.text((nx, 848), val, font=SANS_B(17), fill=(255, 252, 244))
        d.text((nx, 868), lab, font=SANS(11), fill=(200, 212, 226))
        nx += 252

    # ---------- index: also today ----------
    d.text((28, 896), "ALSO TODAY", font=SANS_B(15), fill=RED)
    d.line([(28, 918), (W - 28, 918)], fill=GREY_LINE, width=2)
    items = [
        "Akvan: 20–30 cm of rain; flood warnings in 7 districts.",
        "Akvan: schools shut in 11 districts; 69 trains cancelled.",
        "Akvan is the third cyclone on this coast in a month.",
        "COP31: Türkiye's 35-by-35 power pledge on the table.",
        "Anthropic shares trade a second day as ANT.",
        "GTA VI on sale for a second day after Thursday's launch.",
        "Children's Day: KL Tower and Exchange 106 go blue tonight.",
        "COP31: final deals often run past the scheduled close.",
    ]
    for i, item in enumerate(items):
        cx = 28 if i < 4 else 524
        cy = 930 + (i % 4) * 15
        d.text((cx, cy), f"{i + 1}.", font=SANS_B(12), fill=RED)
        d.text((cx + 22, cy), item, font=SANS(12), fill=INK)

    # ---------- footer ----------
    d.text((28, 1002),
           "Sources: India Meteorological Department · Reuters · AP · AFP · UNICEF · APEC Secretariat",
           font=SANS(11), fill=INK_SOFT)
    right = "Drawn entirely from code — no photographs"
    d.text((W - 28 - d.textlength(right, font=SANS(11)), 1002), right,
           font=SANS(11), fill=INK_SOFT)

    img.save(OUT, "PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    print(build())
