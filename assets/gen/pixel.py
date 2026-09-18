#!/usr/bin/env python3
"""Pixel art for README.md, drawn as SVG rects on a grid. PICO-8 palette.

  desk.svg      a desk at night: string lights, monitor, coffee, a cat
  btn-*.svg     link buttons

No dependencies.  python3 assets/gen/pixel.py
"""
import random

P = dict(k="#1D2B53", K="#10193A", w="#FFF1E8", s="#FFCCAA", b="#AB5236", B="#7A3A22",
         d="#7E2553", y="#FFEC27", o="#FFA300", g="#00E436", G="#5F574F", l="#C2C3C7",
         m="#83769C", p="#FF77A8", r="#FF004D", c="#29ADFF", e="#008751", n="#000000", j="#2A3F6E")

class Canvas:
    def __init__(s, w, h, bg=None):
        s.w, s.h = w, h
        s.g = [[bg]*w for _ in range(h)]
    def px(s, x, y, c):
        if 0 <= x < s.w and 0 <= y < s.h: s.g[y][x] = c
    def rect(s, x, y, w, h, c):
        for j in range(y, y+h):
            for i in range(x, x+w): s.px(i, j, c)
    def hline(s, x, y, w, c): s.rect(x, y, w, 1, c)
    def vline(s, x, y, h, c): s.rect(x, y, 1, h, c)
    def blit(s, x, y, rows, key):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch != ".": s.px(x+i, y+j, key[ch])
    def svg(s, scale, label, rx=0):
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w*scale} {s.h*scale}" '
               f'width="{s.w*scale}" height="{s.h*scale}" shape-rendering="crispEdges" role="img" aria-label="{label}">']
        if rx:
            out.append(f'<clipPath id="r"><rect width="{s.w*scale}" height="{s.h*scale}" rx="{rx}"/></clipPath><g clip-path="url(#r)">')
        # run-length rows: one rect per run of the same colour
        for j, row in enumerate(s.g):
            i = 0
            while i < s.w:
                c = row[i]
                if c is None: i += 1; continue
                k = i
                while k < s.w and row[k] == c: k += 1
                out.append(f'<rect x="{i*scale}" y="{j*scale}" width="{(k-i)*scale}" height="{scale}" fill="{P[c]}"/>')
                i = k
        if rx: out.append('</g>')
        out.append('</svg>\n')
        return "\n".join(out)

