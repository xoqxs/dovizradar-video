"""Sing with Tavo – fixed render engine (Baby Collective). Do NOT rewrite per song.

Per song you only write song.py (lyrics/melody/sections) and topic.py (guests, themes, words).
Run in the work folder (needs voice_env.npy + final_audio.wav for final/short):

  python3 engine.py still h <sec> out.jpg      # one 16:9 frame (check before rendering)
  python3 engine.py still v <sec> out.jpg      # one 9:16 frame
  python3 engine.py render                     # 16:9 video only -> video_h.mp4 (2 processes)
  python3 engine.py final OUT.mp4              # mux video_h.mp4 + final_audio.wav (loudnorm -14)
  python3 engine.py short <t0> <dur> OUT.mp4   # NATIVE vertical 1080x1920 Short of that window
  python3 engine.py thumb OUT.jpg              # 1280x720 thumbnail
  python3 engine.py chorus_starts              # prints chorus start times (pick the Short window)
"""
import math, os, sys, subprocess
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from song import SECTIONS, BEAT, TOTAL_BEATS, events
import topic as T
import chars as C

FPS = 30
TAIL = 2.5
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = next(p for p in ['Fredoka-Bold.ttf', os.path.join(HERE, 'Fredoka-Bold.ttf'), '/home/claude/build/Fredoka-Bold.ttf'] if os.path.exists(p))
_fc = {}


def font(sz):
    sz = max(4, int(sz))
    if sz not in _fc:
        _fc[sz] = ImageFont.truetype(FONT, sz)
    return _fc[sz]


LAY = {
    'h': dict(W=1920, H=1080, word=(960, 150, 170), guest=(960, 560, 440), host=(270, 690, 330),
              lyr_top=880, lyr_font=84, lyr_max=1720, ground=(-300, 760, 2220, 1500),
              rb=(960, 980, 900, 48), clouds=[(260, 210, 1.0), (1650, 160, 1.2), (1500, 420, 0.7), (400, 470, 0.8)],
              ch_guest_y=520, ch_guest_size=300, ch_host=(230, 760, 300), ch_rosy=(1700, 770, 290), ch_grid=None,
              logo=(960, 78, 58), title=(960, 172, 100), brand=(960, 262, 40), intro_tavo=(960, 610, 600),
              intro_crew=[('rosy', 450, 690, 340), ('rubbo', 1450, 720, 310), ('lino', 1710, 650, 340)],
              note=(960, 965, 80), end_title=(960, 170, 170), end_tavo=(960, 590, 520),
              end_row=[(240, 700), (520, 730), (1400, 730), (1680, 700)], end_size=300),
    'v': dict(W=1080, H=1920, word=(540, 250, 150), guest=(560, 740, 600), host=(165, 1010, 290),
              lyr_top=1150, lyr_font=72, lyr_max=860, ground=(-400, 1060, 1480, 2400),
              rb=(540, 1120, 560, 34), clouds=[(180, 170, 0.8), (900, 140, 0.9), (880, 470, 0.6), (190, 520, 0.6)],
              ch_guest_y=None, ch_guest_size=300, ch_host=(190, 1430, 290), ch_rosy=(870, 1450, 250),
              ch_grid={1: [(540, 720)], 2: [(320, 720), (760, 720)], 3: [(300, 600), (780, 600), (540, 930)],
                       4: [(320, 580), (760, 580), (320, 930), (760, 930)],
                       5: [(250, 580), (540, 580), (830, 580), (390, 930), (690, 930)]},
              logo=(540, 190, 66), title=(540, 300, 88), brand=(540, 390, 42), intro_tavo=(540, 790, 640),
              intro_crew=[('rosy', 190, 1250, 300), ('lino', 540, 1290, 300), ('rubbo', 880, 1270, 280)],
              note=(540, 1460, 80), end_title=(540, 290, 160), end_tavo=(540, 760, 560),
              end_row=[(160, 1200), (410, 1230), (670, 1230), (920, 1200)], end_size=260),
}

# verse index for each section
VIDX = {}
_k = 0
for _i, _s in enumerate(SECTIONS):
    if _s['kind'] == 'verse':
        VIDX[_i] = _k
        _k += 1
GUEST_ORDER = []
for v in T.VERSES:
    if v['guest'] not in GUEST_ORDER:
        GUEST_ORDER.append(v['guest'])
ACTION_LINE = getattr(T, 'ACTION_LINE', 2)
REVEAL = getattr(T, 'REVEAL', True)          # guess pause: silhouette + '?' then Rosy colours the guest in
REVEAL_AT = getattr(T, 'REVEAL_AT', (5.0, 7.4))  # beats into the verse (line 1 = question, its rest = guessing time)

# ------------------------------------------------------------ timing helpers
NOTES, _ = events()
_ENV = None


def env():
    global _ENV
    if _ENV is None:
        _ENV = np.load('voice_env.npy') if os.path.exists('voice_env.npy') else np.zeros(1)
    return _ENV


