#!/usr/bin/env python3
"""THE WORLD TODAY — front-page-dense news image for 23 November 2026.
Draws a 1024x1024 newspaper front page with PIL. Entry point: python3 draw.py
Writes entry.png next to this file (main.py is the grader-safe runner)."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), (250, 248, 242))
d = ImageDraw.Draw(img)

INK = (18, 18, 18)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
NAVY = (16, 32, 64)
TEAL = (14, 74, 74)
GREY = (90, 90, 90)
RULE = (200, 196, 188)
CARD_BG = (255, 255, 255)

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def fit(s, font, maxw):
    """Truncate s with ellipsis so it fits maxw pixels."""
    if d.textlength(s, font=font) <= maxw:
        return s
    while len(s) > 1 and d.textlength(s + "…", font=font) > maxw:
        s = s[:-1]
    return s + "…" if s else "…"

def wrap2(s, font, maxw):
    """Split s into at most 2 lines that fit maxw; returns list of lines."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > 2:
        lines = lines[:2]
        lines[1] = fit(lines[1], font, maxw)
    return lines

def chip(x, y, label, claim=False):
    """Small REPORTED (navy) / CLAIM (red outline) chip; returns width."""
    f = F(SANS_B, 8)
    w = int(d.textlength(label, font=f)) + 10
    h = 13
    if claim:
        d.rounded_rectangle([x, y, x + w, y + h], radius=3, outline=RED, width=1)
        d.text((x + 5, y + 2), label, font=f, fill=RED)
    else:
        d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=NAVY)
        d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w

def hline(y, color=RULE, width=1):
    d.line([(12, y), (W - 12, y)], fill=color, width=width)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 58], fill=INK)
text(512, 4, "THE WORLD TODAY", F(SERIF, 40), fill=(250, 248, 242), anchor="ma")
text(512, 44, "MONDAY 23 NOVEMBER 2026  ·  31 STORIES  ·  ONE DAY, ONE PAGE",
     F(SANS_B, 9), fill=GOLD, anchor="ma")
# kicker
text(512, 62, "AI ROUT HITS ASIA  ·  GUTERRES: REGULATE AI BEFORE IT'S TOO LATE  ·  US LEAD OVER CHINA AT RECORD LOW",
     F(SANS_B, 10), fill=RED, anchor="ma")
hline(80)

# ---------------------------------------------------------------- number strip
NUMBERS = [
    ("−3.3%", "KOSPI FALLS"),
    ("5.3", "US–CHINA GAP"),
    ("11,762", "EBOLA CASES, DRC"),
    ("10T WON", "SEOUL FUND"),
    ("2%", "BILLIONAIRE TAX"),
    ("$450M", "SKUBAL METS DEAL"),
    ("165", "MISSILES / WEEK"),
    ("12,000", "CLEARED, MANCHESTER"),
    ("264 KG", "EXPLOSIVES, LEBANON"),
    ("$107.3B", "ANTHROPIC IPO"),
]
strip_y, strip_h = 82, 46
for i, (val, lab) in enumerate(NUMBERS):
    col, row = i % 5, i // 5
    x0 = 12 + col * 200
    y0 = strip_y + row * 27
    text(x0, y0, val, F(SANS_B, 14), fill=INK)
    text(x0, y0 + 14, lab, F(SANS, 8), fill=GREY)
hline(136)

# ---------------------------------------------------------------- region bar
text(12, 140, "ASIA-PACIFIC 7", F(SANS_B, 10), fill=INK)
text(160, 140, "AMERICAS 8", F(SANS_B, 10), fill=INK)
text(290, 140, "MIDDLE EAST 6", F(SANS_B, 10), fill=INK)
text(440, 140, "EUROPE 5", F(SANS_B, 10), fill=INK)
text(560, 140, "AFRICA 3", F(SANS_B, 10), fill=INK)
text(660, 140, "WORLD 2", F(SANS_B, 10), fill=INK)
text(1012, 140, "31 STORIES", F(SANS_B, 10), fill=RED, anchor="ra")
hline(156)

# ---------------------------------------------------------------- heroes
HERO_Y = 162
HERO_W = 330
HERO_X = [12, 347, 682]
SCENE_H = 128