# ---------------------------------------------------------------- desk scene
def desk():
    W, H = 128, 44
    cv = Canvas(W, H, "k")
    rng = random.Random(7)

    # sky: stars
    for _ in range(40):
        x, y = rng.randrange(0, W), rng.randrange(6, 22)
        cv.px(x, y, "w" if rng.random() < .35 else "m")
    # moon, top left
    cv.blit(22, 8, [
        "..sss.",
        ".ss...",
        "ss....",
        "ss....",
        "ss....",
        ".ss...",
        "..sss.",
    ], {"s": "s"})
    cv.blit(23, 9, ["ww", "ww", "ww", "ww", "ww"], {"w": "w"})

    # string lights: a drooping wire with bulbs
    wire_y = [1,1,2,2,3,3,4,4,4,4,4,4,3,3,2,2,1,1]
    for x in range(W):
        cv.px(x, wire_y[x % len(wire_y)], "G")
    bulbs = "yopcyog"
    for n, x in enumerate(range(4, W, 9)):
        y = wire_y[x % len(wire_y)] + 1
        cv.px(x, y, "G")
        cv.rect(x-1, y+1, 3, 2, bulbs[n % len(bulbs)])
        cv.px(x, y+3, bulbs[n % len(bulbs)])

    # wall shelf, right
    cv.hline(98, 17, 26, "B"); cv.hline(98, 18, 26, "b")
    books = "rcyop"
    for n, x in enumerate(range(100, 116, 3)):
        cv.rect(x, 11 - (n % 2), 2, 6 + (n % 2), books[n % 5])
    cv.rect(118, 14, 4, 3, "b"); cv.blit(117, 10, [".e.e.", "eeeee", ".eee.", "..e.."], {"e": "e"})

    # desk
    cv.rect(0, 33, W, 2, "b"); cv.rect(0, 35, W, 1, "B")
    cv.rect(0, 36, W, 8, "K")
    cv.rect(8, 36, 2, 8, "B"); cv.rect(118, 36, 2, 8, "B")  # legs

    # desk lamp, left: shade, stem, base, and a soft cone of light on the desk
    lx = 14
    for j, (x0, w) in enumerate(((lx-3, 6), (lx-4, 8), (lx-5, 10), (lx-6, 12))):
        for x in range(x0, x0 + w):
            for y in range(23 + j*3, 23 + j*3 + 3):
                if cv.g[y][x] == "k": cv.px(x, y, "j")
    cv.rect(lx-3, 20, 6, 1, "o"); cv.rect(lx-4, 21, 8, 1, "o"); cv.rect(lx-5, 22, 10, 1, "B")
    cv.rect(lx-4, 23, 8, 1, "y")
    cv.vline(lx, 23, 10, "G"); cv.rect(lx-2, 32, 5, 1, "G")

    # succulent in a pot
    cv.rect(24, 30, 5, 3, "b"); cv.rect(23, 29, 7, 1, "B")
    cv.blit(23, 24, ["..g....", ".g.g.e.", ".g.g.e.", "..gee..", "..ege..", ".eeeee."], {"g": "g", "e": "e"})

    # coffee
    cv.rect(34, 27, 6, 6, "w"); cv.rect(35, 28, 4, 1, "b")
    cv.vline(40, 28, 4, "w"); cv.px(41, 29, "w"); cv.px(41, 30, "w")
    for i, (dx, dy) in enumerate(((1,25),(2,23),(3,24),(2,21),(4,22))):
        cv.px(34+dx, dy, "s" if i % 2 else "l")

    # monitor
    mx, my = 48, 14
    cv.rect(mx, my, 34, 16, "l"); cv.rect(mx+1, my+1, 32, 14, "K")
    cv.rect(mx+15, my+16, 4, 2, "G"); cv.rect(mx+11, my+18, 12, 1, "l")  # stand
    lines = [("g",3),("m",8),("c",5),("w",7),("m",10),("o",4),("w",9),("c",6),("g",5),("m",9)]
    for n, (col, ln) in enumerate(lines):
        y = my + 2 + n
        cv.hline(mx + 3 + (2 if n in (3,4,7,8) else 0), y, ln, col)
    cv.rect(mx + 3, my + 13, 1, 1, "g")                     # prompt
    cv.rect(mx + 5, my + 13, 2, 1, "w")                     # cursor
    # keyboard and mouse
    cv.rect(52, 31, 26, 2, "G"); cv.hline(54, 31, 22, "l")
    cv.rect(84, 31, 3, 2, "l")

    # cat asleep on the desk, right; head left, tail curled up on the right
    cv.blit(94, 25, [
        ".G.G..........",
        ".GGG.GGGGGGG..",
        "GGGGGGGGGGGGG.",
        "GGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGG",
        ".GGGGGGGGGGGG.",
        "..GG.GG..GG.GG",
    ], {"G": "G"})
    cv.px(95, 27, "K"); cv.px(97, 27, "K")                  # closed eyes
    cv.px(96, 28, "p")                                       # nose
    cv.rect(107, 24, 1, 3, "G"); cv.rect(106, 23, 1, 1, "G") # tail
    return cv


# ---------------------------------------------------------------- buttons
def button(label, glyph_rows, accent):
    # 8px-tall pixel font would be overkill; the label is rendered as SVG text next to a pixel glyph
    W, H, S = 11, 11, 3
    cv = Canvas(W, H, "K")
    cv.rect(0, 0, W, 1, accent); cv.rect(0, H-1, W, 1, accent); cv.vline(0, 0, H, accent); cv.vline(W-1, 0, H, accent)
    cv.blit(2, 2, glyph_rows, {"x": accent, "w": "w"})
    icon = cv.svg(S, label)
    # wrap: icon + label in one svg
    body = icon.split("\n", 1)[1].rsplit("</svg>", 1)[0]
    tw = 8 * len(label) + 14
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W*S+tw} {H*S}" width="{W*S+tw}" height="{H*S}" '
            f'role="img" aria-label="{label}">'
            f'<g shape-rendering="crispEdges">{body}</g>'
            f'<text x="{W*S+8}" y="{H*S/2+5}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="14" fill="#8C959F">{label}</text></svg>\n')

GLYPHS = {
    "linkedin": ("LinkedIn", ["x......", ".......", "x..xxx.", "x..x..x", "x..x..x", "x..x..x", "x..x..x"], "c"),
    "email":    ("Email",    ["xxxxxxx", ".xxxxx.", "x.xxx.x", "xx.x.xx", "xxxxxxx", "xxxxxxx", "xxxxxxx"], "o"),
    "leetcode": ("LeetCode", ["....xx.", "...x...", "..x....", ".x..xxx", "..x....", "...x...", "....xx."], "y"),
    "codewars": ("Codewars", ["..xxxx.", ".x....x", "x......", "x......", "x......", ".x....x", "..xxxx."], "r"),
}

if __name__ == "__main__":
    with open("assets/desk.svg", "w") as f:
        f.write(desk().svg(7, "pixel art: a desk at night — string lights, a monitor with code, coffee, a lamp and a cat asleep", rx=10))
    print("assets/desk.svg")
    for name, (title, rows, acc) in GLYPHS.items():
        with open(f"assets/btn-{name}.svg", "w") as f: f.write(button(title, rows, acc))
        print(f"assets/btn-{name}.svg")