def talking(t):
    e = env()
    i = int(t * FPS)
    if len(e) > 1:
        return i < len(e) and e[i] > 0.12
    b = t / BEAT
    return any(b0 <= b < b0 + d * 0.85 for b0, d, *_ in NOTES)


def blink(t, seed):
    return (t + seed * 1.37) % 3.3 < 0.12


def ease_back(u):
    u = min(max(u, 0.0), 1.0)
    c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (u - 1) ** 3 + c1 * (u - 1) ** 2


# ------------------------------------------------------------ sprites
_SPR = {}


def spr(name, mo, bl, size, **kw):
    size = max(8, int(size))
    key = (name, mo, bl, size, tuple(sorted(kw.items())))
    if key not in _SPR:
        f = C.CREW.get(name) or T.GUESTS[name]
        _SPR[key] = f(mo, bl, size, **kw)
    return _SPR[key]


def paste(base, im, cx, cy, sx=1.0, sy=1.0, rot=0.0):
    if sx <= 0.02 or sy <= 0.02:
        return
    if abs(sx - 1) > 1e-3 or abs(sy - 1) > 1e-3:
        im = im.resize((max(1, int(im.width * sx)), max(1, int(im.height * sy))), Image.BILINEAR)
    if rot:
        im = im.rotate(rot, resample=Image.BILINEAR, expand=True)
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def text(d, x, y, s, sz, fill, stroke=8, sfill='white', anchor='mm'):
    if sz < 6:
        return
    d.text((x, y), s, font=font(sz), fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)


def star(d, x, y, r, col):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    d.polygon(pts, fill=col)


# ------------------------------------------------------------ backgrounds
_BG = {}


def _cloud(d, x, y, s, a=235):
    for dx, dy, rr in [(0, 0, 70), (70, 15, 55), (-70, 15, 55), (35, -35, 55)]:
        d.ellipse([x + dx * s - rr * s, y + dy * s - rr * s, x + dx * s + rr * s, y + dy * s + rr * s], fill=(255, 255, 255, a))


def _grad(W, H, top, bot, y0=0.0, y1=1.0):
    y = np.clip((np.linspace(0, 1, H) - y0) / max(1e-6, y1 - y0), 0, 1)[:, None, None]
    return (np.array(top)[None, None] * (1 - y) + np.array(bot)[None, None] * y) * np.ones((1, W, 1))


SCENES = ('sea', 'farm', 'road', 'sky', 'garden', 'night', 'room', 'park')


