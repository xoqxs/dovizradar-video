"""Topic file for ONE song (rewrite this file for every new song).

Song: "Who Says Moo?" (farm animals + sounds). The engine (engine.py) reads:
  TITLE, TOPIC, INTRO_LINE, OUTRO_LINE, VOICE, CHORUS_TITLE, OUTRO_TITLE,
  THEMES, VERSES, GUESTS, THUMB
Guest sprites must use chars.canvas / chars.face / chars.finish so they match the house style.
Signature of every guest function: f(mouth_open: bool, blink: bool, size: int) -> RGBA image (size x size).
"""
import math
from PIL import Image, ImageDraw
from chars import canvas, face, finish

TITLE = 'Who Says Moo?'
TOPIC = 'farm animals'
VOICE = 'af_heart'                      # Tavo's fixed voice – do not change
INTRO_LINE = "Hi friends! It's Tavo! Let's sing about farm animals!"
OUTRO_LINE = "Bye bye, friends! See you next time with Tavo!"
CHORUS_TITLE = 'Down on the farm!'
OUTRO_TITLE = 'Bye, farm friends!'

THEMES = {
    'title': dict(top=(170, 222, 255), bot=(226, 246, 214), col=(200, 70, 40), rainbow=True),
    'cow':   dict(top=(236, 244, 255), bot=(196, 232, 176), col=(120, 74, 40)),
    'duck':  dict(top=(226, 244, 255), bot=(160, 214, 250), col=(230, 140, 0)),
    'pig':   dict(top=(255, 236, 242), bot=(250, 196, 214), col=(214, 60, 120)),
    'sheep': dict(top=(240, 246, 255), bot=(206, 226, 250), col=(70, 100, 190)),
    'farm':  dict(top=(170, 222, 255), bot=(226, 246, 214), col=(200, 70, 40), rainbow=True),
    'end':   dict(top=(170, 222, 255), bot=(226, 246, 214), col=(200, 70, 40), rainbow=True),
}

VERSES = [
    dict(guest='cow', word='COW', theme='cow'),
    dict(guest='duck', word='DUCK', theme='duck'),
    dict(guest='pig', word='PIG', theme='pig'),
    dict(guest='sheep', word='SHEEP', theme='sheep'),
]

THUMB = dict(lines=['Who Says', 'Moo?'], theme='title')


# ------------------------------------------------------------------ guests (original designs)
def cow(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2; r = S * 0.34
    for sx in (-1, 1):  # horns + ears
        d.ellipse([c + sx * r * 0.55 - 30, c - r * 1.15, c + sx * r * 0.55 + 30, c - r * 0.7], fill=(250, 226, 160))
        d.ellipse([c + sx * r * 1.05 - 80, c - r * 0.75, c + sx * r * 1.05 + 80, c - r * 0.35], fill=(240, 240, 240), outline=(90, 90, 90), width=5)
    d.ellipse([c - r, c - r * 0.95, c + r, c + r * 0.85], fill=(250, 250, 250), outline=(90, 90, 90), width=6)
    d.ellipse([c - r * 0.95, c - r * 0.8, c - r * 0.3, c - r * 0.15], fill=(110, 70, 45))
    d.ellipse([c + r * 0.45, c - r * 0.95, c + r * 0.9, c - r * 0.45], fill=(110, 70, 45))
    d.ellipse([c - r * 0.7, c + r * 0.35, c + r * 0.7, c + r * 1.05], fill=(255, 180, 190), outline=(200, 110, 120), width=5)
    for sx in (-1, 1):
        d.ellipse([c + sx * r * 0.3 - 18, c + r * 0.6 - 14, c + sx * r * 0.3 + 18, c + r * 0.6 + 14], fill=(170, 80, 95))
    face(d, c, c - r * 0.25, r * 0.95, mouth_open, blink, blush=False, mouth_dy=r * 0.55)
    return finish(im, size)


def duck(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    d.ellipse([c - S * 0.36, c - S * 0.02, c + S * 0.32, c + S * 0.4], fill=(255, 214, 40))
    d.polygon([(c + S * 0.26, c + S * 0.12), (c + S * 0.44, c + S * 0.02), (c + S * 0.36, c + S * 0.24)], fill=(255, 214, 40))
    d.ellipse([c - S * 0.2, c + S * 0.08, c + S * 0.12, c + S * 0.3], fill=(240, 186, 20))
    r = S * 0.24
    d.ellipse([c - r, c - S * 0.42, c + r, c - S * 0.42 + 2 * r], fill=(255, 220, 50))
    d.ellipse([c - 20, c - S * 0.47, c + 30, c - S * 0.38], fill=(255, 220, 50))
    by = c - S * 0.42 + r * 1.35
    d.rounded_rectangle([c - r * 0.55, by - 22, c + r * 0.55, by + 40], radius=30, fill=(255, 140, 30), outline=(220, 100, 10), width=4)
    face(d, c, c - S * 0.42 + r * 0.85, r * 1.1, False, blink, blush=True, mouth_dy=-1000)
    if mouth_open:
        d.ellipse([c - r * 0.3, by + 10, c + r * 0.3, by + 46], fill=(150, 50, 20))
    return finish(im, size)


def pig(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2; r = S * 0.36
    for sx in (-1, 1):
        d.polygon([(c + sx * r * 0.35, c - r * 0.75), (c + sx * r * 0.95, c - r * 1.1), (c + sx * r * 0.85, c - r * 0.35)], fill=(246, 150, 180))
    d.ellipse([c - r, c - r * 0.85, c + r, c + r * 0.9], fill=(255, 182, 200), outline=(220, 120, 150), width=6)
    sy = c + r * 0.3
    d.ellipse([c - r * 0.42, sy - r * 0.26, c + r * 0.42, sy + r * 0.26], fill=(246, 140, 172), outline=(210, 100, 135), width=5)
    for sx in (-1, 1):
        d.ellipse([c + sx * r * 0.16 - 16, sy - 20, c + sx * r * 0.16 + 16, sy + 20], fill=(170, 60, 95))
    face(d, c, c - r * 0.25, r * 0.9, mouth_open, blink, blush=True, mouth_dy=r * 0.5)
    return finish(im, size)


def sheep(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    for k in range(12):
        a = 2 * math.pi * k / 12
        x, y = c + S * 0.3 * math.cos(a), c + S * 0.03 + S * 0.28 * math.sin(a)
        d.ellipse([x - S * 0.12, y - S * 0.12, x + S * 0.12, y + S * 0.12], fill=(255, 255, 255), outline=(200, 200, 215), width=4)
    d.ellipse([c - S * 0.3, c - S * 0.25, c + S * 0.3, c + S * 0.31], fill=(255, 255, 255))
    r = S * 0.2
    for sx in (-1, 1):
        d.ellipse([c + sx * r * 1.15 - 60, c - r * 0.45, c + sx * r * 1.15 + 60, c - r * 0.05], fill=(90, 80, 90))
    d.ellipse([c - r, c - r * 0.9, c + r, c + r * 1.0], fill=(110, 98, 110))
    for xx in (-0.5, 0, 0.5):
        x = c + xx * r; y = c - r * 0.95
        d.ellipse([x - r * 0.35, y - r * 0.3, x + r * 0.35, y + r * 0.3], fill=(255, 255, 255))
    face(d, c, c, r * 1.05, mouth_open, blink, blush=True)
    return finish(im, size)


GUESTS = {'cow': cow, 'duck': duck, 'pig': pig, 'sheep': sheep}
