"""Topic file for ONE song (rewrite this file for every new song).

Example: "Colors in My Lunchbox" (colors + fruits). The engine (engine.py) reads:
  TITLE, TOPIC, INTRO_LINE, OUTRO_LINE, VOICE, CHORUS_TITLE, OUTRO_TITLE,
  THEMES, VERSES, GUESTS, THUMB
Guest sprites must use chars.canvas / chars.face / chars.finish so they match the house style.
Signature of every guest function: f(mouth_open: bool, blink: bool, size: int) -> RGBA image (size x size).
"""
import math
from PIL import Image, ImageDraw
from chars import canvas, face, finish

TITLE = 'Colors in My Lunchbox'
TOPIC = 'colors'
VOICE = 'af_heart'                      # Tavo's fixed voice – do not change
INTRO_LINE = "Hi friends! It's Tavo! Let's sing about colors!"
OUTRO_LINE = "Bye bye, friends! See you next time with Tavo!"
CHORUS_TITLE = 'Colors, colors!'
OUTRO_TITLE = 'Healthy colors!'

# Background themes used by song.py section 'theme' names (and by VERSES).
# top/bot = gradient, col = accent (big word + lyric highlight), ground = hill colour, rainbow = draw rainbow arc
THEMES = {
    'title':   dict(top=(170, 222, 255), bot=(232, 248, 255), col=(216, 27, 96), rainbow=True),
    'red':     dict(top=(255, 232, 232), bot=(255, 186, 186), col=(229, 57, 53)),
    'yellow':  dict(top=(255, 250, 220), bot=(255, 226, 140), col=(232, 150, 0)),
    'green':   dict(top=(232, 250, 228), bot=(178, 232, 170), col=(56, 150, 60)),
    'blue':    dict(top=(228, 242, 255), bot=(170, 212, 255), col=(30, 120, 220)),
    'rainbow': dict(top=(170, 222, 255), bot=(232, 248, 255), col=(216, 27, 96), rainbow=True),
    'end':     dict(top=(170, 222, 255), bot=(232, 248, 255), col=(216, 27, 96), rainbow=True),
}

# One entry per verse section, in order.
VERSES = [
    dict(guest='apple', word='RED', theme='red'),
    dict(guest='banana', word='YELLOW', theme='yellow'),
    dict(guest='grapes', word='GREEN', theme='green'),
    dict(guest='blueberry', word='BLUE', theme='blue'),
]

THUMB = dict(lines=['Colors in', 'My Lunchbox'], theme='title')


# ------------------------------------------------------------------ guests
def apple(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2; r = S * 0.38
    d.ellipse([c - r * 1.02, c - r * 0.82, c + r * 0.12, c + r], fill=(226, 45, 45))
    d.ellipse([c - r * 0.12, c - r * 0.82, c + r * 1.02, c + r], fill=(226, 45, 45))
    d.ellipse([c - r * 0.85, c - r * 0.6, c + r * 0.85, c + r * 1.0], fill=(226, 45, 45))
    d.ellipse([c - r * 0.7, c - r * 0.6, c - r * 0.35, c - r * 0.25], fill=(255, 150, 150))
    d.rounded_rectangle([c - S * 0.018, c - r * 1.2, c + S * 0.018, c - r * 0.6], radius=10, fill=(110, 70, 40))
    d.ellipse([c + S * 0.01, c - r * 1.25, c + r * 0.6, c - r * 0.92], fill=(76, 175, 80))
    face(d, c, c + r * 0.1, r * 1.05, mouth_open, blink)
    return finish(im, size)


def banana(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
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
    return finish(im, size)


def grapes(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2; gr = S * 0.105
    rows = [(-0.3, [-1.5, -0.5, 0.5, 1.5]), (-0.05, [-1, 0, 1]), (0.2, [-1.5, -0.5, 0.5, 1.5]), (0.4, [-0.5, 0.5])]
    for ry, xs in rows:
        for xx in xs:
            x, y = c + xx * gr * 1.9, c + ry * S
            d.ellipse([x - gr, y - gr, x + gr, y + gr], fill=(110, 190, 70), outline=(70, 140, 45), width=4)
            d.ellipse([x - gr * 0.55, y - gr * 0.6, x - gr * 0.15, y - gr * 0.2], fill=(200, 240, 170))
    d.rounded_rectangle([c - 10, c - S * 0.47, c + 10, c - S * 0.36], radius=6, fill=(110, 70, 40))
    d.ellipse([c + 5, c - S * 0.48, c + S * 0.2, c - S * 0.38], fill=(56, 142, 60))
    fr = S * 0.21
    d.ellipse([c - fr, c - fr + S * 0.02, c + fr, c + fr + S * 0.02], fill=(124, 204, 80), outline=(70, 140, 45), width=5)
    face(d, c, c, fr * 1.15, mouth_open, blink)
    return finish(im, size)


def blueberry(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
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
    return finish(im, size)


GUESTS = {'apple': apple, 'banana': banana, 'grapes': grapes, 'blueberry': blueberry}