def _scene(o, th, scene):
    """Static backdrop for a topic scene (cached). Land = LAY ground ellipse so characters stand on it."""
    L = LAY[o]; W, H = L['W'], L['H']
    x0, y0, x1, y1 = L['ground']
    hz = y0 + 40                       # horizon a bit under the land top
    sky_t, sky_b = th.get('top', (150, 210, 255)), th.get('bot', (225, 245, 255))
    if scene == 'night':
        sky_t, sky_b = (20, 30, 80), (70, 70, 150)
    arr = _grad(W, H, sky_t, sky_b, 0, hz / H)
    im = Image.fromarray(arr.astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(im, 'RGBA')
    rng = np.random.default_rng(len(scene) * 97 + W)
    land = th.get('ground', (140, 215, 105))
    if scene == 'sea':
        wt = int(H * 0.36)
        sea = Image.fromarray(_grad(W, H - wt, (90, 200, 240), (20, 110, 190)).astype(np.uint8)).convert('RGBA')
        im.alpha_composite(sea, (0, wt))
        d = ImageDraw.Draw(im, 'RGBA')
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        for k in range(10):                                   # soft light rays
            x = rng.uniform(0, W); w = rng.uniform(30, 80)
            od.polygon([(x, wt), (x + w, wt), (x + w - 160, H), (x - 160, H)], fill=(255, 255, 255, 28))
        im.alpha_composite(ov); d = ImageDraw.Draw(im, 'RGBA')
        bed = H * 0.9
        d.ellipse([-W * 0.2, bed, W * 1.2, H + H * 0.3], fill=(236, 205, 140, 255))
        for k in range(9):                                    # seaweed + rocks on the bottom
            x = rng.uniform(0, W); hh = rng.uniform(H * 0.1, H * 0.2)
            for j in range(3):
                d.line([(x + j * 14, H), (x + j * 14 + 25 * math.sin(j), H - hh)], fill=(40, 150, 90, 255), width=14)
        for k in range(6):
            x = rng.uniform(0, W); r = rng.uniform(40, 90)
            d.ellipse([x - r, H - r * 0.6, x + r, H + r * 0.6], fill=(120, 110, 140, 255))
        hx, hy, hs = L['host']                                # small sandy island for Tavo
        d.ellipse([hx - hs * 0.95, hy + hs * 0.32, hx + hs * 0.95, hy + hs * 0.95], fill=(222, 190, 125, 255))
        d.ellipse([hx - hs * 0.85, hy + hs * 0.36, hx + hs * 0.85, hy + hs * 0.9], fill=(244, 214, 150, 255))
        return im
        land = (244, 214, 150)
    elif scene == 'night':
        for k in range(70):
            x, y = rng.uniform(0, W), rng.uniform(0, hz * 0.9)
            r = rng.uniform(2, 5); d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 220, 230))
        mx, my, mr = W * 0.82, H * 0.14, min(W, H) * 0.07
        d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(255, 245, 190, 255))
        d.ellipse([mx - mr * 0.55, my - mr * 1.05, mx + mr * 1.4, my + mr * 0.9], fill=sky_t + (255,))
        land = (60, 110, 90)
    elif scene == 'room':
        wall = th.get('top', (255, 236, 210))
        im = Image.fromarray(_grad(W, H, wall, th.get('bot', (255, 220, 190))).astype(np.uint8)).convert('RGBA')
        d = ImageDraw.Draw(im, 'RGBA')
        fy = y0 + 60
        d.rectangle([0, fy, W, H], fill=(196, 140, 92, 255))
        for k in range(0, W, 140):
            d.line([(k, fy), (k - 80, H)], fill=(170, 118, 76, 255), width=4)
        wx, wy, ww = W * 0.72, H * 0.12, min(W, H) * 0.28
        d.rounded_rectangle([wx, wy, wx + ww, wy + ww * 0.8], radius=18, fill=(170, 220, 255, 255), outline=(255, 255, 255, 255), width=14)
        d.line([(wx + ww / 2, wy), (wx + ww / 2, wy + ww * 0.8)], fill='white', width=10)
        d.ellipse([W / 2 - W * 0.38, H - (H - fy) * 0.55, W / 2 + W * 0.38, H + (H - fy) * 0.3], fill=tuple(int(c * 0.45 + 255 * 0.55) for c in th.get('col', (216, 27, 96))) + (255,))
        return im
    else:
        if scene in ('sky', 'park', 'garden', 'farm', 'road'):
            sx, sy, sr = W * 0.86, H * 0.12, min(W, H) * 0.075
            d.ellipse([sx - sr * 1.5, sy - sr * 1.5, sx + sr * 1.5, sy + sr * 1.5], fill=(255, 240, 150, 90))
            d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 214, 60, 255))
        # far hills
        for k, (c, yy) in enumerate([((170, 225, 150), hz - 70), ((150, 210, 130), hz - 30)]):
            for j in range(4):
                cx = W * (j / 3) + (k * 160); r = W * 0.28
                d.ellipse([cx - r, yy, cx + r, yy + r * 0.9], fill=c + (255,))
        if scene == 'farm':
            bx, by = W * 0.8, hz - H * 0.14
            bw, bh = min(W, H) * 0.22, H * 0.16
            d.rectangle([bx - bw / 2, by, bx + bw / 2, by + bh], fill=(205, 50, 45, 255))
            d.polygon([(bx - bw * 0.6, by), (bx, by - bh * 0.6), (bx + bw * 0.6, by)], fill=(150, 40, 40, 255))
            d.rectangle([bx - bw * 0.15, by + bh * 0.4, bx + bw * 0.15, by + bh], fill=(255, 240, 220, 255))
            for k in range(0, W, 90):                                 # fence
                d.rectangle([k, hz - 10, k + 16, hz + 60], fill=(250, 245, 235, 255))
            d.rectangle([0, hz + 5, W, hz + 20], fill=(250, 245, 235, 255)); d.rectangle([0, hz + 35, W, hz + 50], fill=(250, 245, 235, 255))
        if scene in ('park', 'garden', 'road'):
            for k in range(5):
                tx = rng.uniform(0, W); ty = hz - rng.uniform(0, 40); tr = rng.uniform(60, 110)
                d.rectangle([tx - 12, ty, tx + 12, ty + tr * 1.3], fill=(130, 90, 60, 255))
                d.ellipse([tx - tr, ty - tr * 1.4, tx + tr, ty + tr * 0.4], fill=(70, 170, 80, 255))
    # land
    g2 = tuple(max(0, v - 25) for v in land)
    d.ellipse([x0, y0, x1, y1], fill=g2 + (255,))
    d.ellipse([x0 + 100, y0 + 30, x1 - 100, y1], fill=land + (255,))
    if scene == 'road':
        ry = y0 + 95
        d.rectangle([0, ry - H * 0.05, W, ry + H * 0.05], fill=(90, 90, 100, 255))
    if scene == 'garden':
        for k in range(26):
            fx, fy = rng.uniform(0, W), rng.uniform(y0 + 60, H)
            c = [(255, 120, 170), (255, 210, 60), (180, 120, 255), (255, 255, 255)][k % 4]
            for a in range(5):
                aa = a * 2 * math.pi / 5
                d.ellipse([fx + 14 * math.cos(aa) - 11, fy + 14 * math.sin(aa) - 11, fx + 14 * math.cos(aa) + 11, fy + 14 * math.sin(aa) + 11], fill=c + (255,))
            d.ellipse([fx - 8, fy - 8, fx + 8, fy + 8], fill=(255, 190, 40, 255))
    return im


