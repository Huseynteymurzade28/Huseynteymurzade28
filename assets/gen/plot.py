#!/usr/bin/env python3
"""Generates the line-art strip used in README.md.

  topo-*.svg  contour lines (marching squares) over a Perlin fBm field
  mark-*.svg  a damped harmonograph curve, used as a colophon mark

No dependencies. Deterministic: same seed, same picture.
  python3 assets/gen/plot.py
"""
import math, random

SEED = 28
OUT = "assets"

# ---- palette -------------------------------------------------------------
INK   = {"light": "#59636E", "dark": "#8B949E"}   # ordinary lines
INDEX = {"light": "#D2853F", "dark": "#E8A15C"}   # every n-th contour
DOT   = INDEX

# ---- perlin --------------------------------------------------------------
class Perlin:
    def __init__(self, seed):
        rng = random.Random(seed)
        p = list(range(256)); rng.shuffle(p)
        self.p = p + p
    @staticmethod
    def fade(t): return t*t*t*(t*(t*6-15)+10)
    @staticmethod
    def grad(h, x, y):
        h &= 7
        u = x if h < 4 else y
        v = y if h < 4 else x
        return (u if h & 1 == 0 else -u) + (v if h & 2 == 0 else -v) * 0.5
    def noise(self, x, y):
        X, Y = int(math.floor(x)) & 255, int(math.floor(y)) & 255
        x -= math.floor(x); y -= math.floor(y)
        u, v = self.fade(x), self.fade(y)
        p = self.p
        a, b = p[X]+Y, p[X+1]+Y
        lerp = lambda t, a, b: a + t*(b-a)
        return lerp(v,
            lerp(u, self.grad(p[a], x, y),   self.grad(p[b], x-1, y)),
            lerp(u, self.grad(p[a+1], x, y-1), self.grad(p[b+1], x-1, y-1)))
    def fbm(self, x, y, octaves=4, lac=2.0, gain=0.5):
        amp, freq, s, norm = 1.0, 1.0, 0.0, 0.0
        for _ in range(octaves):
            s += amp * self.noise(x*freq, y*freq); norm += amp
            amp *= gain; freq *= lac
        return s / norm

# ---- marching squares ----------------------------------------------------
def contours(field, w, h, cell, level):
    """Return list of polylines (lists of (x,y)) for one iso-level."""
    segs = []
    def interp(p1, v1, p2, v2):
        t = (level - v1) / (v2 - v1) if v2 != v1 else 0.5
        return (p1[0] + t*(p2[0]-p1[0]), p1[1] + t*(p2[1]-p1[1]))
    for j in range(h-1):
        for i in range(w-1):
            v = [field[j][i], field[j][i+1], field[j+1][i+1], field[j+1][i]]
            pts = [(i*cell, j*cell), ((i+1)*cell, j*cell), ((i+1)*cell, (j+1)*cell), (i*cell, (j+1)*cell)]
            idx = sum(1 << k for k in range(4) if v[k] >= level)
            if idx in (0, 15): continue
            e = [None]*4
            for k in range(4):
                a, b = k, (k+1) % 4
                if (v[a] >= level) != (v[b] >= level):
                    e[k] = interp(pts[a], v[a], pts[b], v[b])
            edges = [k for k in range(4) if e[k] is not None]
            if len(edges) == 2:
                segs.append((e[edges[0]], e[edges[1]]))
            else:  # saddle: resolve by centre value
                c = sum(v)/4
                if (c >= level) == (v[0] >= level):
                    segs.append((e[0], e[1])); segs.append((e[2], e[3]))
                else:
                    segs.append((e[0], e[3])); segs.append((e[1], e[2]))
    # link segments into polylines
    key = lambda p: (round(p[0], 3), round(p[1], 3))
    ends = {}
    for s in segs:
        for p in s: ends.setdefault(key(p), []).append(s)
    used, lines = set(), []
    for s in segs:
        if id(s) in used: continue
        used.add(id(s)); line = [s[0], s[1]]
        for head in (True, False):
            while True:
                p = line[-1] if head else line[0]
                nxt = next((t for t in ends.get(key(p), []) if id(t) not in used), None)
                if nxt is None: break
                used.add(id(nxt))
                q = nxt[1] if key(nxt[0]) == key(p) else nxt[0]
                line.append(q) if head else line.insert(0, q)
        lines.append(line)
    return lines

