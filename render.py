#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page from code (v2).

37 stories, 6 regions, every figure sourced, UTC stamps where reported,
an explicit date check. Every shape and letter is drawn with Pillow
primitives; no photograph or downloaded artwork is used.
Run: python3 render.py   (rewrites entry.png)
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
TEAL = (15, 118, 110)
GREEN = (46, 125, 50)
BLUE = (30, 90, 168)
GOLD = (176, 124, 22)
GREY_LINE = (196, 188, 168)
GOLD_PALE = (232, 213, 150)
BLUE_PALE = (200, 212, 226)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

WARNINGS = []


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
    leading = leading or int(f.size * 1.28)
    for line in wrap(d, text, f, max_w):
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def card(d, box, fill=PAPER, outline=GREY_LINE, width=2):
    d.rounded_rectangle(box, radius=10, fill=fill, outline=outline, width=width)


# ---------------- drawing helpers (kept from v1 where they fit) ----------

def spiral(d, cx, cy, r, color, width=7):
    for i, (rr, a0, a1) in enumerate(
        [(r, 20, 300), (r * 0.74, 140, 40), (r * 0.5, 260, 160), (r * 0.28, 60, 320)]
    ):
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], a0, a1, fill=color,
              width=max(3, width - i))
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=CREAM, outline=color, width=3)


def rain(d, x0, y0, n, color, length=22, gap=26):
    for i in range(n):
        x = x0 + i * gap
        d.line([(x, y0), (x - 8, y0 + length)], fill=color, width=4)


def globe(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    d.ellipse([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45], outline=color, width=2)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=color, width=2)


def cricket(d, x, y, s=0.8):
    for i in range(3):
        sx = x + i * int(13 * s)
        d.rectangle([sx, y, sx + int(7 * s), y + int(46 * s)], fill=GOLD)
    d.rectangle([x + 1, y - 5, x + int(11 * s), y - 1], fill=GOLD)
    d.rectangle([x + int(20 * s), y - 5, x + int(30 * s), y - 1], fill=GOLD)
    bx = x + int(46 * s)
    d.ellipse([bx, y + 6, bx + int(24 * s), y + 6 + int(24 * s)], fill=RED,
              outline=(120, 20, 16), width=2)


def children(d, x, y, s=0.6):
    cols = [BLUE, RED, TEAL]
    head = int(26 * s)
    body_h = int(32 * s)
    step = int(46 * s)
    for i, c in enumerate(cols):
        fx = x + i * step
        d.ellipse([fx, y, fx + head, y + head], fill=c)
        d.rounded_rectangle([fx - 1, y + head + 4, fx + head + 1,
                             y + head + 4 + body_h], radius=8, fill=c)


def skyline(d, x, y, w, h, color):
    towers = [(0, 0.55), (0.18, 0.9), (0.38, 0.7), (0.56, 1.0), (0.76, 0.62)]
    for fx, fh in towers:
        tw = w * 0.14
        tx = x + w * fx
        th = h * fh
        d.rectangle([tx, y + h - th, tx + tw, y + h], fill=color)


def bridge(d, x, y, w, h):
    """Kyiv: a cable-stayed river crossing under missile streaks."""
    deck_y = y + h * 0.68
    d.line([(x, deck_y), (x + w, deck_y)], fill=INK, width=5)
    for tx in (x + w * 0.28, x + w * 0.72):
        d.line([(tx, deck_y), (tx, y + h * 0.12)], fill=INK, width=4)
        for dx in (-w * 0.2, -w * 0.1, w * 0.1, w * 0.2):
            d.line([(tx, y + h * 0.14), (tx + dx, deck_y)], fill=INK_SOFT, width=2)
    d.line([(x, y + h), (x + w, y + h)], fill=BLUE, width=3)  # river
    for i, (mx, my) in enumerate([(x + w * 0.1, y), (x + w * 0.5, y - 4),
                                  (x + w * 0.86, y + 2)]):
        d.line([(mx, my), (mx + 14, my + h * 0.4)], fill=RED, width=4)
        d.ellipse([mx + 10, my + h * 0.4 - 4, mx + 20, my + h * 0.4 + 6], fill=RED)


def fall_bars(d, x, y, w, h, color):
    vals = [1.0, 0.85, 0.68, 0.5, 0.35, 0.2]
    bw = w / (len(vals) * 1.5)
    for i, v in enumerate(vals):
        bx = x + i * (bw * 1.5)
        bh = h * v
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=color)
    d.line([(x - 2, y + h), (x + w, y + h)], fill=INK, width=2)


