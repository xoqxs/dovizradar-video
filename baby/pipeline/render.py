import math, sys, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from song import *

W, H, FPS = 1920, 1080, 30
FONT = '/home/claude/build/Fredoka-Bold.ttf'
_fc = {}
def font(sz):
    if sz not in _fc: _fc[sz] = ImageFont.truetype(FONT, sz)
    return _fc[sz]

THEMES = {
    'red':    dict(top=(255, 232, 232), bot=(255, 186, 186), word='RED', col=(229, 57, 53), fruit='apple'),
    'yellow': dict(top=(255, 250, 220), bot=(255, 226, 140), word='YELLOW', col=(240, 165, 0), fruit='banana'),
    'green':  dict(top=(232, 250, 228), bot=(178, 232, 170), word='GREEN', col=(56, 160, 60), fruit='grapes'),
    'blue':   dict(top=(228, 242, 255), bot=(170, 212, 255), word='BLUE', col=(30, 120, 220), fruit='blueberry'),
    'rainbow': dict(top=(170, 222, 255), bot=(232, 248, 255), col=(216, 27, 96)),
    'title':  dict(top=(170, 222, 255), bot=(232, 248, 255), col=(216, 27, 96)),
    'end':    dict(top=(170, 222, 255), bot=(232, 248, 255), col=(216, 27, 96)),
}
FRUIT_ORDER = ['apple', 'banana', 'grapes', 'blueberry']

# ---------------- sprites (drawn at 2x, downsampled) ----------------
def face(d, cx, cy, s, mouth_open, blink):
    ex = 0.36 * s; er = 0.17 * s
    for sx in (-1, 1):
        x = cx + sx * ex
        if blink:
            d.arc([x - er, cy - er * 0.6, x + er, cy + er * 0.9], 200, 340, fill=(40, 30, 30), width=int(s * 0.05))
        else:
            d.ellipse([x - er, cy - er * 1.15, x + er, cy + er * 1.15], fill='white', outline=(40, 30, 30), width=int(s * 0.025))
            pr = er * 0.62
            d.ellipse([x - pr, cy - pr * 0.9, x + pr, cy + pr * 1.3], fill=(40, 30, 30))
            g = pr * 0.4
            d.ellipse([x - pr * 0.3 - g, cy - pr * 0.5 - g, x - pr * 0.3 + g, cy - pr * 0.5 + g], fill='white')
        # cheeks
        d.ellipse([x + sx * er * 0.6 - er * 0.75, cy + er * 1.5, x + sx * er * 0.6 + er * 0.75, cy + er * 2.3], fill=(255, 150, 165))
    my = cy + 0.38 * s; mw = 0.26 * s
    if mouth_open:
        d.ellipse([cx - mw * 0.75, my - mw * 0.35, cx + mw * 0.75, my + mw * 0.95], fill=(120, 20, 40))
        d.ellipse([cx - mw * 0.45, my + mw * 0.35, cx + mw * 0.45, my + mw * 0.9], fill=(255, 120, 140))
    else:
        d.arc([cx - mw, my - mw * 0.9, cx + mw, my + mw * 0.6], 20, 160, fill=(60, 20, 30), width=int(s * 0.05))