def scene_fx(o, base, theme, t):
    """Moving parts of a scene (drawn every frame)."""
    th = T.THEMES[theme]; scene = th.get('scene')
    if not scene:
        return
    L = LAY[o]; W, H = L['W'], L['H']
    d = ImageDraw.Draw(base, 'RGBA')
    if scene == 'sea':
        wt = int(H * 0.36)
        for k in range(3):
            pts = [(x, wt + 8 + k * 14 + 9 * math.sin(x / 70 + t * 2.2 + k)) for x in range(0, W + 40, 40)]
            d.line(pts, fill=(255, 255, 255, 150 - k * 40), width=6)
        for k in range(18):
            ph = (t * (0.08 + 0.02 * (k % 4)) + k * 0.137) % 1
            x = (k * 263) % W + 18 * math.sin(t * 2 + k); y = H - ph * (H - wt)
            r = 6 + (k % 5) * 3
            d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 255, 255, 170), width=3)
    elif scene == 'night':
        for k in range(12):
            x = (k * 337) % W; y = (k * 151) % int(H * 0.45)
            a = int(127 + 127 * math.sin(t * 3 + k))
            star(d, x, y, 10, (255, 255, 210, a))
    elif scene in ('sky', 'farm', 'park', 'garden', 'road'):
        for k, (x, y, s) in enumerate(L['clouds']):
            xx = (x + t * (14 + 6 * k)) % (W + 400) - 200
            _cloud(d, xx, y, s * 0.9, 220)
        if scene == 'road':
            x0, y0, x1, y1 = L['ground']
            ry = y0 + 95
            off = (t * 160) % 160
            for x in range(-160, W + 160, 160):
                d.rectangle([x - off, ry - 6, x - off + 80, ry + 6], fill=(255, 255, 255, 255))


_BG = {}


def background(o, theme):
    key = (o, theme)
    if key in _BG:
        return _BG[key]
    L = LAY[o]; W, H = L['W'], L['H']
    th = T.THEMES[theme]
    if th.get('scene') in SCENES:
        im = _scene(o, th, th['scene'])
        _BG[key] = im
        return im
    y = np.linspace(0, 1, H)[:, None, None]
    arr = (np.array(th['top'])[None, None] * (1 - y) + np.array(th['bot'])[None, None] * y) * np.ones((1, W, 1))
    im = Image.fromarray(arr.astype(np.uint8))
    d = ImageDraw.Draw(im, 'RGBA')
    if th.get('rainbow'):
        cols = [(244, 67, 54), (255, 152, 0), (255, 235, 59), (76, 175, 80), (33, 150, 243), (103, 58, 183)]
        cx, cy, R, bw = L['rb']
        for i, cl in enumerate(cols):
            r = R - i * bw
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=cl + (255,))
        r = R - len(cols) * bw
        lay = Image.fromarray(arr.astype(np.uint8))
        m = Image.new('L', (W, H), 0)
        ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
        im.paste(lay, (0, 0), m)
        d = ImageDraw.Draw(im, 'RGBA')
        for (x, yy, s) in L['clouds']:
            _cloud(d, x, yy, s)
    else:
        rng = np.random.default_rng(sum(ord(ch) * (i + 1) for i, ch in enumerate(theme)) % 9973)
        for _ in range(26 if o == 'h' else 22):
            x, yy, r = rng.uniform(0, W), rng.uniform(0, H * 0.75), rng.uniform(20, 70)
            d.ellipse([x - r, yy - r, x + r, yy + r], fill=(255, 255, 255, 70))
    g = th.get('ground', (140, 215, 105))
    g2 = tuple(max(0, v - 25) for v in g)
    x0, y0, x1, y1 = L['ground']
    d.ellipse([x0, y0, x1, y1], fill=g2 + (255,))
    d.ellipse([x0 + 100, y0 + 30, x1 - 100, y1], fill=g + (255,))
    im = im.convert('RGBA')
    _BG[key] = im
    return im


_SIL = {}


def silhouette(im):
    k = id(im)
    if k not in _SIL:
        a = im.getchannel('A')
        s = Image.new('RGBA', im.size, (55, 50, 95, 0)); s.putalpha(a.point(lambda v: int(v * 0.92)))
        _SIL[k] = s
    return _SIL[k]


def motion(kind, beat, amp):
    """(dx, dy, rot) for a guest's signature movement."""
    ph = beat % 1.0; b = abs(math.sin(math.pi * ph))
    if kind == 'swim':
        return 60 * math.sin(math.pi * beat / 2), -14 * math.sin(math.pi * beat), 8 * math.cos(math.pi * beat / 2)
    if kind == 'walk':
        return 45 * math.sin(math.pi * beat), -b * amp * 0.4, 5 * math.sin(2 * math.pi * beat)
    if kind == 'hop':
        return 0, -b * amp * 1.8, 0
    if kind == 'fly':
        return 40 * math.sin(math.pi * beat / 2), -30 - 25 * math.sin(math.pi * beat), 6 * math.sin(math.pi * beat)
    if kind == 'roll':
        return 40 * math.sin(math.pi * beat / 2), -b * amp * 0.3, 20 * math.sin(math.pi * beat / 2)
    if kind == 'drive':
        return 70 * math.sin(math.pi * beat / 4), -abs(math.sin(2 * math.pi * beat)) * 6, 0
    return 0, -b * amp, 0


