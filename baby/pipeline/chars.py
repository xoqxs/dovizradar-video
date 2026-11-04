"""Sing with Tavo – fixed character library (Baby Collective).

DO NOT redesign these characters per video: they are the channel's recurring cast.
Every function returns an RGBA image of size x size (drawn at 2x, downsampled).

  tavo(mouth_open, blink, size, case_open=False, wave=False)  – baby fox host, green scarf, yellow pencil case
  rosy(mouth_open, blink, size)   – pink crayon
  rubbo(mouth_open, blink, size)  – eraser (pink + purple sleeve)
  lino(mouth_open, blink, size)   – wooden ruler

Helpers for topic sprites (use them so every guest matches the house style):
  canvas(S) -> (img, draw)           transparent 2x canvas
  face(d, cx, cy, s, mouth_open, blink)
  finish(img, size)                   downsample to final size
"""
import math
from PIL import Image, ImageDraw

INK = (60, 40, 40)
CHEEK = (255, 150, 165)


def canvas(S):
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im, 'RGBA')


def finish(im, size):
    return im.resize((size, size), Image.LANCZOS)


def face(d, cx, cy, s, mouth_open=False, blink=False, blush=True, mouth_dy=0.0):
    """Standard house face. s = face scale (≈ distance unit)."""
    ex = 0.36 * s
    er = 0.17 * s
    lw = max(2, int(s * 0.03))
    for sx in (-1, 1):
        x = cx + sx * ex
        if blink:
            d.arc([x - er, cy - er * 0.6, x + er, cy + er * 0.9], 200, 340, fill=INK, width=max(3, int(s * 0.05)))
        else:
            d.ellipse([x - er, cy - er * 1.15, x + er, cy + er * 1.15], fill='white', outline=INK, width=lw)
            pr = er * 0.62
            d.ellipse([x - pr, cy - pr * 0.9, x + pr, cy + pr * 1.3], fill=INK)
            g = pr * 0.42
            d.ellipse([x - pr * 0.3 - g, cy - pr * 0.5 - g, x - pr * 0.3 + g, cy - pr * 0.5 + g], fill='white')
        if blush:
            d.ellipse([x + sx * er * 0.6 - er * 0.75, cy + er * 1.5, x + sx * er * 0.6 + er * 0.75, cy + er * 2.3], fill=CHEEK)
    my = cy + 0.38 * s + mouth_dy
    mw = 0.26 * s
    if mouth_open:
        d.ellipse([cx - mw * 0.75, my - mw * 0.35, cx + mw * 0.75, my + mw * 0.95], fill=(120, 20, 40))
        d.ellipse([cx - mw * 0.45, my + mw * 0.35, cx + mw * 0.45, my + mw * 0.9], fill=(255, 120, 140))
    else:
        d.arc([cx - mw, my - mw * 0.9, cx + mw, my + mw * 0.6], 20, 160, fill=(60, 20, 30), width=max(3, int(s * 0.05)))


def limb(d, x0, y0, x1, y1, w, col=INK):
    d.line([x0, y0, x1, y1], fill=col, width=w)
    r = w * 0.9
    d.ellipse([x1 - r, y1 - r, x1 + r, y1 + r], fill=col)


# ---------------------------------------------------------------- Tavo
OR, DK, WH = (245, 130, 50), (90, 50, 40), (255, 248, 238)
SCARF, SCARF_D = (76, 175, 80), (56, 142, 60)
CASE, CASE_D = (255, 205, 60), (220, 165, 30)