def sprite(kind, mouth_open=False, blink=False, size=440):
    S = size * 2
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im, 'RGBA')
    c = S / 2
    if kind == 'apple':
        r = S * 0.38
        d.ellipse([c - r * 1.02, c - r * 0.82, c + r * 0.12, c + r], fill=(226, 45, 45))
        d.ellipse([c - r * 0.12, c - r * 0.82, c + r * 1.02, c + r], fill=(226, 45, 45))
        d.ellipse([c - r * 0.85, c - r * 0.6, c + r * 0.85, c + r * 1.0], fill=(226, 45, 45))
        d.ellipse([c - r * 0.7, c - r * 0.6, c - r * 0.35, c - r * 0.25], fill=(255, 150, 150))
        d.rounded_rectangle([c - S * 0.018, c - r * 1.2, c + S * 0.018, c - r * 0.6], radius=10, fill=(110, 70, 40))
        d.ellipse([c + S * 0.01, c - r * 1.25, c + r * 0.6, c - r * 0.92], fill=(76, 175, 80))
        face(d, c, c + r * 0.1, r * 1.05, mouth_open, blink)
    elif kind == 'banana':
        cx0, cy0, R, W0 = c, c - 0.32 * S, 0.5 * S, 0.27 * S
        outer, inner = [], []
        for k in range(61):
            a = math.radians(18 + 144 * k / 60)
            w = W0 * max(math.sin(math.pi * k / 60), 0) ** 0.6 + 6
            outer.append((cx0 + (R + w / 2) * math.cos(a), cy0 + (R + w / 2) * math.sin(a)))
            inner.append((cx0 + (R - w / 2) * math.cos(a), cy0 + (R - w / 2) * math.sin(a)))
        d.polygon(outer + inner[::-1], fill=(255, 214, 40), outline=(220, 170, 20), width=8)
        for k in (2, 58):
            a = math.radians(18 + 144 * k / 60)
            x, y = cx0 + R * math.cos(a), cy0 + R * math.sin(a)
            d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=(110, 80, 30))
        face(d, c, cy0 + R - 0.05 * S, S * 0.24, mouth_open, blink)
    elif kind == 'grapes':
        gr = S * 0.105
        rows = [(-0.3, [-1.5, -0.5, 0.5, 1.5]), (-0.05, [-1, 0, 1]), (0.2, [-1.5, -0.5, 0.5, 1.5]), (0.4, [-0.5, 0.5])]
        for ry, xs in rows:
            for xx in xs:
                x, y = c + xx * gr * 1.9, c + ry * S
                d.ellipse([x - gr, y - gr, x + gr, y + gr], fill=(110, 190, 70), outline=(70, 140, 45), width=4)
                d.ellipse([x - gr * 0.55, y - gr * 0.6, x - gr * 0.15, y - gr * 0.2], fill=(200, 240, 170))
        d.rounded_rectangle([c - 10, c - S * 0.47, c + 10, c - S * 0.36], radius=6, fill=(110, 70, 40))
        d.ellipse([c + 5, c - S * 0.48, c + S * 0.2, c - S * 0.38], fill=(56, 142, 60))
        # face on a bigger front grape
        fr = S * 0.21
        d.ellipse([c - fr, c - fr + S * 0.02, c + fr, c + fr + S * 0.02], fill=(124, 204, 80), outline=(70, 140, 45), width=5)
        face(d, c, c + S * 0.0, fr * 1.15, mouth_open, blink)
    elif kind == 'blueberry':
        for ox, oy, rr in [(-0.27, 0.2, 0.13), (0.29, 0.22, 0.12)]:
            x, y, r = c + ox * S, c + oy * S, rr * S
            d.ellipse([x - r, y - r, x + r, y + r], fill=(60, 90, 190))
            d.ellipse([x - r * 0.6, y - r * 0.6, x - r * 0.2, y - r * 0.2], fill=(140, 170, 240))
        r = S * 0.3
        d.ellipse([c - r, c - r, c + r, c + r], fill=(70, 100, 205))
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            rr = r * (0.2 if k % 2 == 0 else 0.09)
            pts.append((c + rr * math.cos(a), c - r * 0.85 + rr * math.sin(a)))
        d.polygon(pts, fill=(35, 45, 110))
        d.ellipse([c - r * 0.7, c - r * 0.6, c - r * 0.35, c - r * 0.25], fill=(150, 180, 245))
        face(d, c, c + r * 0.12, r * 1.05, mouth_open, blink)
    elif kind == 'lunchbox':
        bw, bh = S * 0.7, S * 0.42
        x0, y0 = c - bw / 2, c - bh / 2 + S * 0.08
        d.rounded_rectangle([c - S * 0.12, y0 - S * 0.14, c + S * 0.12, y0 + 10], radius=30, outline=(60, 60, 80), width=22)
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=50, fill=(255, 120, 60), outline=(200, 80, 30), width=10)
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh * 0.3], radius=50, fill=(255, 170, 60), outline=(200, 80, 30), width=10)
        d.rounded_rectangle([c - 30, y0 + bh * 0.22, c + 30, y0 + bh * 0.36], radius=10, fill=(255, 230, 120))
        face(d, c, y0 + bh * 0.58, bh * 0.55, mouth_open, blink)
    im = im.resize((size, size), Image.LANCZOS)
    return im