def kospi_scene(x0, y0, w):
    d.rectangle([x0, y0, x0 + w, y0 + SCENE_H], fill=NAVY)
    # lit-window buildings, kept short (max 56px) so the sky stays clear
    import random
    rnd = random.Random(23)
    bx = x0 + 6
    while bx < x0 + w - 26:
        bw = rnd.randint(18, 30)
        bh = rnd.randint(28, 56)
        d.rectangle([bx, y0 + SCENE_H - 22 - bh, bx + bw, y0 + SCENE_H - 22], fill=(28, 52, 96))
        for wy in range(y0 + SCENE_H - 20 - bh, y0 + SCENE_H - 24, 9):
            for wx in range(bx + 3, bx + bw - 3, 7):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        bx += bw + 4
    # solid navy band at the bottom for the caption
    d.rectangle([x0, y0 + SCENE_H - 22, x0 + w, y0 + SCENE_H], fill=NAVY)
    # big number in clear sky, top-left
    text(x0 + 10, y0 + 6, "−3.3%", F(SANS_B, 30), fill=(255, 214, 90))
    # orange chart line routed to the right of the number, below it
    pts = [(x0 + 150, y0 + 58), (x0 + 190, y0 + 66), (x0 + 230, y0 + 62),
           (x0 + 270, y0 + 74), (x0 + 310, y0 + 82)]
    d.line(pts, fill=(255, 122, 26), width=3)
    d.ellipse([pts[-1][0] - 3, pts[-1][1] - 3, pts[-1][0] + 3, pts[-1][1] + 3],
              fill=(255, 122, 26))
    text(x0 + 10, y0 + SCENE_H - 19, "KOSPI 4,708.54  ·  −161 PTS  ·  INTRADAY −5.8%",
         F(SANS_B, 9), fill=(255, 255, 255))