def tavo(mouth_open=False, blink=False, size=440, case_open=False, wave=False):
    S = 900
    im, d = canvas(S)
    c = S / 2
    # tail (behind)
    tail = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    td = ImageDraw.Draw(tail, 'RGBA')
    td.ellipse([c + S * 0.10, c + S * 0.08, c + S * 0.46, c + S * 0.30], fill=OR)
    td.ellipse([c + S * 0.34, c + S * 0.12, c + S * 0.47, c + S * 0.26], fill=WH)
    tail = tail.rotate(25, center=(c + S * 0.15, c + S * 0.25), resample=Image.BICUBIC)
    im.alpha_composite(tail)
    d = ImageDraw.Draw(im, 'RGBA')
    # body
    d.rounded_rectangle([c - S * 0.15, c + S * 0.04, c + S * 0.15, c + S * 0.36], radius=70, fill=OR)
    d.ellipse([c - S * 0.09, c + S * 0.10, c + S * 0.09, c + S * 0.33], fill=WH)
    for sx in (-1, 1):
        d.rounded_rectangle([c + sx * S * 0.08 - S * 0.05, c + S * 0.31, c + sx * S * 0.08 + S * 0.05, c + S * 0.40], radius=25, fill=DK)
    # scarf
    d.rounded_rectangle([c - S * 0.17, c + S * 0.03, c + S * 0.17, c + S * 0.10], radius=25, fill=SCARF)
    d.polygon([(c + S * 0.06, c + S * 0.08), (c + S * 0.16, c + S * 0.08), (c + S * 0.13, c + S * 0.19), (c + S * 0.07, c + S * 0.17)], fill=SCARF_D)
    # ears + head
    for sx in (-1, 1):
        d.polygon([(c + sx * S * 0.08, c - S * 0.30), (c + sx * S * 0.27, c - S * 0.42), (c + sx * S * 0.25, c - S * 0.17)], fill=OR)
        d.polygon([(c + sx * S * 0.12, c - S * 0.30), (c + sx * S * 0.245, c - S * 0.38), (c + sx * S * 0.23, c - S * 0.23)], fill=DK)
    d.ellipse([c - S * 0.27, c - S * 0.36, c + S * 0.27, c + S * 0.08], fill=OR)
    d.ellipse([c - S * 0.23, c - S * 0.14, c - S * 0.01, c + S * 0.08], fill=WH)
    d.ellipse([c + S * 0.01, c - S * 0.14, c + S * 0.23, c + S * 0.08], fill=WH)
    d.ellipse([c - S * 0.03, c - S * 0.125, c + S * 0.03, c - S * 0.09], fill=DK)
    face(d, c, c - S * 0.20, S * 0.24, mouth_open, blink, mouth_dy=S * 0.05)
    if wave:  # raised arm in front, paw waving beside the cheek
        d.line([(c + S * 0.13, c + S * 0.11), (c + S * 0.34, c - S * 0.06)], fill=OR, width=int(S * 0.08))
        d.ellipse([c + S * 0.29, c - S * 0.13, c + S * 0.41, c - S * 0.01], fill=OR, outline=(215, 105, 35), width=6)
        for k in range(3):
            x0 = c + S * (0.315 + k * 0.03)
            d.line([(x0, c - S * 0.125), (x0, c - S * 0.095)], fill=(215, 105, 35), width=5)
    # pencil case
    tip_h = 0.12 if case_open else 0.07
    for k, col in enumerate([(235, 64, 120), (255, 160, 40), (120, 190, 70)]):
        x = c - S * 0.07 + k * S * 0.07
        top = c + S * (0.19 - tip_h)
        d.rectangle([x - 14, top, x + 14, c + S * 0.19], fill=col)
        d.polygon([(x - 14, top), (x + 14, top), (x, top - S * 0.03)], fill=col)
    if case_open:  # sparkles above the open case
        for k, (dx, dy, r) in enumerate([(-0.13, 0.07, 0.028), (0.0, 0.035, 0.03), (0.13, 0.07, 0.028)]):
            x, y, rr = c + S * dx, c + S * dy, S * r
            pts = []
            for j in range(8):
                a = -math.pi / 2 + j * math.pi / 4
                q = rr if j % 2 == 0 else rr * 0.4
                pts.append((x + q * math.cos(a), y + q * math.sin(a)))
            d.polygon(pts, fill=(255, 215, 0))
    d.rounded_rectangle([c - S * 0.15, c + S * 0.17, c + S * 0.15, c + S * 0.29], radius=28, fill=CASE, outline=CASE_D, width=7)
    d.line([c - S * 0.13, c + S * 0.20, c + S * 0.13, c + S * 0.20], fill=(200, 150, 30), width=6)
    d.ellipse([c + S * 0.10, c + S * 0.185, c + S * 0.13, c + S * 0.215], fill=(200, 150, 30))
    paws = (-1,) if wave else (-1, 1)
    for sx in paws:
        d.ellipse([c + sx * S * 0.15 - S * 0.04, c + S * 0.19, c + sx * S * 0.15 + S * 0.04, c + S * 0.26], fill=OR)
    return finish(im, size)


