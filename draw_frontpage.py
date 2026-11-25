"""Draw the News Image 20261124 v2 front page.

A single 1024x1024 PNG summing up Tuesday 24 November 2026: three big
illustrated leads, a stats band, a world map strip, and 33 one-line briefs
across six regions (36 stories in total). DejaVu fonts only, with a
resilient fallback chain. Deterministic: same input bytes every run.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (20, 20, 20)
NAVY = (22, 50, 79)
RED = (179, 38, 30)
GOLD = (201, 162, 39)
TEAL = (38, 110, 128)
SEA = (72, 143, 168)
SAND = (232, 214, 176)
CARD = (255, 255, 255)
RULE = (216, 210, 196)
MUTED = (90, 86, 76)
MAP_BG = (228, 237, 243)
LAND = (169, 190, 205)

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
]


def font(name, size):
    for path in FONT_DIRS:
        if name in path:
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def sans_b(size):
    return font("DejaVuSans-Bold", size)


def sans(size):
    return font("DejaVuSans", size)


def serif_b(size):
    return font("DejaVuSerif-Bold", size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def centre(draw, x0, x1, y, s, f, fill):
    w = text_w(draw, s, f)
    draw.text(((x0 + x1 - w) / 2, y), s, font=f, fill=fill)


def wrap(draw, s, f, max_w):
    words = s.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def rrect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# --- verified story set: 3 leads + 33 briefs = 36 stories, 6 regions ---

LEADS = [
    {
        "tag": "LIBYA  ·  BENGHAZI",
        "kind": "warship",
        "headline": "UKRAINE SINKS RUSSIAN WARSHIP",
        "summary": "Seven naval drones sank the corvette Merkury off Benghazi.",
    },
    {
        "tag": "TECH  ·  NVIDIA",
        "kind": "chip",
        "headline": "HUANG RETURNS AS NVIDIA CHIEF",
        "summary": "Shares jump 31% as Jensen Huang retakes the top job.",
    },
    {
        "tag": "STRAIT OF HORMUZ",
        "kind": "tankers",
        "headline": "THREE TANKERS HIT MINES IN HORMUZ",
        "summary": "Iran says three tankers struck mines in the Strait.",
    },
]

STATS = [
    ("96", "DRONES"),
    ("700,000", "RUSSIAN DEAD"),
    ("31%", "NVIDIA SHARES"),
    ("26", "FACTORY-FIRE DEAD"),
    ("7", "NAVAL DRONES"),
    ("3", "TANKERS HIT"),
]

REGIONS = [
    ("EUROPE", [
        "Russia warns Estonia its actions risk open war",
        "EU unveils new sanctions on banks and shadow fleet",
        "Burnham: no EU return without a referendum",
        "Hungary's PM to meet Zelenskyy in western Ukraine",
        "Britain warns firms aiding Ukraine of sabotage",
        "NATO vows to defend space amid nuclear fears",
    ]),
    ("MIDDLE EAST", [
        "Gaza strike kills Hamas security chief, six others",
        "Iran sets seven conditions before any US talks",
        "Netanyahu urges Trump to resume strikes on Iran",
        "Vance and Rubio meet Qatar's PM in Washington",
        "Trump warns Iran of a 'very traumatic' outcome",
        "Eleven die in coach-truck crash in Ras el-Khaimah",
    ]),
    ("ASIA-PACIFIC", [
        "Solomon Islands to end its security pact with China",
        "UK sanctions Myanmar generals after genocide ruling",
        "Malaysia to send 6,500 Rohingya back to Myanmar",
        "Quake of 5.6 strikes Nepal near the China border",
        "Pakistani astronaut to join China's space station",
        "South Korea scrambles jets as Russian planes near",
    ]),
    ("AMERICAS", [
        "Car bomb wrecks buildings in Villavicencio, Colombia",
        "Mexico to try 'El Chapo Isidro' despite US request",
        "Pennsylvania measles outbreak claims ninth death",
        "Trump: China plans to buy more Boeing planes",
        "Watchdog: ICE cut new-officer training too far",
    ]),
    ("AFRICA", [
        "Borno school enrolment nearly doubles after conflict",
        "Two Nigerians die while serving in Russian military",
        "Tripoli denies any deal with Kyiv over Benghazi",
        "Erdogan plans first Libya trip in over a decade",
        "Analysts: Libya strike takes the war to Africa",
    ]),
    ("TECH & MARKETS", [
        "Singapore vows action in Nvidia chip-diversion case",
        "US targets seven firms over chip diversion to China",
        "UN chief wants AI-risk rules agreed within a year",
        "SpaceX outages shake confidence across Europe",
        "Asian markets rally after Huang's return",
    ]),
]

NORTH_AMERICA = [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80),
                 (-85, 70), (-75, 62), (-65, 60), (-55, 52), (-60, 46),
                 (-70, 42), (-75, 35), (-80, 26), (-85, 20), (-90, 15),
                 (-95, 16), (-100, 20), (-105, 22), (-115, 28), (-125, 40),
                 (-125, 48), (-140, 60), (-155, 58), (-165, 60)]
SOUTH_AMERICA = [(-80, 10), (-75, 12), (-70, 12), (-62, 10), (-52, 5),
                 (-50, 0), (-42, -5), (-35, -8), (-40, -20), (-48, -28),
                 (-55, -35), (-65, -40), (-70, -50), (-73, -53), (-70, -40),
                 (-72, -20), (-78, -5), (-80, 2)]
EUROPE = [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (5, 53),
          (8, 57), (10, 59), (18, 56), (21, 55), (24, 58), (28, 60),
          (30, 62), (32, 60), (28, 55), (24, 52), (20, 50), (16, 46),
          (14, 42), (12, 44), (8, 44), (3, 42), (0, 38), (-6, 36)]
AFRICA = [(-6, 35), (-10, 31), (-15, 27), (-17, 20), (-17, 15), (-12, 8),
          (-8, 5), (-4, 5), (6, 4), (9, 4), (12, -2), (13, -10),
          (12, -18), (16, -28), (20, -35), (28, -33), (32, -28),
          (35, -20), (40, -15), (42, -10), (46, -2), (51, 2), (51, 10),
          (48, 11), (44, 12), (40, 15), (38, 18), (35, 22), (32, 28),
          (30, 31), (22, 33), (15, 32), (10, 34)]
ASIA = [(30, 62), (40, 68), (50, 70), (60, 70), (70, 72), (80, 73),
        (90, 75), (100, 76), (110, 76), (120, 73), (130, 72), (140, 72),
        (150, 70), (158, 66), (162, 60), (158, 55), (150, 60), (142, 55),
        (140, 45), (135, 43), (130, 38), (127, 35), (122, 30), (120, 25),
        (115, 22), (110, 20), (105, 10), (100, 8), (98, 12), (95, 16),
        (92, 20), (88, 22), (85, 20), (80, 15), (77, 8), (75, 12),
        (72, 20), (68, 22), (62, 25), (58, 26), (55, 26), (52, 28),
        (50, 30), (48, 30), (44, 29), (42, 28), (40, 30), (38, 32),
        (36, 36), (33, 38), (30, 40), (28, 42), (28, 45), (30, 48),
        (32, 52), (35, 55), (38, 58)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
             (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
             (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)]

CONTINENTS = [NORTH_AMERICA, SOUTH_AMERICA, EUROPE, AFRICA, ASIA, AUSTRALIA]

PINS = [
    ("BENGHAZI", 20.1, 32.1, "right"),
    ("HORMUZ", 56.5, 26.5, "below"),
    ("KYIV", 30.5, 50.4, "above"),
    ("TAIPEI", 121.5, 25.0, "right"),
    ("WASHINGTON", -77.0, 38.9, "left"),
    ("BEIJING", 116.4, 39.9, "above"),
]


def draw_warship(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(196, 222, 232))
    draw.rectangle([x0, y0 + 92, x0 + w, y0 + h], fill=SEA)
    for i in range(5):
        yy = y0 + 108 + i * 11
        draw.arc([x0 + 8, yy, x0 + w - 8, yy + 16], 180, 360, fill=(255, 255, 255), width=2)
    hull = [(x0 + 52, y0 + 96), (x0 + 268, y0 + 96), (x0 + 250, y0 + 128),
            (x0 + 70, y0 + 128)]
    draw.polygon(hull, fill=(52, 58, 64))
    draw.rectangle([x0 + 130, y0 + 66, x0 + 185, y0 + 96], fill=(72, 78, 84))
    draw.rectangle([x0 + 200, y0 + 76, x0 + 212, y0 + 96], fill=(52, 58, 64))
    draw.line([x0 + 158, y0 + 66, x0 + 158, y0 + 44], fill=(52, 58, 64), width=3)
    for cx, cy, r in [(x0 + 205, y0 + 58, 9), (x0 + 218, y0 + 48, 12), (x0 + 232, y0 + 36, 15)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 120, 118))
    for i, (dx, dy) in enumerate([(36, 26), (78, 14), (120, 30), (168, 10),
                                 (216, 24), (258, 12), (296, 28)]):
        draw.ellipse([x0 + dx - 3, y0 + dy - 3, x0 + dx + 3, y0 + dy + 3], fill=INK)
        draw.line([x0 + dx, y0 + dy + 3, x0 + dx - 14, y0 + dy + 22],
                  fill=(255, 255, 255), width=1)
    for bx, by, s in [(x0 + 96, y0 + 88, 16), (x0 + 112, y0 + 76, 11), (x0 + 84, y0 + 74, 9)]:
        draw.regular_polygon((bx, by, s), 8, fill=(255, 176, 32),
                             outline=(179, 38, 30), width=2)


def draw_chip(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 32, 46))
    for gy in range(y0 + 12, y0 + h, 26):
        draw.line([x0, gy, x0 + w, gy], fill=(28, 58, 74), width=1)
    for gx in range(x0 + 12, x0 + w, 26):
        draw.line([gx, y0, gx, y0 + h], fill=(28, 58, 74), width=1)
    cx, cy = x0 + 108, y0 + 82
    for px in range(cx - 44, cx + 45, 22):
        draw.line([px, cy - 44, px, cy - 58], fill=GOLD, width=3)
        draw.line([px, cy + 44, px, cy + 58], fill=GOLD, width=3)
    for py in range(cy - 44, cy + 45, 22):
        draw.line([cx - 44, py, cx - 58, py], fill=GOLD, width=3)
        draw.line([cx + 44, py, cx + 58, py], fill=GOLD, width=3)
    draw.rectangle([cx - 44, cy - 44, cx + 44, cy + 44], fill=(24, 52, 38),
                   outline=GOLD, width=3)
    draw.rectangle([cx - 20, cy - 20, cx + 20, cy + 20], fill=GOLD)
    pts = [(x0 + 205, y0 + 128), (x0 + 235, y0 + 104), (x0 + 258, y0 + 112),
           (x0 + 288, y0 + 74), (x0 + 308, y0 + 52)]
    draw.line(pts, fill=(255, 255, 255), width=4, joint="curve")
    draw.polygon([(x0 + 308, y0 + 52), (x0 + 296, y0 + 54), (x0 + 306, y0 + 66)],
                 fill=(255, 255, 255))
    f = sans_b(30)
    draw.text((x0 + 208, y0 + 14), "+31%", font=f, fill=(120, 220, 130))


def draw_tankers(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(238, 226, 200))
    draw.rectangle([x0, y0 + 62, x0 + w, y0 + h], fill=TEAL)
    for i in range(4):
        yy = y0 + 78 + i * 18
        draw.arc([x0 + 10, yy, x0 + w - 10, yy + 14], 180, 360,
                 fill=(255, 255, 255), width=2)
    for tx, tw in [(28, 96), (140, 108), (238, 72)]:
        ty = y0 + 84
        draw.polygon([(x0 + tx, ty), (x0 + tx + tw, ty),
                      (x0 + tx + tw - 10, ty + 18), (x0 + tx + 10, ty + 18)],
                     fill=(30, 30, 30))
        draw.rectangle([x0 + tx + tw - 26, ty - 16, x0 + tx + tw - 8, ty],
                       fill=(245, 245, 245))
    for mx, my in [(x0 + 128, y0 + 118), (x0 + 232, y0 + 126), (x0 + 66, y0 + 130)]:
        for k in range(8):
            ang = k * 3.14159 / 4
            x1 = mx + 10 * __import__("math").cos(ang)
            y1 = my + 10 * __import__("math").sin(ang)
            x2 = mx + 16 * __import__("math").cos(ang)
            y2 = my + 16 * __import__("math").sin(ang)
            draw.line([x1, y1, x2, y2], fill=INK, width=2)
        draw.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=INK)
    tri = [(x0 + 268, y0 + 18), (x0 + 296, y0 + 58), (x0 + 240, y0 + 58)]
    draw.polygon(tri, fill=(255, 176, 32), outline=RED, width=2)
    draw.text((x0 + 264, y0 + 30), "!", font=sans_b(22), fill=RED)


ILLUSTRATORS = {"warship": draw_warship, "chip": draw_chip, "tankers": draw_tankers}


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead
    centre(draw, 0, W, 12, "MAKE.FUN  ·  WORLD NEWS IN ONE IMAGE", sans_b(13), NAVY)
    centre(draw, 0, W, 24, "THE WORLD IN ONE DAY", serif_b(46), INK)
    centre(draw, 0, W, 78, "TUESDAY  24  NOVEMBER  2026", sans_b(23), RED)
    draw.line([16, 98, 1008, 98], fill=INK, width=2)

    # Stats band
    rrect(draw, [16, 104, 1008, 164], 8, fill=NAVY)
    cell_w = 992 / 6
    for i, (num, label) in enumerate(STATS):
        cx0 = 16 + i * cell_w
        if i:
            draw.line([cx0, 114, cx0, 156], fill=(90, 120, 150), width=1)
        centre(draw, cx0, cx0 + cell_w, 112, num, sans_b(30), (255, 255, 255))
        centre(draw, cx0, cx0 + cell_w, 146, label, sans_b(11), (255, 217, 160))

    # Three leads
    for i, lead in enumerate(LEADS):
        x0 = 16 + i * 336
        x1 = x0 + 320
        draw.rectangle([x0, 172, x1, 492], fill=CARD, outline=RULE, width=1)
        ILLUSTRATORS[lead["kind"]](draw, x0, 172, 320, 150)
        tag_f = sans_b(11)
        tw = text_w(draw, lead["tag"], tag_f)
        rrect(draw, [x0 + 10, 300, x0 + 22 + tw, 322], 4, fill=RED)
        draw.text((x0 + 16, 305), lead["tag"], font=tag_f, fill=(255, 255, 255))
        lines = wrap(draw, lead["headline"], sans_b(24), 296)
        assert len(lines) <= 3, lead["headline"]
        y = 332
        for line in lines:
            draw.text((x0 + 12, y), line, font=sans_b(24), fill=INK)
            y += 29
        slines = wrap(draw, lead["summary"], sans(15), 296)
        assert len(slines) <= 2, lead["summary"]
        y = 332 + 3 * 29 + 8
        for line in slines:
            draw.text((x0 + 12, y), line, font=sans(15), fill=MUTED)
            y += 20

    # World map strip
    draw.rectangle([16, 500, 1008, 640], fill=MAP_BG, outline=RULE, width=1)
    draw.text((28, 506), "WHERE THE DAY HAPPENED", font=sans_b(13), fill=NAVY)
    right = "6 REGIONS  ·  36 STORIES"
    draw.text((1008 - 12 - text_w(draw, right, sans_b(12)), 507), right,
              font=sans_b(12), fill=MUTED)

    def proj(lon, lat):
        return (24 + (lon + 170) / 360 * 976, 528 + (75 - lat) / 130 * 106)

    for poly in CONTINENTS:
        draw.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
                     outline=(120, 140, 155))
    lab_f = sans_b(12)
    for name, lon, lat, side in PINS:
        px, py = proj(lon, lat)
        draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                     outline=(255, 255, 255), width=2)
        lw = text_w(draw, name, lab_f)
        if side == "right":
            lx, ly = px + 9, py - 6
        elif side == "left":
            lx, ly = px - 9 - lw, py - 6
        elif side == "above":
            lx, ly = px - lw / 2, py - 20
        else:
            lx, ly = px - lw / 2, py + 9
        draw.text((lx, ly), name, font=lab_f, fill=INK)

    # Region briefs: 2 columns x 3 rows
    brief_f = sans(12)
    head_f = sans_b(15)
    for idx, (region, briefs) in enumerate(REGIONS):
        col, row = idx % 2, idx // 2
        bx = 16 + col * 504
        by = 648 + row * 120
        draw.text((bx, by), region, font=head_f, fill=NAVY)
        n = f"({len(briefs)})"
        draw.text((bx + text_w(draw, region, head_f) + 8, by + 2), n,
                  font=sans_b(12), fill=RED)
        draw.line([bx, by + 22, bx + 488, by + 22], fill=RED, width=2)
        y = by + 26
        for brief in briefs:
            assert text_w(draw, brief, brief_f) <= 464, brief
            draw.rectangle([bx, y + 4, bx + 7, y + 11], fill=RED)
            draw.text((bx + 14, y), brief, font=brief_f, fill=INK)
            y += 15

    centre(draw, 0, W, 1010,
           "36 stories  ·  6 regions  —  every event above happened or was "
           "first reported on Tuesday 24 November 2026",
           sans(11), MUTED)
    return img


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    build().save(os.path.join(here, "entry.png"), "PNG")
    print("wrote entry.png")