def zoom(base, cx, cy, z):
    if z <= 1.001:
        return base
    W, H = base.size
    w, h = W / z, H / z
    x0 = min(max(cx - w / 2, 0), W - w); y0 = min(max(cy - h / 2, 0), H - h)
    return base.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + w, y0 + h))


# ------------------------------------------------------------ lyrics
def draw_lyrics(o, base, sec, beat, col):
    L = LAY[o]; W = L['W']
    rel = beat - sec['start']
    li = int(rel // 8)
    if li < 0 or li >= len(sec['lines']):
        return
    line = sec['lines'][li]
    lb = sec['start'] + 8 * li
    starts = []; bb = lb
    for p, dd in line['notes']:
        if p != 'r':
            starts.append(bb)
        bb += dd
    pieces = [s.replace('_', ' ') for s in line['syl']]
    sz = L['lyr_font']
    f = font(sz)
    widths = [f.getlength(p) for p in pieces]
    rows = [list(range(len(pieces)))]
    if sum(widths) > L['lyr_max']:
        sz2 = int(sz * L['lyr_max'] / sum(widths))
        if sz2 >= sz * 0.8:
            sz = sz2
        else:  # wrap into two rows at the word boundary nearest the middle
            ends = [i for i, p in enumerate(pieces) if p.endswith(' ')]
            half = sum(widths) / 2; acc = 0; best = None
            for i, w in enumerate(widths):
                acc += w
                if i in ends and (best is None or abs(acc - half) < abs(best[1] - half)):
                    best = (i, acc)
            cut = best[0] + 1 if best else len(pieces) // 2
            rows = [list(range(cut)), list(range(cut, len(pieces)))]
            sz = min(sz, int(sz * L['lyr_max'] / max(sum(widths[:cut]), sum(widths[cut:]))))
        f = font(sz)
        widths = [f.getlength(p) for p in pieces]
    lh = int(sz * 1.25)
    box_w = max(sum(widths[i] for i in r) for r in rows) + 120
    box_h = lh * len(rows) + 50
    top = L['lyr_top']
    lay = Image.new('RGBA', base.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay, 'RGBA')
    ld.rounded_rectangle([W / 2 - box_w / 2, top, W / 2 + box_w / 2, top + box_h], radius=40, fill=(255, 255, 255, 232), outline=col + (255,), width=6)
    base.alpha_composite(lay)
    d = ImageDraw.Draw(base, 'RGBA')
    centers = {}
    for ri, r in enumerate(rows):
        x = W / 2 - sum(widths[i] for i in r) / 2
        y = top + 25 + lh * ri + lh / 2
        for i in r:
            sung = beat >= starts[i]
            d.text((x, y), pieces[i], font=f, fill=col if sung else (90, 90, 100), anchor='lm')
            centers[i] = (x + f.getlength(pieces[i].rstrip()) / 2, y - lh / 2)
            x += widths[i]
    if beat < starts[0]:
        i, u = 0, 0.0
        (bx, by0), hop = centers[0], 0.0
    else:
        i = max(k for k in range(len(starts)) if starts[k] <= beat)
        if i + 1 < len(starts) and centers[i + 1][1] == centers[i][1]:
            u = (beat - starts[i]) / (starts[i + 1] - starts[i])
            bx = centers[i][0] + (centers[i + 1][0] - centers[i][0]) * u
            by0 = centers[i][1]; hop = math.sin(math.pi * u)
        else:
            u = min((beat - starts[i]) / 1.0, 1)
            bx, by0 = centers[i]; hop = math.sin(math.pi * u) * 0.5
    yy = by0 + 12 - hop * 40
    d.ellipse([bx - 15, yy - 15, bx + 15, yy + 15], fill=col + (255,), outline='white', width=4)


# ------------------------------------------------------------ frame
def frame(o, si, t):
    sec = SECTIONS[si]
    L = LAY[o]
    beat = t / BEAT
    rel = beat - sec['start']
    ph = beat % 1.0
    bounce = abs(math.sin(math.pi * ph))
    kind = sec['kind']
    theme = sec['theme']
    if kind == 'verse':
        theme = T.VERSES[VIDX[si]].get('theme', theme)
    th = T.THEMES[theme]
    base = background(o, theme).copy()
    d = ImageDraw.Draw(base, 'RGBA')
    sing = talking(t)
    col = th['col']

    if kind == 'verse':
        v = T.VERSES[VIDX[si]]
        scene_fx(o, base, theme, t)
        hx, hy, hs = L['host']
        li = int(rel // 8)
        action = (li == ACTION_LINE)
        r0, r1 = REVEAL_AT if REVEAL else (-1, -0.5)
        # Tavo: opens his case, listens ("?") during the guess pause, joins the action line
        case_open = rel < 2.0
        if action:
            tdx, tdy, trot = 0, -abs(math.sin(math.pi * ph)) * 38, 9 * math.sin(math.pi * beat)
        else:
            tdx, tdy, trot = 0, -bounce * 8, 0
        paste(base, spr('tavo', sing, blink(t, 2), hs, case_open=case_open), hx + tdx, hy + tdy, 1, 1, trot)
        if o == 'h':   # Rubbo + Lino watch from the right and join the action
            for k, (nm, x, y, sz) in enumerate([('rubbo', 1770, 770, 200), ('lino', 1620, 740, 230)]):
                bb = abs(math.sin(math.pi * (beat + k * 0.5))) * (30 if action else 6)
                paste(base, spr(nm, False, blink(t, 6 + k), sz), x, y - bb, 1, 1, (7 * math.sin(math.pi * beat + k)) if action else 0)
        u = min(max(rel / 1.0, 0), 1)
        gx0, gy0 = hx, hy + hs * 0.1
        gx, gy, gs = L['guest']
        e = ease_back(u)
        cx_ = gx0 + (gx - gx0) * min(1, e); cy_ = gy0 + (gy - gy0) * min(1, e)
        amp = 55 if action else 30
        sq = 1 + 0.06 * math.cos(2 * math.pi * ph)
        sc = (0.15 + 0.85 * e) * (1.08 if action else 1.0)
        mv = v.get('motion', 'bounce')
        if u >= 1 and rel >= r1:
            mdx, mdy, mrot = motion(mv, beat, amp)
            if action:
                mrot += 6 * math.sin(math.pi * beat)
        else:
            mdx, mdy, mrot = 0, -(bounce * 10 if u >= 1 else 0), 0
        g = spr(v['guest'], sing and rel >= r1, blink(t, 1), gs)
        if abs(sc / sq - 1) > 1e-3 or abs(sc * sq - 1) > 1e-3:
            g = g.resize((max(1, int(g.width * sc / sq)), max(1, int(g.height * sc * sq))), Image.BILINEAR)
        if mrot:
            g = g.rotate(mrot, resample=Image.BILINEAR, expand=True)
        px, py = cx_ + mdx, cy_ + mdy
        if rel < r0:                                   # guess: only a silhouette
            paste(base, silhouette(g), px, py)
        elif rel < r1:                                 # Rosy colours it in, left -> right
            w = (rel - r0) / (r1 - r0)
            sil = silhouette(g).copy()
            colr = g.copy()
            cut = int(colr.width * w)
            m = Image.new('L', colr.size, 0); ImageDraw.Draw(m).rectangle([0, 0, cut, colr.height], fill=255)
            sil.paste(colr, (0, 0), Image.composite(colr.getchannel('A'), Image.new('L', colr.size, 0), m))
            paste(base, sil, px, py)
            rx = px - colr.width / 2 + cut
            ry = py - colr.height * 0.15 + colr.height * 0.25 * math.sin(w * math.pi * 6)
            paste(base, spr('rosy', True, False, int(gs * 0.55)), rx + gs * 0.12, ry - gs * 0.12, 1, 1, -35)
            dd = ImageDraw.Draw(base, 'RGBA')
            for k in range(4):
                a = k * 1.7 + rel * 5
                star(dd, rx + 50 * math.cos(a), ry + 50 * math.sin(a), 16, (255, 215, 0, 220))
        else:
            paste(base, g, px, py)
        d = ImageDraw.Draw(base, 'RGBA')
        wx, wy, wsz = L['word']
        if rel < r1 and REVEAL:
            text(d, wx, wy, '?', wsz * min(1, ease_back(rel / 1.2)) * (1 + 0.08 * math.sin(math.pi * beat)), col, stroke=12)
            if 1.0 < rel < r0:   # Tavo's thinking bubble
                bx_, by_ = hx + hs * 0.42, hy - hs * 0.62
                d.ellipse([bx_ - 48, by_ - 48, bx_ + 48, by_ + 48], fill=(255, 255, 255, 235), outline=col + (255,), width=5)
                d.ellipse([bx_ - 70, by_ + 52, bx_ - 52, by_ + 70], fill=(255, 255, 255, 235))
                text(d, bx_, by_ + 2, '?', 70, col, stroke=0)
        else:
            text(d, wx, wy, v['word'], wsz * min(1, ease_back((rel - (r1 if REVEAL else 0)) / 1.2)) * (1 + 0.05 * (1 - ph) ** 3), col, stroke=12)
        # collected guests
        prev = [T.VERSES[k]['guest'] for k in range(VIDX[si])]
        if o == 'h':
            for k, gg in enumerate(prev):
                paste(base, spr(gg, False, False, 130), L['W'] - 110 - k * 120, 110)
        else:
            n = len(prev)
            for k, gg in enumerate(prev):
                paste(base, spr(gg, False, False, 110), L['W'] / 2 + (k - (n - 1) / 2) * 115, 385)
        if action:
            d = ImageDraw.Draw(base, 'RGBA')
            R = gs * 0.62
            for k in range(6):
                a = k * math.pi / 3 + beat * 0.8
                r = R + 20 * math.sin(beat * math.pi)
                star(d, gx + r * math.cos(a), gy + r * 0.75 * math.sin(a), 26, (255, 215, 0, 230))
        # slow push-in towards the guest (reflective "camera zoom", no cuts)
        z = 1.0 + 0.06 * min(1, max(0, rel - 1) / 30.0)
        base = zoom(base, gx, gy, z)
        draw_lyrics(o, base, sec, beat, col)

    elif kind in ('chorus', 'outro'):
        scene_fx(o, base, theme, t)
        n = len(GUEST_ORDER)
        if o == 'h':
            gsz = L['ch_guest_size'] if n <= 4 else 260
            span = 1100
            pos = [(960 + (k - (n - 1) / 2) * (span / max(1, n - 1) if n > 1 else 0), L['ch_guest_y']) for k in range(n)]
        else:
            gsz = L['ch_guest_size'] if n <= 4 else 260
            grid = L['ch_grid']
            pos = grid.get(n, grid[5])[:n]
        for k, g in enumerate(GUEST_ORDER[:len(pos)]):
            p2 = (beat + k * 0.5) % 1.0
            bb = abs(math.sin(math.pi * p2))
            rot = 8 * math.sin(math.pi * (beat + k * 0.5))
            paste(base, spr(g, sing, blink(t, k), gsz), pos[k][0], pos[k][1] - bb * 40, 1, 1, rot)
        hx, hy, hs = L['ch_host']
        paste(base, spr('tavo', sing, blink(t, 2), hs), hx, hy - bounce * 25, 1, 1, 5 * math.sin(math.pi * beat))
        rx, ry, rs = L['ch_rosy']
        paste(base, spr('rosy', sing, blink(t, 5), rs), rx, ry - abs(math.sin(math.pi * (beat + 0.5))) * 25)
        d = ImageDraw.Draw(base, 'RGBA')
        wx, wy, wsz = L['word']
        title = T.CHORUS_TITLE if kind == 'chorus' else T.OUTRO_TITLE
        text(d, wx, wy, title, wsz * 0.78 * (1 + 0.04 * (1 - ph) ** 3), col, stroke=12)
        draw_lyrics(o, base, sec, beat, col)

    elif kind == 'intro':
        scene_fx(o, base, theme, t)
        tx, ty, ts = L['intro_tavo']
        open_ = rel >= 3.5
        wave = 1.0 <= rel < 3.5
        paste(base, spr('tavo', sing, blink(t, 2), ts, case_open=open_, wave=wave), tx, ty - bounce * 18)
        for k, (nm, x, y, s) in enumerate(L['intro_crew']):
            a = ease_back((rel - 4 - k * 1.0) / 1.0)
            if s and a > 0.02:
                bb = abs(math.sin(math.pi * (beat + k * 0.33)))
                paste(base, spr(nm, sing and rel > 12, blink(t, k + 3), s), x, y - bb * 20, a, a)
        d = ImageDraw.Draw(base, 'RGBA')
        lx, ly, lsz = L['logo']
        a = ease_back(rel / 1.2)
        text(d, lx, ly, 'Sing with Tavo', lsz * a, (30, 120, 220), stroke=10)
        x, y, s = L['title']
        text(d, x, y, T.TITLE, s * ease_back((rel - 0.5) / 1.2), (216, 27, 96), stroke=14)
        if rel > 8:
            nx, ny, ns = L['note']
            text(d, nx, ny, "Let's sing along!", ns * ease_back((rel - 8) / 1.0), (30, 120, 220), stroke=10)
        bx, by, bs = L['brand']
        text(d, bx, by, 'Baby Collective', bs, (90, 90, 110), stroke=6)

    elif kind == 'end':
        scene_fx(o, base, theme, t)
        tx, ty, ts = L['end_tavo']
        paste(base, spr('tavo', sing, blink(t, 2), ts, wave=True), tx, ty, 1, 1, 4 * math.sin(2 * math.pi * beat * 0.5))
        row = ['rosy', 'rubbo', 'lino'] + GUEST_ORDER[:1]
        for k, nm in enumerate(row):
            x, y = L['end_row'][k]
            wv = 10 * math.sin(2 * math.pi * (beat * 0.5 + k * 0.25))
            paste(base, spr(nm, sing, blink(t, k), L['end_size']), x, y, 1, 1, wv)
        d = ImageDraw.Draw(base, 'RGBA')
        x, y, s = L['end_title']
        text(d, x, y, 'Bye bye!', s * ease_back(rel / 1.2), (216, 27, 96), stroke=14)
        nx, ny, ns = L['note']
        text(d, nx, ny, 'See you next time!', ns * ease_back((rel - 1) / 1.2), (30, 120, 220), stroke=10)
    return base.convert('RGB')


def section_at(t):
    b = t / BEAT
    return max(i for i, s in enumerate(SECTIONS) if s['start'] <= b + 1e-9)


def sec_frames(i):
    f0 = round(SECTIONS[i]['start'] * BEAT * FPS)
    f1 = round(SECTIONS[i + 1]['start'] * BEAT * FPS) if i + 1 < len(SECTIONS) else round((TOTAL_BEATS * BEAT + TAIL) * FPS)
    return f0, f1


# ------------------------------------------------------------ rendering
def _segment(args):
    o, si, F0, F1, path, fade_last = args
    L = LAY[o]
    tmp = path + '.tmp.mp4'
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f"{L['W']}x{L['H']}", '-r', str(FPS), '-i', '-']
    if fade_last:
        cmd += ['-vf', f'fade=t=out:st={(F1 - F0) / FPS - 1.0:.3f}:d=1.0']
    cmd += ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-g', '60', tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(F0, F1):
        p.stdin.write(frame(o, si, fi / FPS).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise SystemExit('ffmpeg failed for ' + path)
    os.replace(tmp, path)
    return path


def render_range(o, t0, t1, out, workers=2):
    F0, F1 = round(t0 * FPS), round(t1 * FPS)
    jobs = []
    last = len(SECTIONS) - 1
    for i in range(len(SECTIONS)):
        a, b = sec_frames(i)
        a, b = max(a, F0), min(b, F1)
        if b > a:
            jobs.append((o, i, a, b, f'seg_{o}_{i:02d}.mp4', o == 'h' and i == last and b == sec_frames(i)[1]))
    with Pool(workers) as pool:
        paths = pool.map(_segment, jobs)
    with open(f'list_{o}.txt', 'w') as fh:
        fh.writelines(f"file '{p}'\n" for p in paths)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'list_{o}.txt', '-c', 'copy', out], check=True)
    return out