def path(pts):
    f = lambda v: ("%.1f" % v).rstrip("0").rstrip(".")
    return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)

def svg_open(w, h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{label}">\n'
            f'<defs>'
            f'<linearGradient id="fx" x1="0" x2="1" y1="0" y2="0">'
            f'<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            f'<stop offset="0.12" stop-color="#fff" stop-opacity="1"/>'
            f'<stop offset="0.88" stop-color="#fff" stop-opacity="1"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="fy" x1="0" x2="0" y1="0" y2="1">'
            f'<stop offset="0" stop-color="#fff" stop-opacity="0.25"/>'
            f'<stop offset="0.22" stop-color="#fff" stop-opacity="1"/>'
            f'<stop offset="0.78" stop-color="#fff" stop-opacity="1"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0.25"/></linearGradient>'
            f'<mask id="mx"><rect width="{w}" height="{h}" fill="url(#fx)"/></mask>'
            f'<mask id="my"><rect width="{w}" height="{h}" fill="url(#fy)"/></mask></defs>\n'
            f'<g mask="url(#mx)"><g mask="url(#my)" fill="none" stroke-linecap="round" stroke-linejoin="round">\n')

# ---- topo strip ----------------------------------------------------------
def topo(theme):
    W, H, CELL = 1200, 210, 5
    w, h = W//CELL + 1, H//CELL + 1
    pn = Perlin(SEED)
    field = [[pn.fbm(i*CELL/430.0, j*CELL/430.0 + 3.2, octaves=4, gain=0.42) for i in range(w)] for j in range(h)]
    lo = min(min(r) for r in field); hi = max(max(r) for r in field)
    levels = 12
    out = [svg_open(W, H, "contour lines of a Perlin noise field")]
    for n in range(1, levels):
        lvl = lo + (hi-lo) * n / levels
        index = (n % 4 == 0)
        col = INDEX[theme] if index else INK[theme]
        sw  = 1.1 if index else 0.7
        op  = 0.85 if index else 0.55
        for line in contours(field, w, h, CELL, lvl):
            if len(line) < 6: continue
            out.append(f'<path d="{path(line)}" stroke="{col}" stroke-width="{sw}" opacity="{op}"/>')
    # a survey point: the highest cell
    jm, im = max(((j, i) for j in range(int(h*.25), int(h*.75)) for i in range(int(w*.15), int(w*.85))), key=lambda t: field[t[0]][t[1]])
    out.append(f'<circle cx="{im*CELL}" cy="{jm*CELL}" r="2.4" fill="{DOT[theme]}" stroke="none"/>')
    out.append('</g></g></svg>\n')
    return "\n".join(out)

# ---- colophon mark -------------------------------------------------------
def mark(theme):
    W = H = 140
    cx, cy, R = W/2, H/2, 58
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'role="img" aria-label="harmonograph curve"><g fill="none" stroke-linecap="round">']
    # two damped pendulums, almost in tune: the ellipse slowly turns as it decays
    pts = []
    for n in range(2300):
        t = n * 0.014
        d = math.exp(-t * 0.034)
        x = cx + R*d*math.sin(3.00*t + math.pi/2)
        y = cy + R*d*math.sin(3.07*t)
        pts.append((x, y))
    out.append(f'<path d="{path(pts)}" stroke="{INK[theme]}" stroke-width="0.55" opacity="0.7"/>')
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.8" fill="{DOT[theme]}" stroke="none"/>')
    out.append('</g></svg>\n')
    return "\n".join(out)

if __name__ == "__main__":
    for theme in ("light", "dark"):
        for name, fn in (("topo", topo), ("mark", mark)):
            p = f"{OUT}/{name}-{theme}.svg"
            with open(p, "w") as f: f.write(fn(theme))
            print(p)