# ---------------------------------------------------------------- crew
def rosy(mouth_open=False, blink=False, size=300):
    S = 900
    im, d = canvas(S)
    c = S / 2
    col, dark = (235, 64, 120), (190, 40, 95)
    w = S * 0.12
    for sx in (-1, 1):
        limb(d, c + sx * w, c + S * 0.02, c + sx * (w + S * 0.10), c + S * 0.12, 18)
        limb(d, c + sx * w * 0.5, c + S * 0.30, c + sx * w * 0.6, c + S * 0.41, 18)
    d.polygon([(c - w, c - S * 0.26), (c + w, c - S * 0.26), (c, c - S * 0.43)], fill=col)
    d.rectangle([c - w, c - S * 0.26, c + w, c + S * 0.30], fill=col)
    d.rectangle([c - w, c - S * 0.18, c + w, c + S * 0.20], fill=(255, 250, 240))
    d.rectangle([c - w, c - S * 0.18, c + w, c - S * 0.15], fill=dark)
    d.rectangle([c - w, c + S * 0.17, c + w, c + S * 0.20], fill=dark)
    # little bow = Rosy's signature
    d.polygon([(c + w * 0.2, c - S * 0.30), (c + w * 1.1, c - S * 0.36), (c + w * 1.1, c - S * 0.24)], fill=(255, 205, 60))
    d.polygon([(c + w * 0.2, c - S * 0.30), (c - w * 0.7, c - S * 0.36), (c - w * 0.7, c - S * 0.24)], fill=(255, 205, 60))
    face(d, c, c - S * 0.04, S * 0.21, mouth_open, blink)
    return finish(im, size)


def rubbo(mouth_open=False, blink=False, size=300):
    S = 900
    im, d = canvas(S)
    c = S / 2
    PK, SL = (255, 150, 170), (150, 110, 230)
    for sx in (-1, 1):
        limb(d, c + sx * S * 0.22, c + S * 0.05, c + sx * S * 0.32, c + S * 0.15, 18)
        limb(d, c + sx * S * 0.10, c + S * 0.20, c + sx * S * 0.12, c + S * 0.33, 18)
    d.rounded_rectangle([c - S * 0.24, c - S * 0.18, c + S * 0.24, c + S * 0.22], radius=50, fill=PK)
    d.rectangle([c - S * 0.24, c + S * 0.04, c + S * 0.24, c + S * 0.20], fill=SL)
    d.rounded_rectangle([c - S * 0.24, c - S * 0.18, c + S * 0.24, c + S * 0.22], radius=50, outline=(220, 110, 135), width=8)
    face(d, c, c - S * 0.07, S * 0.26, mouth_open, blink)
    return finish(im, size)


def lino(mouth_open=False, blink=False, size=300):
    S = 900
    im, d = canvas(S)
    c = S / 2
    WD = (250, 215, 120)
    for sx in (-1, 1):
        limb(d, c + sx * S * 0.10, c - S * 0.02, c + sx * S * 0.20, c + S * 0.08, 16)
        limb(d, c + sx * S * 0.05, c + S * 0.38, c + sx * S * 0.07, c + S * 0.46, 16)
    d.rounded_rectangle([c - S * 0.10, c - S * 0.42, c + S * 0.10, c + S * 0.38], radius=20, fill=WD, outline=(210, 170, 80), width=6)
    for k in range(16):
        y = c - S * 0.38 + k * S * 0.048
        L = S * 0.06 if k % 4 == 0 else S * 0.035
        d.line([c - S * 0.10, y, c - S * 0.10 + L, y], fill=(150, 110, 50), width=5)
    face(d, c + S * 0.02, c - S * 0.12, S * 0.17, mouth_open, blink)
    return finish(im, size)


CREW = {'tavo': tavo, 'rosy': rosy, 'rubbo': rubbo, 'lino': lino}

if __name__ == '__main__':
    # model sheet for checking
    W, H = 1900, 560
    sheet = Image.new('RGBA', (W, H), (255, 246, 230, 255))
    items = [tavo(size=420), tavo(True, False, 420, case_open=True, wave=True), tavo(False, True, 300), rosy(size=300),
             rubbo(True, size=300), lino(blink=True, size=300)]
    x = 0
    for im in items:
        sheet.alpha_composite(im, (x, H - im.height - 40))
        x += im.width - 40
    sheet.convert('RGB').save('crew_sheet.jpg', quality=90)
    print('ok')