SPR = {}
def spr(kind, mo=False, bl=False, size=440):
    k = (kind, mo, bl, size)
    if k not in SPR: SPR[k] = sprite(kind, mo, bl, size)
    return SPR[k]

# ---------------- backgrounds ----------------
BG = {}
def background(theme):
    if theme in BG: return BG[theme]
    th = THEMES[theme]
    y = np.linspace(0, 1, H)[:, None, None]
    a = np.array(th['top'])[None, None]; b = np.array(th['bot'])[None, None]
    arr = (a * (1 - y) + b * y) * np.ones((1, W, 1))
    im = Image.fromarray(arr.astype(np.uint8))
    d = ImageDraw.Draw(im, 'RGBA')
    if theme in ('rainbow', 'title', 'end'):
        cols = [(244, 67, 54), (255, 152, 0), (255, 235, 59), (76, 175, 80), (33, 150, 243), (103, 58, 183)]
        cx, cy, R, bw = W / 2, 980, 900, 48
        for i, cl in enumerate(cols):
            r = R - i * bw
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=cl + (255,))
        r = R - len(cols) * bw
        lay = Image.fromarray(arr.astype(np.uint8))
        m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
        im.paste(lay, (0, 0), m)
        d = ImageDraw.Draw(im, 'RGBA')
        for (x, yy, s) in [(260, 210, 1.0), (1650, 160, 1.2), (1500, 420, 0.7), (400, 470, 0.8)]:
            for dx, dy, rr in [(0, 0, 70), (70, 15, 55), (-70, 15, 55), (35, -35, 55)]:
                d.ellipse([x + dx * s - rr * s, yy + dy * s - rr * s, x + dx * s + rr * s, yy + dy * s + rr * s], fill=(255, 255, 255, 235))
    else:
        rng = np.random.default_rng(len(theme))
        for _ in range(26):
            x, yy, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(20, 70)
            d.ellipse([x - r, yy - r, x + r, yy + r], fill=(255, 255, 255, 70))
    # grass hill
    d.ellipse([-300, 760, W + 300, 1500], fill=(120, 200, 90, 255))
    d.ellipse([-200, 790, W + 200, 1500], fill=(140, 215, 105, 255))
    im = im.convert('RGBA')
    BG[theme] = im
    return im

# ---------------- helpers ----------------
def ease_back(u):
    u = min(max(u, 0), 1); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (u - 1) ** 3 + c1 * (u - 1) ** 2

def paste_center(base, im, cx, cy, sx=1.0, sy=1.0, rot=0):
    if sx <= 0.01 or sy <= 0.01: return
    w, h = im.size
    if abs(sx - 1) > 1e-3 or abs(sy - 1) > 1e-3:
        im = im.resize((max(1, int(w * sx)), max(1, int(h * sy))), Image.BILINEAR)
    if rot: im = im.rotate(rot, resample=Image.BILINEAR, expand=True)
    base.alpha_composite(im, (int(cx - im.size[0] / 2), int(cy - im.size[1] / 2)))

def text_center(d, x, y, s, sz, fill, stroke=8, sfill='white'):
    if sz < 4: return
    f = font(sz)
    d.text((x, y), s, font=f, fill=fill, anchor='mm', stroke_width=stroke, stroke_fill=sfill)

def star(d, x, y, r, col):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    d.polygon(pts, fill=col)

NOTES, _ = events()
NOTE_STARTS = [(b, b + d) for b, d, *_ in NOTES]
def singing(beat):
    for b0, b1 in NOTE_STARTS:
        if b0 <= beat < b0 + (b1 - b0) * 0.85: return True
    return False

ENV = np.load('/home/claude/build/voice_env.npy')
def talking(t):
    i = int(t * FPS)
    return i < len(ENV) and ENV[i] > 0.12