def final(out, max_mb=24):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'video_h.mp4', '-i', 'final_audio.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], check=True)
    src = out + '.src.mp4'
    for crf in (25, 28, 31):          # keep uploads small enough for GitHub raw + browser transfer
        if os.path.getsize(out) <= max_mb * 1e6:
            break
        if not os.path.exists(src):
            os.replace(out, src)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-c:v', 'libx264', '-preset', 'medium', '-crf', str(crf), '-tune', 'animation', '-pix_fmt', 'yuv420p',
                        '-c:a', 'copy', '-movflags', '+faststart', out], check=True)
    if os.path.exists(src):
        os.remove(src)
    print(f'{out}: {os.path.getsize(out) / 1e6:.1f} MB')


def short(t0, dur, out):
    render_range('v', t0, t0 + dur, 'video_v.mp4')
    fo = dur - 0.7
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'video_v.mp4', '-ss', f'{t0:.3f}', '-t', f'{dur:.3f}', '-i', 'final_audio.wav',
                    '-map', '0:v', '-map', '1:a', '-vf', f'fade=t=in:st=0:d=0.3,fade=t=out:st={fo:.3f}:d=0.7',
                    '-af', f'afade=t=in:st=0:d=0.3,afade=t=out:st={dur - 0.9:.3f}:d=0.9,loudnorm=I=-14:TP=-1.5:LRA=11',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-ar', '48000', '-c:a', 'aac', '-b:a', '160k',
                    '-shortest', '-movflags', '+faststart', out], check=True)


