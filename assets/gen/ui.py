#!/usr/bin/env python3
"""The small pieces around the scene, in the same font and palette:

  header-{dark,light}.svg   name and two lines, pixel type
  btn-*.svg                 link buttons
  palette.svg               the colours dusk.svg is painted with

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

def header(name_c, sub_c, low_c):
    cv = Canvas(300, 46)
    big(cv, 1, 1, "Hüseyn Teymurzade", name_c, accent=ORANGE)
    cv.text(1, 24, "computer engineering · marmara university", sub_c)
    cv.text(1, 36, "low-level, systems, and the layers underneath", low_c)
    return svg(cv, scale=5, label="Hüseyn Teymurzade — computer engineering, Marmara University")

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

def palette():
    cols = ["#10133a", "#1f2566", "#2f2d7c", "#4b3689", "#7a4390", "#b5557f", "#e07a6a", "#f2a65a", "#ffd86b",
            "#f4ecd8", "#7fe0d0", "#3f8f4f", "#b5573a", "#8a5a3a", "#2b1d2e"]
    cv = Canvas(len(cols) * 4 - 1, 3)
    for n, c in enumerate(cols): cv.rect(n * 4, 0, 3, 3, c)
    return svg(cv, scale=4, label="the palette")

if __name__ == "__main__":
    files = {"header-dark.svg": header(CREAM, MID, LOW), "header-light.svg": header(INK, LOW, MID), "palette.svg": palette()}
    files.update({f"btn-{k}.svg": button(*v) for k, v in GLYPHS.items()})
    for name, body in files.items():
        with open(os.path.join(HERE, name), "w") as f: f.write(body)
        print(name)
    print(text_width("computer engineering · marmara university"), text_width("low-level, systems, and the layers underneath"))