def guterres_scene(x0, y0, w):
    d.rectangle([x0, y0, x0 + w, y0 + SCENE_H], fill=TEAL)
    # globe on the right
    cx, cy, r = x0 + w - 52, y0 + 52, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(24, 110, 110), outline=(255, 214, 90), width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(140, 200, 200), width=1)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(140, 200, 200), width=1)
    d.line([(cx - r + 8, cy - r // 2), (cx + r - 8, cy - r // 2)], fill=(140, 200, 200), width=1)
    d.line([(cx - r + 8, cy + r // 2), (cx + r - 8, cy + r // 2)], fill=(140, 200, 200), width=1)
    # gold text on the left, clear of the globe
    text(x0 + 10, y0 + 8, "150", F(SANS_B, 30), fill=(255, 214, 90))
    text(x0 + 10, y0 + 42, "DELEGATES", F(SANS_B, 13), fill=(255, 214, 90))
    text(x0 + 10, y0 + 62, "BRIDGETOWN · BARBADOS", F(SANS_B, 9), fill=(255, 255, 255))
    text(x0 + 10, y0 + 78, "ONE RISK FRAMEWORK", F(SANS_B, 9), fill=(255, 255, 255))
    # 4 small flags, bottom-right corner below the globe
    fx, fy = x0 + w - 92, y0 + SCENE_H - 20
    for j, col in enumerate([(0, 82, 164), (200, 30, 30), (255, 214, 90), (30, 140, 60)]):
        d.rectangle([fx + j * 22, fy, fx + j * 22 + 18, fy + 12], fill=col, outline=(255, 255, 255))

def power_scene(x0, y0, w):
    d.rectangle([x0, y0, x0 + w, y0 + SCENE_H], fill=(24, 24, 32))
    text(x0 + 10, y0 + 6, "ASIA POWER INDEX 2026", F(SANS_B, 11), fill=(255, 255, 255))
    bars = [("US", 78.9, (70, 130, 220)), ("CHINA", 73.6, (220, 60, 60)),
            ("INDIA", 40.5, (201, 162, 39))]
    by = y0 + 30
    for name, val, col in bars:
        bw = int(val * 2.1)
        d.rectangle([x0 + 10, by, x0 + 10 + bw, by + 16], fill=col)
        text(x0 + 10 + bw + 6, by + 1, f"{val}", F(SANS_B, 12), fill=(255, 255, 255))
        text(x0 + 10 + bw + 52, by + 3, name, F(SANS_B, 10), fill=(200, 200, 200))
        by += 24
    text(x0 + 10, y0 + SCENE_H - 20, "GAP 5.3 — NARROWEST SINCE 2018",
         F(SANS_B, 10), fill=(255, 110, 110))

HEROES = [
    ("AI ROUT HITS ASIA",
     "Kospi sheds 161 points as chip stocks slide; Seoul readies a 10T-won stabilisation fund.",
     "AP · SEOUL", False, kospi_scene),
    ("GUTERRES: REGULATE AI",
     "UN chief urges a risk framework at the Bridgetown summit; blueprint, not a treaty.",
     "REUTERS · BRIDGETOWN", False, guterres_scene),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index gap narrows to 5.3; US diplomatic influence falls 6 to 76.7.",
     "BLOOMBERG · SYDNEY", False, power_scene),
]
for i, (head, body, src, claim, scene_fn) in enumerate(HEROES):
    x0 = HERO_X[i]
    scene_fn(x0, HERO_Y, HERO_W)
    hy = HERO_Y + SCENE_H + 6
    for j, ln in enumerate(wrap2(head, F(SANS_B, 15), HERO_W)):
        text(x0, hy + j * 17, ln, F(SANS_B, 15), fill=INK)
    by = hy + 36
    for j, ln in enumerate(wrap2(body, F(SANS, 11), HERO_W)):
        text(x0, by + j * 13, ln, F(SANS, 11), fill=(50, 50, 50))
    # source + chip row, kept clear of the black bar below (bar starts y424)
    sy = HERO_Y + SCENE_H + 94
    text(x0, sy + 1, src, F(SANS, 9), fill=GREY)
    chip(x0 + 150, sy, "REPORTED")

# black divider bar
d.rectangle([0, 424, W, 442], fill=INK)
text(12, 428, "MORE OF THE DAY", F(SANS_B, 11), fill=(255, 255, 255))
text(1012, 428, "10 STORIES", F(SANS_B, 10), fill=GOLD, anchor="ra")

# ---------------------------------------------------------------- 10 cards
CARDS = [
    ("BESSENT DEMANDS NVIDIA ANSWERS", "Treasury chief presses chipmaker over China sales.", "AP", False),
    ("FBI PROBES NCIC HACK", "Police-database breach under investigation.", "REUTERS", False),
    ("TRUMP: IRAN STRIKES MAY RESUME", "US president warns of action in the New Year.", "AP", False),
    ("NASDAQ FUTURES +3%", "Holiday week opens higher on tech hopes.", "BLOOMBERG", False),
    ("SKUBAL SIGNS $450M METS DEAL", "Two-time Cy Young winner, nine-year pact.", "AP", False),
    ("TOM JACKSON DIES AT 75", "Former NFL linebacker and broadcaster.", "AP", False),
    ("STATES SUE SPACEX", "AI safety claims challenged in court.", "REUTERS", False),
    ("ANTHROPIC IPO AT $107.3B", "Raised at $83/share; debut close $97.17.", "BLOOMBERG", False),
    ("POLAND: RUSSIAN MISSILES CROSSED AIRSPACE", "Warsaw says 3 Kh-101s entered its skies.", "REUTERS", True),
    ("INTEL WARNS OF RUSSIAN NUCLEAR SATELLITE", "US assessment flags orbital weapon risk.", "AP", True),
]
CARD_Y, CARD_H, CARD_W = 448, 46, 500
for i, (head, body, src, claim) in enumerate(CARDS):
    col, row = i % 2, i // 2
    x0 = 12 + col * 500
    y0 = CARD_Y + row * 48
    d.rectangle([x0, y0, x0 + CARD_W - 4, y0 + CARD_H], fill=CARD_BG,
                outline=RULE, width=1)
    text(x0 + 8, y0 + 4, fit(head, F(SANS_B, 11), CARD_W - 20), F(SANS_B, 11), fill=INK)
    text(x0 + 8, y0 + 19, fit(body, F(SANS, 10), CARD_W - 20), F(SANS, 10), fill=(60, 60, 60))
    text(x0 + 8, y0 + 33, src, F(SANS, 8), fill=GREY)
    chip(x0 + 60, y0 + 32, "CLAIM" if claim else "REPORTED", claim=claim)

# ---------------------------------------------------------------- map + ALSO
MAP_Y = 700
d.rectangle([12, MAP_Y, 508, MAP_Y + 176], fill=(232, 238, 244), outline=RULE, width=1)
text(20, MAP_Y + 4, "THE WORLD IN 13 PINS", F(SANS_B, 11), fill=INK)
# stylised blobs (Americas left, Eurasia centre-right, Africa lower-right)
d.ellipse([40, MAP_Y + 40, 150, MAP_Y + 150], fill=(190, 205, 190))          # Americas
d.ellipse([200, MAP_Y + 30, 420, MAP_Y + 120], fill=(190, 205, 190))         # Eurasia
d.ellipse([300, MAP_Y + 110, 380, MAP_Y + 168], fill=(190, 205, 190))        # Africa
PINS = [
    (1, "Seoul", 400, MAP_Y + 62), (2, "Bridgetown", 96, MAP_Y + 128),
    (3, "Washington", 82, MAP_Y + 72), (4, "Paris", 268, MAP_Y + 66),
    (5, "London", 244, MAP_Y + 60), (6, "Manchester", 220, MAP_Y + 62),
    (7, "Warsaw", 292, MAP_Y + 52), (8, "Kyiv", 322, MAP_Y + 56),
    (9, "Beirut", 334, MAP_Y + 84), (10, "Gaza", 312, MAP_Y + 102),
    (11, "Bahrain", 356, MAP_Y + 92), (12, "Khartoum", 334, MAP_Y + 122),
    (13, "Kinshasa", 316, MAP_Y + 144),
]
for n, name, px, py in PINS:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
    d.text((px, py - 1), str(n), font=F(SANS_B, 8), fill=(255, 255, 255), anchor="mm")
# legend, compact block at the bottom of the map panel
d.rectangle([12, MAP_Y + 154, 508, MAP_Y + 176], fill=(232, 238, 244))
text(20, MAP_Y + 156, "1 Seoul · 2 Bridgetown · 3 Washington · 4 Paris · 5 London · 6 Manchester",
     F(SANS, 8), fill=GREY)
text(20, MAP_Y + 167, "7 Warsaw · 8 Kyiv · 9 Beirut · 10 Gaza · 11 Bahrain · 12 Khartoum · 13 Kinshasa",
     F(SANS, 8), fill=GREY)

# ALSO list, right column, 2 columns x 9 rows
text(524, MAP_Y + 4, "ALSO ON MONDAY", F(SANS_B, 11), fill=INK)
ALSO = [
    "Paris: 100+ back 2% billionaire tax",
    "Manchester: 12,000 cleared",
    "Zelenskyy: 165 missiles in a week",
    "COP31: day after Antalya pact",
    "Israel unity talks resume",
    "Gaza: two killed in Israeli strike",
    "West Bank settler attacks",
    "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives",
    "Bahrain Sat: strike hits plant, 2 hurt",
    "Benghazi: UN probe demand [CLAIM]",
    "Sudan: drones downed [CLAIM]",
    "DRC: fighting traps Ebola teams",
    "Bangladesh: Hasina jailed if returns",
    "Seoul minister quits over AI exam",
    "SK Telecom −7.3%",
    "China eases margin rules to 80%",
    "Seoul readies 10T-won fund",
]
for i, item in enumerate(ALSO):
    col, row = i // 9, i % 9
    x0 = 524 + col * 244
    y0 = MAP_Y + 24 + row * 17
    d.text((x0, y0), "·", font=F(SANS_B, 10), fill=RED)
    text(x0 + 10, y0, fit(item, F(SANS, 9), 228), F(SANS, 9), fill=INK)

# ---------------------------------------------------------------- DATE CHECK
DC_Y = 884
d.rectangle([12, DC_Y, 1012, DC_Y + 98], fill=(255, 235, 235), outline=RED, width=2)
text(20, DC_Y + 5, "DATE CHECK — NOT 23 NOVEMBER", F(SANS_B, 11), fill=RED)
LEFT_OUT = ["Democrats reach 258 (22 Nov)", "Sparta II fire (22 Nov)",
            "El Chapo Isidro captured (22 Nov)", "EU–Indonesia pact (21 Nov)",
            "Nigeria boat (21 Nov)", "ICJ Myanmar ruling (19 Nov)"]
text(20, DC_Y + 21, "LEFT OUT:", F(SANS_B, 9), fill=RED)
for i, item in enumerate(LEFT_OUT):
    col, row = i % 3, i // 3
    x0 = 20 + col * 330
    y0 = DC_Y + 34 + row * 12
    text(x0, y0, "✕ " + item, F(SANS, 9), fill=INK)
text(20, DC_Y + 60, "NOT YET:", F(SANS_B, 9), fill=RED)
NOT_YET = ["Dymer search continues (14 missing)", "4 House races uncalled",
           "COP32 venue not set", "WHO evacuating trapped Ebola staff"]
for i, item in enumerate(NOT_YET):
    col, row = i % 2, i // 2
    x0 = 20 + col * 480
    y0 = DC_Y + 72 + row * 12
    text(x0, y0, "… " + item, F(SANS, 9), fill=INK)

# ---------------------------------------------------------------- footer
text(12, 988, "SOURCES: AP · REUTERS · BLOOMBERG · YONHAP · Lowy Institute Asia Power Index 2026",
     F(SANS, 8), fill=GREY)
text(12, 1000, "REPORTED = confirmed by wires  ·  CLAIM = one side's claim  ·  All stories dated Monday 23 November 2026",
     F(SANS, 8), fill=GREY)
text(1012, 988, "THE WORLD TODAY", F(SANS_B, 8), fill=GREY, anchor="ra")

img.save(OUT, optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