def thumb(out):
    o = 'h'; L = LAY[o]
    theme = T.THUMB.get('theme', 'title')
    base = background(o, theme).copy()
    paste(base, spr('tavo', True, False, 700, case_open=True, wave=True), 470, 600)
    lines = T.THUMB.get('lines', [T.TITLE])
    d = ImageDraw.Draw(base, 'RGBA')
    sz = 150 if max(len(s) for s in lines) <= 11 else 120
    for k, s in enumerate(lines):
        text(d, 1300, 300 + k * (sz + 20), s, sz, (216, 27, 96), stroke=16)
    gs = GUEST_ORDER[:4]
    for k, g in enumerate(gs):
        paste(base, spr(g, False, False, 230), 1300 + (k - (len(gs) - 1) / 2) * 230, 300 + len(lines) * (sz + 20) + 120)
    d = ImageDraw.Draw(base, 'RGBA')
    d.rounded_rectangle([40, 36, 520, 126], radius=45, fill=(30, 120, 220, 255))
    d.text((280, 81), 'Sing with Tavo', font=font(56), fill='white', anchor='mm')
    base.convert('RGB').resize((1280, 720), Image.LANCZOS).save(out, quality=92)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == 'still':
        o, t = a[1], float(a[2])
        frame(o, section_at(t), t).save(a[3], quality=90)
    elif a[0] == 'render':
        render_range('h', 0, TOTAL_BEATS * BEAT + TAIL, 'video_h.mp4')
    elif a[0] == 'final':
        final(a[1])
    elif a[0] == 'short':
        short(float(a[1]), float(a[2]), a[3])
    elif a[0] == 'thumb':
        thumb(a[1])
    elif a[0] == 'chorus_starts':
        for s in SECTIONS:
            if s['kind'] == 'chorus':
                print(f"{s['name']}: {s['start'] * BEAT:.2f}s  ({s['beats'] * BEAT:.1f}s long)")
    else:
        print(__doc__)