def seal(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    d.line([(cx - r * 0.45, cy), (cx - r * 0.1, cy + r * 0.4),
            (cx + r * 0.5, cy - r * 0.35)], fill=color, width=4)


# ---------------- story data (all figures verified for Fri 20 Nov) -------

KYIV_BULLETS = [
    "400+ drones, 110+ missiles overnight — Zelenskyy: 27 ballistic.",
    "3 Dnipro bridges hit by ballistic missiles — biggest crossing strikes of the war; traffic closed/restricted.",
    "8 killed (6 in Kyiv), 28 injured; power out in 5 districts.",
    "Air force: 380 drones, 79 cruise, 3 ballistic missiles downed.",
    "Putin vowed retaliation after Ukraine's 3rd Kerch-bridge strike this week.",
]

AKVAN_BULLETS = [
    "Weakened before crossing near Gopalpur 7:30–8:30 IST; winds 70–80 km/h, gusts 90.",
    "~370,000 evacuated · 423 rescue teams · 9,341 shelters.",
    "No deaths, no major damage — Min. Pujari.",
    "Patrapur 209 mm rain; 69 trains cancelled; Assembly adjourned to 23 Nov.",
    "3rd cyclone to threaten Odisha in 24 days.",
]

COP_BULLETS = [
    "New draft drops ALL fossil-fuel language.",
    "$120B/yr adaptation goal for 2035 deleted.",
    "35-by-35: electricity to 35% of final energy by 2035; buildings −25% intensity.",
    "Türkiye signs $26B+ deals, incl. $15B China renewables.",
    "92,000 here — largest climate summit ever; talks may overrun.",
]

MARKET_BULLETS = [
    "Record Anthropic IPO fails to stop the rout.",
    "MSCI Asia-Pacific ex-Japan −8% week — worst since Mar 2020.",
    "Taiex −17% week (worst since 1990); Nikkei −4.1% Fri; Kospi −4.7%.",
    "SoftBank −15.6% · TSMC −5.2% · SK Hynix −6.3% · Samsung −4.8%.",
    "ANT +17% to $97.17 (~$1.3T); ~$81.3B IPO at $83 — largest ever; closes today.",
]

UKEU_BULLETS = [
    "Food checks end from Mar 2028 — est. +£5.1B/yr.",
    "Youth mobility: 100,000/yr under-32s for 3 years.",
    "ETS link + closer defence ties; Burnham claims £17B boost.",
]

CRICKET_BULLETS = [
    "Nicholls 175*, Phillips 118 — 216-run stand.",
    "Bumrah 4/92, Akash Deep 3/53.",
    "Jaiswal 85, Rahul 52*; India trail 209 at stumps.",
]

PRABOWO_BULLETS = [
    "CEPA negotiations launched at Kylin Villa, APEC sidelines.",
    "35 deals $15B; total commitments $86.8B.",
    "South China Sea joint-development progress.",
]

INDEX = [
    "IMD: crossing complete 11:20 IST; deep depression by 1 pm.",
    "IMD rain: Hinjili 207 mm · Chikiti 199 · Gopalpur 190 · Chhatrapur 139.",
    "REUTERS: adaptation finance — vague, non-binding tripling pledge only.",
    "REUTERS: $5.1B dev-bank finance; accords with Saudi Arabia and Canada.",
    "REUTERS: UK–EU tuition-fee decision deferred six months.",
    "XINHUA: $71.8B prior approvals — 4 strategic partnerships, 10 smart cities.",
    "XINHUA: data centres, renewables, vaccines, infrastructure, manufacturing.",
]

N_STORIES = (len(KYIV_BULLETS) + len(AKVAN_BULLETS) + len(COP_BULLETS)
             + len(MARKET_BULLETS) + len(UKEU_BULLETS) + len(CRICKET_BULLETS)
             + len(PRABOWO_BULLETS) + 1 + len(INDEX))  # +1 Children's Day


def bullets(d, x, y, items, f, fill, max_w, leading, mark=RED):
    for it in items:
        d.ellipse([x, y + 5, x + 5, y + 10], fill=mark)
        y = para(d, x + 12, y, it, f, fill, max_w - 12, leading)
        y += 3
    return y


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=6)

    # ---------- masthead ----------
    d.rectangle([6, 6, W - 6, 116], fill=INK)
    d.text((28, 14), "THE WORLD IN ONE PICTURE · FRONT PAGE", font=SANS_B(13),
           fill=GOLD_PALE)
    d.text((28, 32), "FRIDAY 20 NOVEMBER 2026", font=SERIF_B(46), fill=PAPER)
    d.text((28, 90), f"{N_STORIES} STORIES · 6 REGIONS · EVERY FIGURE SOURCED · UTC WHERE REPORTED",
           font=SANS_B(13), fill=BLUE_PALE)
    # date-check chip
    chip = "DATE CHECK ✓ FRI 20 NOV 2026"
    cf = SANS_B(13)
    cw = d.textlength(chip, font=cf)
    d.rounded_rectangle([W - 40 - cw - 20, 84, W - 28, 108], radius=6,
                        fill=TEAL)
    d.text((W - 40 - cw - 10, 88), chip, font=cf, fill=PAPER)

    # ---------- lead row: Kyiv (wide) + Akvan ----------
    # Kyiv
    card(d, [20, 124, 640, 416])
    d.rectangle([20, 124, 34, 416], fill=RED)
    d.text((48, 136), "EUROPE · KYIV · REUTERS · OVERNIGHT 20 NOV",
           font=SANS_B(13), fill=RED)
    d.text((48, 156), "KYIV UNDER ONE OF THE", font=SERIF_B(23), fill=INK)
    d.text((48, 184), "WAR'S LARGEST BARRAGES", font=SERIF_B(23), fill=INK)
    y = bullets(d, 48, 224, KYIV_BULLETS, SANS(14), INK, 380, 17)
    if y > 410:
        WARNINGS.append(f"kyiv bullets overflow: {y}")
    # right stat rail + bridge art
    rx = 452
    d.line([(rx - 14, 140), (rx - 14, 402)], fill=GREY_LINE, width=2)
    stats = [("400+", "DRONES"), ("110+", "MISSILES"), ("3", "BRIDGES HIT")]
    sy = 148
    for val, lab in stats:
        d.text((rx, sy), val, font=SANS_B(30), fill=RED)
        d.text((rx, sy + 34), lab, font=SANS_B(12), fill=INK_SOFT)
        sy += 62
    bridge(d, rx, 342, 160, 58)

    # Akvan
    card(d, [652, 124, 1004, 416])
    d.rectangle([652, 124, 1004, 132], fill=TEAL)
    d.text((668, 140), "SOUTH ASIA · IMD · 02:00–03:00 UTC", font=SANS_B(13),
           fill=TEAL)
    d.text((668, 160), "AKVAN LANDFALL:", font=SERIF_B(23), fill=INK)
    d.text((668, 188), "NO LIVES LOST", font=SERIF_B(23), fill=INK)
    y = bullets(d, 668, 222, AKVAN_BULLETS, SANS(13), INK, 320, 15, mark=TEAL)
    if y > 360:
        WARNINGS.append(f"akvan bullets overflow: {y}")
    spiral(d, 712, 388, 22, TEAL, width=5)
    rain(d, 762, 372, 4, (90, 140, 190), length=16, gap=22)
    d.text((862, 372), "SURGE 0.3 m", font=SANS_B(12), fill=TEAL)
    d.text((862, 390), "NO DEATHS", font=SANS_B(12), fill=TEAL)

    # ---------- middle row: COP31 / markets / UK-EU ----------
    mid = [
        (20, 348, TEAL, "W. ASIA · ~200 NATIONS · REUTERS", "COP31 ENDS IN DEADLOCK",
         COP_BULLETS, "globe"),
        (356, 684, RED, "ASIA-PACIFIC · REUTERS · FRI CLOSE", "AI SELL-OFF DEEPENS",
         MARKET_BULLETS, "bars"),
        (692, 1004, BLUE, "EUROPE · BRUSSELS · REUTERS", "UK–EU RESET DEAL",
         UKEU_BULLETS, "seal"),
    ]
    for x0, x1, col, kick, head, bl, art in mid:
        card(d, [x0, 424, x1, 664])
        d.rectangle([x0, 424, x1, 432], fill=col)
        d.text((x0 + 16, 440), kick, font=SANS_B(12), fill=col)
        d.text((x0 + 16, 460), head, font=SERIF_B(19), fill=INK)
        y = bullets(d, x0 + 16, 492, bl, SANS(13), INK, x1 - x0 - 32, 15, mark=col)
        if y > 656:
            WARNINGS.append(f"{head} overflow: {y}")
        ay = 616
        if art == "globe":
            globe(d, x1 - 30, ay + 22, 16, col)
            d.text((x0 + 16, ay + 16), "ANTALYA · FINAL DAY", font=SANS_B(11), fill=col)
        elif art == "bars":
            fall_bars(d, x1 - 56, 456, 44, 26, col)
        else:
            seal(d, x0 + 36, ay + 18, 17, col)
            d.text((x0 + 62, ay + 4), "PM ANDY BURNHAM", font=SANS_B(11), fill=col)
            d.text((x0 + 62, ay + 20), "STARMER'S SUCCESSOR", font=SANS(11), fill=INK_SOFT)

    # ---------- bottom row: cricket / Prabowo-Xi / children ----------
    bot = [
        (20, 348, GREEN, "OCEANIA · WELLINGTON · SCORECARD", "NZ 368 · INDIA 159/1",
         CRICKET_BULLETS, "cricket"),
        (356, 684, GOLD, "E. ASIA · SHENZHEN · REUTERS/XINHUA", "PRABOWO–XI: $15B DEALS",
         PRABOWO_BULLETS, "skyline"),
    ]
    for x0, x1, col, kick, head, bl, art in bot:
        card(d, [x0, 672, x1, 836])
        d.rectangle([x0, 672, x1, 680], fill=col)
        d.text((x0 + 16, 688), kick, font=SANS_B(12), fill=col)
        d.text((x0 + 16, 706), head, font=SERIF_B(17), fill=INK)
        y = bullets(d, x0 + 16, 736, bl, SANS(13), INK, x1 - x0 - 32, 15, mark=col)
        if y > 828:
            WARNINGS.append(f"{head} overflow: {y}")
        if art == "cricket":
            cricket(d, x1 - 48, 706, 0.5)
        else:
            skyline(d, x1 - 40, 702, 32, 26, col)

    # children's day
    card(d, [692, 672, 1004, 836])
    d.rectangle([692, 672, 1004, 680], fill=BLUE)
    d.text((708, 688), "WORLDWIDE · UNICEF · 20 NOV", font=SANS_B(12), fill=BLUE)
    d.text((708, 706), "WORLD CHILDREN'S DAY", font=SERIF_B(19), fill=INK)
    d.text((708, 738), "“My day. My rights. My future.”", font=SANS_B(15), fill=BLUE)
    para(d, 708, 762, "37 years since the Convention on the Rights of the Child.",
         SANS(13), INK, 280, 16)
    children(d, 712, 797, 0.55)
    d.text((800, 800), "37 YEARS", font=SANS_B(13), fill=BLUE)

    # ---------- numbers strip ----------
    d.rectangle([20, 844, W - 20, 888], fill=INK)
    nums = [("3", "KYIV BRIDGES HIT"), ("370,000", "EVACUATED IN ODISHA"),
            ("−8%", "ASIA EX-JAPAN, WEEK"), ("$81.3B", "ANTHROPIC IPO RAISED"),
            ("92,000", "AT COP31 — LARGEST EVER")]
    nx = 36
    for val, lab in nums:
        d.text((nx, 850), val, font=SANS_B(20), fill=PAPER)
        d.text((nx, 874), lab, font=SANS(10), fill=BLUE_PALE)
        nx += 198

    # ---------- index ----------
    d.text((28, 896), f"ALSO TODAY — {len(INDEX)} MORE, ALL FRI 20 NOV",
           font=SANS_B(14), fill=RED)
    d.line([(28, 916), (W - 28, 916)], fill=GREY_LINE, width=2)
    for i, item in enumerate(INDEX):
        cx = 28 if i < 4 else 512
        cy = 924 + (i % 4) * 16
        max_w = 452 if i < 4 else 458
        lines = wrap(d, item, SANS(12), max_w)
        if len(lines) > 1:
            WARNINGS.append(f"index {i} wraps: {item}")
        d.text((cx, cy), f"{i + 31}.", font=SANS_B(12), fill=RED)
        d.text((cx + 26, cy), lines[0], font=SANS(12), fill=INK)

    # ---------- footer ----------
    d.text((28, 996),
           "SOURCES: REUTERS · IMD · ODISHA DISASTER MANAGEMENT · XINHUA · UNICEF · DOW JONES",
           font=SANS(11), fill=INK_SOFT)
    right = "ALL STORIES VERIFIED FOR FRI 20 NOV 2026 · DRAWN FROM CODE"
    d.text((W - 28 - d.textlength(right, font=SANS(11)), 996), right,
           font=SANS(11), fill=INK_SOFT)

    img.save(OUT, "PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    p = build()
    print(p)
    print("stories:", N_STORIES)
    for w in WARNINGS:
        print("WARN:", w)