def blink(t, seed):
    p = (t + seed * 1.37) % 3.3
    return p < 0.12

# ---------------- lyrics ----------------
def draw_lyrics(base, sec, beat, col):
    rel = beat - sec['start']
    li = int(rel // 8)
    if li < 0 or li >= len(sec['lines']): return
    line = sec['lines'][li]
    lb = sec['start'] + 8 * li
    starts = []; bb = lb
    for p, dd in line['notes']:
        if p != 'r': starts.append(bb)
        bb += dd
    pieces = [s.replace('_', ' ') for s in line['syl']]
    sz = 84
    f = font(sz)
    widths = [f.getlength(p) for p in pieces]
    tot = sum(widths)
    box = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(box, 'RGBA')
    bw = tot + 140
    d.rounded_rectangle([W / 2 - bw / 2, 880, W / 2 + bw / 2, 1030], radius=40, fill=(255, 255, 255, 230), outline=col + (255,), width=6)
    base.alpha_composite(box)
    d = ImageDraw.Draw(base, 'RGBA')
    x = W / 2 - tot / 2; y = 962
    centers = []
    for i, (p, w) in enumerate(zip(pieces, widths)):
        sung = beat >= starts[i]
        fill = col if sung else (90, 90, 100)
        d.text((x, y), p, font=f, fill=fill, anchor='lm')
        centers.append(x + f.getlength(p.rstrip()) / 2)
        x += w
    # bouncing ball
    if beat < starts[0]:
        bx, by = centers[0], 0.0
    else:
        i = max(k for k in range(len(starts)) if starts[k] <= beat)
        if i + 1 < len(starts):
            u = (beat - starts[i]) / (starts[i + 1] - starts[i])
            bx = centers[i] + (centers[i + 1] - centers[i]) * u
            by = math.sin(math.pi * u)
        else:
            u = min((beat - starts[i]) / 1.0, 1)
            bx, by = centers[i], math.sin(math.pi * min(u, 1)) * 0.5
    yy = 895 - by * 45
    d.ellipse([bx - 16, yy - 16, bx + 16, yy + 16], fill=col + (255,), outline='white', width=4)

# ---------------- frame ----------------
def frame(sec, t):
    beat = t / BEAT
    rel = beat - sec['start']
    ph = beat % 1.0
    bounce = abs(math.sin(math.pi * ph))
    th = THEMES[sec['theme']]
    base = background(sec['theme']).copy()
    d = ImageDraw.Draw(base, 'RGBA')
    sing = talking(t)
    kind = sec['kind']

    if kind == 'verse':
        fruit = th['fruit']
        app = ease_back(rel / 1.2)
        # color word
        ws = 1 + 0.05 * (1 - ph) ** 3
        text_center(d, W / 2, 150, th['word'], int(170 * ws * min(1, app + 0.0001)), th['col'], stroke=12)
        # collected fruits top-right
        idx = FRUIT_ORDER.index(fruit)
        for k in range(idx):
            paste_center(base, spr(FRUIT_ORDER[k], size=130), W - 110 - k * 120, 110)
        # lunchbox left
        paste_center(base, spr('lunchbox', False, blink(t, 3), 360), 300, 650 - bounce * 10)
        # fruit
        li = int(rel // 8)
        yum = (li == 2)
        amp = 55 if yum else 30
        sq = 1 + 0.06 * math.cos(2 * math.pi * ph)
        sc = app * (1.08 if yum else 1.0)
        rot = 6 * math.sin(math.pi * beat) if yum else 0
        paste_center(base, spr(fruit, sing, blink(t, 1)), W / 2, 560 - bounce * amp, sc / sq, sc * sq, rot)
        if yum:
            d = ImageDraw.Draw(base, 'RGBA')
            for k in range(6):
                a = k * math.pi / 3 + beat * 0.8
                r = 270 + 20 * math.sin(beat * math.pi)
                star(d, W / 2 + r * math.cos(a), 560 + r * 0.75 * math.sin(a), 26, (255, 215, 0, 230))
        draw_lyrics(base, sec, beat, th['col'])

    elif kind in ('chorus', 'outro'):
        xs = [420, 780, 1140, 1500]
        for k, fr in enumerate(FRUIT_ORDER):
            p2 = (beat + k * 0.5) % 1.0
            bb = abs(math.sin(math.pi * p2))
            rot = 8 * math.sin(math.pi * (beat + k * 0.5))
            paste_center(base, spr(fr, sing, blink(t, k), 330), xs[k], 560 - bb * 45, 1, 1, rot)
        d = ImageDraw.Draw(base, 'RGBA')
        ws = 1 + 0.04 * (1 - ph) ** 3
        title = 'Colors, colors!' if kind == 'chorus' else 'Healthy colors!'
        text_center(d, W / 2, 150, title, int(130 * ws), (216, 27, 96), stroke=12)
        draw_lyrics(base, sec, beat, (216, 27, 96))

    elif kind == 'intro':
        u = rel / 16
        paste_center(base, spr('lunchbox', sing, blink(t, 2), 520), W / 2, 600 - bounce * 25)
        for k, fr in enumerate(FRUIT_ORDER):
            a = ease_back((rel - 2 - k * 1.5) / 1.0)
            x = [260, 600, 1320, 1660][k]
            paste_center(base, spr(fr, False, blink(t, k), 260), x, 640 - abs(math.sin(math.pi * (beat + k * 0.5))) * 30, a, a)
        d = ImageDraw.Draw(base, 'RGBA')
        ta = ease_back(rel / 1.5)
        text_center(d, W / 2, 175, 'Colors in My Lunchbox', max(1, int(130 * ta)), (216, 27, 96), stroke=14)
        if rel > 8:
            a = min(1, (rel - 8) / 1)
            text_center(d, W / 2, 960, "Let's sing along!", int(80 * ease_back(a)) or 1, (30, 120, 220), stroke=10)
        text_center(d, W / 2, 290, 'Baby Collective', 52, (90, 90, 110), stroke=6)

    elif kind == 'end':
        xs = [420, 780, 1140, 1500]
        for k, fr in enumerate(FRUIT_ORDER):
            wv = 10 * math.sin(2 * math.pi * (beat * 0.5 + k * 0.25))
            paste_center(base, spr(fr, sing, blink(t, k), 330), xs[k], 560, 1, 1, wv)
        d = ImageDraw.Draw(base, 'RGBA')
        a = ease_back(rel / 1.2)
        text_center(d, W / 2, 180, 'Bye bye!', max(1, int(170 * a)), (216, 27, 96), stroke=14)
        text_center(d, W / 2, 950, 'See you next time!', max(1, int(80 * ease_back((rel - 1) / 1.2))), (30, 120, 220), stroke=10)
    return base.convert('RGB')

def sec_frames(i):
    s = SECTIONS[i]
    f0 = round(s['start'] * BEAT * FPS)
    if i + 1 < len(SECTIONS): f1 = round(SECTIONS[i + 1]['start'] * BEAT * FPS)
    else: f1 = round((TOTAL_BEATS * BEAT + 2.5) * FPS)
    return f0, f1

def render_section(i):
    s = SECTIONS[i]
    f0, f1 = sec_frames(i)
    out = f'seg_{i:02d}_{s["name"]}.mp4'; tmp = out + '.tmp.mp4'
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-']
    vf = []
    if i == len(SECTIONS) - 1:
        n = f1 - f0
        vf = ['-vf', f'fade=t=out:st={(n / FPS) - 1.0:.3f}:d=1.0']
    cmd += vf + ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-g', '60', tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fi in range(f0, f1):
        p.stdin.write(frame(s, fi / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, out)
    print('done', out, flush=True)

if __name__ == '__main__':
    if sys.argv[1] == 'still':
        t = float(sys.argv[2])
        b = t / BEAT
        s = [x for x in SECTIONS if x['start'] <= b][-1]
        frame(s, t).save(sys.argv[3], quality=90)
    else:
        for i in map(int, sys.argv[1:]): render_section(i)
