#!/usr/bin/env python3
"""The small pieces around the scene, in the same font and palette:

  header-{dark,light}.svg   name + one line, pixel type
  btn-*.svg                 link buttons

No dependencies.  python3 assets/gen/ui.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from px import Canvas, svg, FONT, text_width

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
INK, CREAM, MID, LOW, ORANGE = "#2b1d2e", "#f4ecd8", "#8a86ab", "#6f6a85", "#f2a65a"

def big(cv, x, y, string, c, k=2, accent=None):
    """text at k times the font's pixel size; accent recolours the dots on ü"""
    for ch in string:
        g = FONT[ch]
        for j, row in enumerate(g):
            for i, bit in enumerate(row):
                if bit == "#":
                    cv.rect(x + i * k, y + j * k, k, k, accent if accent and ch == "ü" and j == 0 else c)
        x += (len(g[0]) + 1) * k
    return x

LINE = "I build whatever I'm curious about."

def header(name_c, line_c):
    """the name, one line under it, and a blinking cursor; centred"""
    nw = big(Canvas(1, 1), 0, 0, "Hüseyn Teymurzade", name_c) - 2
    W = nw + 24
    cv, cur = Canvas(W, 33), Canvas(W, 33)
    big(cv, (W - nw) // 2, 3, "Hüseyn Teymurzade", name_c, accent=ORANGE)
    lw = text_width(LINE) + 5
    x = cv.text((W - lw) // 2, 25, LINE, line_c)
    cur.rect(x + 1, 25, 3, 5, ORANGE)
    css = ".c{animation:b 1.1s steps(1) infinite}@keyframes b{50%{opacity:0}}"
    return svg(cv, [(cur, "c")], scale=4, label=f"Hüseyn Teymurzade — {LINE}", css=css)

GLYPHS = {
    "linkedin": ("LinkedIn", ["x......", ".......", "x..xxx.", "x..x..x", "x..x..x", "x..x..x", "x..x..x"], "#7fa8d8"),
    "email":    ("Email",    ["xxxxxxx", "x.....x", "xx...xx", "x.x.x.x", "x..x..x", "x.....x", "xxxxxxx"], ORANGE),
    "leetcode": ("LeetCode", ["....xx.", "...x...", "..x....", ".x..xxx", "..x....", "...x...", "....xx."], "#ffd86b"),
    "codewars": ("Codewars", ["..xxxx.", ".x....x", "x......", "x......", "x......", ".x....x", "..xxxx."], "#e2656a"),
}

def button(label, rows, accent):
    cv = Canvas(11 + 4 + text_width(label) + 1, 11)
    cv.box(0, 0, 11, 11, INK, accent)
    for x, y in ((0, 0), (10, 0), (0, 10), (10, 10)): cv.g[y][x] = None
    cv.blit(2, 2, rows, {"x": accent})
    cv.text(15, 2, label, MID)
    return svg(cv, scale=3, label=label)

if __name__ == "__main__":
    files = {"header-dark.svg": header(CREAM, MID), "header-light.svg": header(INK, LOW)}
    files.update({f"btn-{k}.svg": button(*v) for k, v in GLYPHS.items()})
    for name, body in files.items():
        with open(os.path.join(HERE, name), "w") as f: f.write(body)
        print(name)
