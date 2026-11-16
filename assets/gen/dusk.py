#!/usr/bin/env python3
"""dusk.svg: a desk under a window at blue hour. The strait and the bridge
outside, a cat on the sill, tea going cold next to the keyboard.

Same method as overworld.py: flat "daylight" colours, then a banded light map.
No dependencies.  python3 assets/gen/dusk.py
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from px import Canvas, svg, hexrgb, rgbhex, mix

W, H = 256, 100
O = "#2b1d2e"
CREAM, PAPER = "#f4ecd8", "#fbf6ea"
WOOD, WOOD_D, WOOD_L = "#8a5a3a", "#6b4630", "#c08a5c"
GREY, GREY_D, GREY_L = "#6f6a85", "#55506a", "#d8d4c8"
E = True

cv = Canvas(W, H, "#cfb9a0")
for x, y in ((8, 70), (140, 70), (201, 62), (250, 58), (136, 20), (3, 30), (198, 30), (252, 8), (130, 44)):
    cv.rect(x, y, 2, 1, "#c4ad94")

def shade(x, y, w, h, t=.3):
    for j in range(y, y + h):
        for i in range(x, x + w):
            c = cv.get(i, j)
            if c and not cv.e[j][i]: cv.px(i, j, rgbhex(mix(hexrgb(c), hexrgb(O), t)))

# ------------------------------------------------------------ the view
X0, X1, Y0, Y1, HZ = 18, 122, 8, 58, 42
cv.box(X0 - 2, Y0 - 2, X1 - X0 + 4, Y1 - Y0 + 4, CREAM, O)
SKY = ["#10133a", "#161b4e", "#1f2566", "#2f2d7c", "#4b3689", "#7a4390", "#b5557f", "#e07a6a", "#f2a65a"]
rows = HZ - Y0
for y in range(Y0, HZ):
    f = (y - Y0) / rows * len(SKY)
    n = min(int(f), len(SKY) - 1)
    for x in range(X0, X1):
        c = SKY[n]
        if n + 1 < len(SKY) and f - n > .72 and (x + y) % 2 == 0: c = SKY[n + 1]
        cv.px(x, y, c, E)
SEA = ["#6a3f84", "#45327a", "#2f2a68", "#232056", "#1b1946"]
for y in range(HZ, Y1):
    n = min((y - HZ) // 3, len(SEA) - 1)
    for x in range(X0, X1):
        c = SEA[n]
        if (y - HZ) % 3 == 2 and n + 1 < len(SEA) and (x + y) % 2: c = SEA[n + 1]
        cv.px(x, y, c, E)
for x, y, w in ((60, 43, 16), (64, 44, 9), (56, 45, 5), (70, 45, 7), (66, 47, 5), (62, 49, 3), (72, 50, 4), (67, 52, 2)):
    cv.rect(x, y, w, 1, "#f2a65a" if y < 45 else "#e07a6a" if y < 49 else "#b5557f", E)
STARS = ((22, 10), (31, 14), (40, 9), (47, 17), (58, 11), (66, 15), (77, 9), (84, 18), (90, 12), (108, 10),
         (115, 16), (27, 21), (112, 23), (73, 21), (36, 25))
for n, (x, y) in enumerate(STARS):
    cv.px(x, y, "#fff3c4" if n % 3 == 0 else "#aab4f0", E)
cv.blit(98, 12, ["..mmm.", ".mm...", "mm....", "mm....", "mm....", ".mm...", "..mmm."], {"m": "#fff3c4"}, emit="m")
# far shore
HILL = "1112223332211122334443322111222233322110011122233332221111222333444332211122233322111122233222111122221111"
for i, ch in enumerate(HILL[:X1 - X0]):
    h = int(ch)
    cv.rect(X0 + i, HZ - h, 1, h, "#2a2060", E)
for x, y in ((24, 41), (29, 40), (37, 41), (44, 39), (81, 40), (86, 41), (103, 40), (110, 39), (117, 41), (48, 41)):
    cv.px(x, y, "#ffd86b", E)
# bridge
BR = "#15123a"
T1, T2, TOP, DECK = 46, 99, 22, 39
for x in range(X0, X1):
    if T1 <= x <= T2:
        m = (T1 + T2) / 2
        y = (DECK - 2) - (DECK - 2 - TOP) * ((x - m) / (m - T1)) ** 2
    elif x < T1: y = TOP + (DECK - 1 - TOP) * (T1 - x) / (T1 - X0 + 6)
    else: y = TOP + (DECK - 1 - TOP) * (x - T2) / (X1 - T2 + 6)
    y = round(y)
    cv.px(x, y, "#6a5aa0", E)
    if x % 4 == 0:
        for yy in range(y + 1, DECK):
            if (yy + x // 4) % 2: cv.px(x, yy, "#4b3f86", E)
for tx in (T1, T2):
    cv.rect(tx, TOP - 1, 2, HZ - TOP + 4, BR, E); cv.rect(tx - 1, HZ + 2, 4, 2, BR, E)
    cv.rect(tx, TOP + 5, 2, 1, "#6a5aa0", E)
cv.rect(X0, DECK, X1 - X0, 2, BR, E)
for x in range(X0 + 1, X1, 3):
    cv.px(x, DECK, "#ffd86b", E)
    if x % 2: cv.px(x, HZ + 3 + (x % 5), "#c98a4a", E)
# near roofs, a dome and its minarets
NR = "#0f0d2a"
for x, w, h in ((18, 9, 5), (27, 5, 3), (50, 12, 6), (62, 7, 4), (69, 10, 7), (79, 8, 4), (87, 12, 6), (99, 6, 3), (105, 10, 8), (115, 7, 5)):
    cv.rect(x, Y1 - h, w, h, NR, E)
cv.blit(76, 45, [
    ".m...............m.",
    ".m...............m.",
    ".m.......d.......m.",
    "mmm.....ddd.....mmm",
    ".m....ddddddd...m..",
    ".m...ddddddddd..m..",
    ".m..ddddddddddd.m..",
    ".m.ddddddddddddd.m.",
    ".mddddddddddddddd.m",
    ".mdddddddddddddddm.",
    ".mdddddddddddddddm.",
    ".mdddddddddddddddm.",
    ".mdddddddddddddddm.",
], {"m": NR, "d": NR}, emit="md")
for x, y in ((20, 55), (23, 55), (53, 54), (57, 56), (72, 53), (75, 55), (90, 54), (95, 56), (108, 52), (111, 55), (118, 55), (65, 56), (38, 55), (42, 55)):
    cv.px(x, y, "#ffd86b" if (x + y) % 3 else "#ffb35c", E)
# mullions, sill
cv.rect(69, Y0, 2, Y1 - Y0, CREAM); cv.rect(X0, 31, X1 - X0, 2, CREAM)
cv.rect(69, Y0, 1, Y1 - Y0, "#cfc2b0")
cv.rect(11, 60, 118, 3, CREAM); cv.rect(11, 60, 118, 1, PAPER); cv.rect(11, 63, 118, 1, O)
shade(14, 64, 112, 2, .2)
# curtains
cv.rect(3, 2, 134, 2, GREY_D); cv.rect(2, 1, 2, 4, GREY); cv.rect(136, 1, 2, 4, GREY)
for x0 in (5, 123):
    for i in range(12):
        col = ("#b5573a", "#c96a48", "#b5573a", "#8f3f2a")[i % 4]
        cv.rect(x0 + i, 4, 1, 64 + (1 if i % 4 == 1 else 0), col)
    cv.rect(x0 - 1, 4, 1, 64, O); cv.rect(x0 + 12, 4, 1, 64, O); cv.rect(x0, 68, 12, 1, O)
    for i in range(0, 12, 3): cv.px(x0 + i + 1, 4, "#ffd86b")

# ------------------------------------------------------------ on the sill
CATX = 30
cv.blit(CATX, 43, [
    "..o.......o.....",
    ".oLo.....oko....",
    ".oLkoooookko....",
    ".oLkkkkkkkko....",
    ".oLkkkkkkkko....",
    ".oLkkkkkkkko....",
    "..okkkkkkko.....",
    "..oLkkkkkko.....",
    ".oLkkkkkkkko....",
    ".oLkkkkkkkkko...",
    "oLkkkkkkkkkko...",
    "oLkkkkkkkkkkko..",
    "oLkkkkkkkkkkko..",
    "oLkkkkkkkkkkko..",
    "oLkkkkkkkkkkko..",
    "okkkkkkkkkkkko..",
    ".oooooooooooo...",
], {"o": "#15102a", "k": "#2a2244", "L": "#8f9fe0"}, emit="okL")
cv.blit(102, 47, [
    "...g.....",
    "..gGg....",
    "..gGg.g..",
    "g.gGggGg.",
    "gGgGggGg.",
    ".ggGgGg..",
    "...Gg....",
    ".ooooooo.",
    ".opPpppo.",
    ".opppppo.",
    "..opppo..",
    "..ooooo..",
    "..ooooo..",
], {"g": "#2a6a45", "G": "#4f9f5a", "o": O, "p": "#b5573a", "P": "#d98a66"})

# ------------------------------------------------------------ wall, right
BULBS = []
for x in range(138, W):
    y = 4 + round(2.6 * math.sin(((x - 138) % 30) / 30 * math.pi))
    cv.px(x, y, "#5a4a4a")
    if (x - 138) % 15 == 7:
        col = ("#ffd86b", "#ff8fa3", "#7fe0d0", "#ffb35c")[((x - 138) // 15) % 4]
        cv.px(x, y + 1, "#5a4a4a"); cv.rect(x - 1, y + 2, 3, 2, col, E); cv.px(x, y + 4, col, E)
        BULBS.append((x, y + 3))
# photos on a string
for x in range(142, 196): cv.px(x, 14 + round(1.6 * math.sin((x - 142) / 54 * math.pi)), "#8a7a6a")
for n, (x, a, b) in enumerate(((146, "#7fb0d8", "#3f8f4f"), (160, "#f2a65a", "#6a3f7c"), (174, "#ff8fa3", "#3d6fb8"), (186, "#7fe0d0", "#e8a03c"))):
    y = 16 + (n in (1, 2))
    cv.box(x, y, 9, 10, PAPER, "#b9ad9c")
    cv.rect(x + 1, y + 1, 7, 6, a); cv.rect(x + 1, y + 5, 7, 2, b); cv.px(x + 3 + n, y + 4, b)
    cv.px(x + 4, y - 1, "#c8434b")
# shelf
cv.rect(202, 28, 52, 2, WOOD_L); cv.rect(202, 30, 52, 1, WOOD_D)
cv.rect(206, 31, 1, 3, WOOD_D); cv.rect(249, 31, 1, 3, WOOD_D)
x = 205
for col, w, h in (("#c8434b", 3, 11), ("#3d6fb8", 2, 9), ("#f4ecd8", 3, 12), ("#3f7f7a", 3, 10), ("#e8a03c", 2, 11), ("#a25a8c", 3, 9), ("#3d6fb8", 3, 12)):
    cv.rect(x, 28 - h, w, h, col); cv.rect(x + w - 1, 28 - h, 1, h, rgbhex(mix(hexrgb(col), hexrgb(O), .35)))
    if w > 2: cv.rect(x, 31 - h, 2, 1, CREAM)
    x += w
cv.box(226, 23, 9, 5, "#e8a03c", O); cv.box(227, 19, 7, 5, "#3f7f7a", O)       # two lying flat
cv.blit(238, 19, ["ooooooooo", "opPpppppo", "opppppppo", ".opppppo.", ".ooooooo."], {"o": O, "p": "#b5573a", "P": "#d98a66"})
cv.blit(236, 11, [
    "...g..gg.....",
    "..gGg.gGg..g.",
    ".gGgggGg..gGg",
    "..gggGgg.gGg.",
    "...ggggggGg..",
    "....gggggg...",
    "g....ggg..g..",
    "Gg...dg..gGg.",
], {"g": "#3f8f4f", "G": "#7cc46a", "d": "#2a6a45"})
cv.blit(246, 24, [
    "..d....",
    ".gd....",
    "gGd.gg.",
    ".gd.gGg",
    "..d..d.",
    ".gd..d.",
    "gGd.gd.",
    ".gd.Ggd",
    "..dg.d.",
    "..Gg.d.",
    "..d.gd.",
    ".gd.Gg.",
    "gGd....",
    ".g.....",
], {"g": "#3f8f4f", "G": "#7cc46a", "d": "#2a6a45"})

# ------------------------------------------------------------ desk
cv.rect(0, 76, W, 5, WOOD_L); cv.rect(0, 76, W, 1, "#dba878"); cv.rect(0, 75, W, 1, O)
cv.rect(0, 81, W, 2, WOOD); cv.rect(0, 83, W, 1, O)
cv.rect(0, 84, W, 16, WOOD_D)
for x0 in (150, 202):
    cv.box(x0, 86, 48, 12, WOOD, O); cv.rect(x0 + 1, 87, 46, 1, "#a06c44"); cv.rect(x0 + 20, 91, 8, 2, "#ffd86b"); cv.rect(x0 + 20, 93, 8, 1, O)
cv.rect(0, 84, 146, 16, "#4a3030"); cv.rect(142, 84, 4, 16, WOOD_D); cv.rect(146, 84, 1, 16, O)
for x in range(20, 140, 37): cv.rect(x, 84, 1, 16, "#3f2a2c")

# monitor
cv.rect(163, 66, 8, 9, GREY_D); cv.rect(164, 66, 2, 9, GREY)
cv.rect(153, 75, 28, 2, GREY); cv.rect(153, 77, 28, 1, GREY_D)
cv.box(138, 27, 58, 40, "#3a3550", O); cv.rect(139, 28, 56, 1, "#55506a")
cv.rect(141, 30, 52, 31, "#0f1626", E)
cv.px(167, 64, "#7cc46a", E)
KW, FN, TX, ST, CM, NUM = "#ff8fa3", "#7fe0d0", "#d8d4c8", "#ffd86b", "#6f6a85", "#ffb35c"
CODE = [
    (0, [(2, KW), (6, FN), (1, TX), (5, ST), (1, TX)]),
    (2, [(3, KW), (4, TX), (1, TX), (9, FN)]),
    (2, [(3, KW), (3, TX), (1, TX), (3, NUM)]),
    (2, [(5, KW), (4, TX), (7, FN), (1, TX)]),
    (4, [(5, KW), (5, TX), (8, FN), (3, TX)]),
    (6, [(2, KW), (4, TX), (6, ST)]),
    (6, [(14, CM)]),
    (6, [(6, FN), (1, TX), (4, NUM), (1, TX)]),
    (4, [(1, TX)]),
    (4, [(4, TX), (2, TX), (7, FN), (5, ST)]),
    (2, [(1, TX)]),
    (2, [(2, FN), (1, TX), (4, TX), (1, TX)]),
    (0, [(1, TX)]),
]
for n, (ind, segs) in enumerate(CODE):
    x = 144 + ind
    cv.px(142, 32 + n * 2, "#3a3f5a", E)
    for ln, col in segs:
        cv.rect(x, 32 + n * 2, ln, 1, col, E); x += ln + 1
# headphones on the corner
cv.blit(190, 24, [
    "..oooo.",
    ".orrrro",
    "or...or",
    "or...or",
    "ok...ko",
    "kkk.kkk",
    "kkk.kkk",
    "kkk.kkk",
    ".k...k.",
], {"o": O, "r": "#c8434b", "k": "#3a3550"})
# keyboard and mouse
cv.rect(145, 78, 44, 3, GREY_L); cv.rect(145, 81, 44, 1, GREY); cv.rect(144, 78, 1, 3, GREY); cv.rect(189, 78, 1, 3, GREY)
for y in (78, 79, 80):
    for x in range(146 + (y % 2), 188, 2): cv.px(x, y, "#a39f98")
cv.rect(158, 80, 16, 1, "#b9b5ac")
cv.rect(193, 78, 5, 3, GREY_L); cv.rect(193, 81, 5, 1, GREY); cv.px(195, 78, "#c8434b")

# crab plush
cv.blit(199, 66, [
    ".oo..........oo.",
    "orro........orro",
    "orRo.oooooo.oRro",
    ".orooRRrrrrooro.",
    "..orRrrrrrrrro..",
    ".orrwkrrrrwkrro.",
    ".orrkkrrrrkkrro.",
    ".orrrrrrrrrrrro.",
    "..orrrrddrrrro..",
    ".o.oooooooooo.o.",
    "o..o..o..o..o..o",
], {"o": O, "r": "#f0743a", "R": "#ffa85e", "k": O, "d": "#c24a26", "w": PAPER})

# lamp
LX = 232
cv.rect(LX - 5, 76, 11, 2, GREY_D); cv.rect(LX - 5, 76, 11, 1, GREY); cv.rect(LX - 5, 78, 11, 1, O)
cv.rect(LX, 51, 1, 25, GREY); cv.rect(LX + 1, 51, 1, 25, GREY_D)
cv.blit(LX - 6, 43, [
    "....ooooo....",
    "...oyyyyyo...",
    "..oyyYYyyyo..",
    ".oyyYYyyyyyo.",
    "oyyyyyyyyyyyo",
    "ooooooooooooo",
    "..lllllllll..",
], {"o": O, "y": "#e8a03c", "Y": "#ffd86b", "l": "#fff3c4"}, emit="yYl")
# pens in a mug
cv.blit(244, 64, [
    ".b..y.r.",
    ".b..y.r.",
    ".b.gy.r.",
    ".b.gy.r.",
    "oooooooo",
    "owwwwwwo",
    "owWwwwwo",
    "owwwwwwo",
    "owwwwwwo",
    "owwwwwwo",
    "owwwwwwo",
    ".oooooo.",
], {"o": O, "w": "#7fa8d8", "W": "#b5d0ee", "b": "#3d6fb8", "y": "#ffd86b", "r": "#c8434b", "g": "#3f8f4f"})

# tea, handheld, books
cv.blit(84, 66, [
    "l.....l",
    "lrrrrrl",
    "lrRrrrl",
    ".lrRrl.",
    "..lrl..",
    ".lrRrl.",
    "lrRrrrl",
    "lrrrrrl",
    "lrrrrrl",
    ".lllll.",
], {"l": "#f4ecd8", "r": "#c2452d", "R": "#e8853a"}, emit="rR")
cv.rect(82, 76, 11, 1, CREAM); cv.rect(83, 77, 9, 1, "#b9ad9c")
cv.rect(95, 76, 2, 2, PAPER); cv.rect(98, 77, 2, 1, PAPER)
cv.blit(104, 68, [
    ".ooooooooooooooooo.",
    "oyyyyyyyyyyyyyyyyyo",
    "oyyyysssssssssyyyyo",
    "oykyysgggggggsyyryo",
    "okkkysgGgggggsyryyo",
    "oykyysgggggggsyyyyo",
    "oyyyysssssssssyyyYo",
    "oYYYYYYYYYYYYYYYYYo",
    ".ooooooooooooooooo.",
], {"o": O, "y": "#e8a03c", "Y": "#c2772f", "s": O, "g": "#2f5f63", "G": "#7fe0d0", "k": "#2b1d2e", "r": "#c8434b"}, emit="gG")
for n, (col, w, dx) in enumerate((("#3d6fb8", 22, 0), ("#c8434b", 19, 2), ("#f4ecd8", 20, 1))):
    y = 73 - n * 4
    cv.box(54 + dx, y, w, 5, col, O); cv.rect(55 + dx, y + 1, w - 2, 1, rgbhex(mix(hexrgb(col), (255, 255, 255), .3)))
    cv.rect(54 + dx + w - 4, y + 1, 1, 3, PAPER)

# ------------------------------------------------------------ light
LAMP = (LX, 52)

def tint(c, kind):
    r, g, b = hexrgb(c)
    dim = (r * .52 + 10, g * .47 + 12, b * .62 + 40)
    if kind == "dim": return dim
    if kind == "half": return mix((r, g, b), dim, .55)
    if kind == "warm": return (r * 1.05 + 14, g * 1.02 + 6, b * .9)
    if kind == "sky": return mix(dim, (190, 150, 220), .22)
    if kind == "glow": return mix((r * .8, g * .82, b * .9), (120, 215, 215), .12)
    return (r, g, b)

def kind_at(x, y):
    d = math.hypot(x - LAMP[0], (y - LAMP[1]) * 1.15)
    ch = (x + y) % 2
    if d < 17 or (d < 19 and ch): k = "warm"
    elif d < 34 or (d < 36 and ch): k = "norm"
    elif d < 54 or (d < 56 and ch): k = "half"
    else: k = "dim"
    for bx, by in BULBS:
        bd = math.hypot(x - bx, y - by)
        if bd < 3.2 and k in ("dim", "half"): k = "norm"
        elif bd < 5.5 and k == "dim": k = "half"
    if k in ("dim", "half"):
        if 76 <= y < 83 and abs(x - 167) < 36 - (y - 76) * 2: k = "glow"
        elif 60 <= y < 63 and 17 <= x < 123: k = "sky"
        elif 76 <= y < 78 and x < 130 and k == "dim": k = "sky"
    return k

for y in range(H):
    for x in range(W):
        if not cv.e[y][x]:
            cv.g[y][x] = rgbhex(tint(cv.g[y][x], kind_at(x, y)))

# ------------------------------------------------------------ moving parts
def layer(): return Canvas(W, H)
tail1, tail2, st1, st2, cur, tw, red = (layer() for _ in range(7))
TK, TO = "#2a2244", "#15102a"
for cvs, pts in ((tail1, ((43, 59), (44, 60), (45, 61), (45, 62), (45, 63), (45, 64), (45, 65), (44, 66), (43, 67), (42, 67))),
                 (tail2, ((43, 59), (44, 60), (45, 61), (45, 62), (45, 63), (45, 64), (46, 65), (47, 66), (48, 67), (49, 67)))):
    for x, y in pts: cvs.rect(x - 1, y, 3, 1, TO)
    for x, y in pts: cvs.px(x, y, TK)
SC = "#e8e0f0"
for x, y in ((86, 63), (87, 62), (87, 60), (86, 59), (89, 64), (89, 61), (88, 57)): st1.px(x, y, SC)
for x, y in ((87, 64), (86, 62), (86, 60), (87, 58), (89, 63), (90, 61), (89, 58)): st2.px(x, y, SC)
cur.rect(146, 56, 2, 1, TX)
for x, y in (STARS[2], STARS[7], STARS[10]): tw.px(x, y, cv.g[y][x - 1])
red.px(T1, TOP - 2, "#ff5d6c"); red.px(T2, TOP - 2, "#ff5d6c")

CSS = (
    ".c{animation:b 1.1s steps(1) infinite}.w{animation:b 3.7s steps(1) infinite}.r{animation:b 2s steps(1) infinite}"
    ".f1{animation:f 2.6s steps(1) infinite}.f2{opacity:0;animation:f 2.6s steps(1) -1.3s infinite}"
    ".s1{animation:f 1.8s steps(1) infinite}.s2{opacity:0;animation:f 1.8s steps(1) -.9s infinite}"
    "@keyframes b{50%{opacity:0}}@keyframes f{0%{opacity:1}50%{opacity:0}}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
)

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dusk.svg")
    with open(out, "w") as f:
        f.write(svg(cv, [(tw, "w"), (red, "r"), (tail1, "f1"), (tail2, "f2"), (st1, "s1"), (st2, "s2"), (cur, "c")],
                    scale=5, css=CSS, rx=3,
                    label="pixel art: a desk under a window at dusk — the Bosphorus bridge outside, a cat on the sill, "
                          "a glass of tea, code on the monitor under a warm lamp"))
    print(os.path.normpath(out))
