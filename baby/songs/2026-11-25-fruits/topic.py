"""Topic file for ONE song: "Yummy Fruits, Who Is Hiding?" (fruits)."""
import math
from PIL import Image, ImageDraw
from chars import canvas, face, finish

TITLE = 'Fruits, Who Is Hiding?'
TOPIC = 'fruits'
VOICE = 'af_heart'
INTRO_LINE = "Hi friends! It's Tavo! I'm at the farm with an empty picnic basket. Which fruits are hiding here? Let's sing!"
OUTRO_LINE = "Bye bye, friends! What a yummy picnic! See you next time with Tavo!"
CHORUS_TITLE = 'Yummy fruits!'
OUTRO_TITLE = 'Picnic time!'

FARM = dict(top=(168, 220, 255), bot=(228, 246, 214), col=(210, 70, 50), scene='farm')
THEMES = {
    'title':      FARM,
    'apple':      dict(FARM, col=(215, 45, 45)),
    'banana':     dict(FARM, col=(225, 160, 0)),
    'strawberry': dict(FARM, col=(225, 60, 110)),
    'pear':       dict(FARM, col=(90, 160, 50)),
    'fruit':      FARM,
    'end':        FARM,
}

VERSES = [
    dict(guest='apple', word='APPLE', theme='apple', motion='roll'),
    dict(guest='banana', word='BANANA', theme='banana', motion='walk'),
    dict(guest='strawberry', word='BERRY', theme='strawberry', motion='hop'),
    dict(guest='pear', word='PEAR', theme='pear', motion='bounce'),
]

THUMB = dict(lines=['Yummy Fruits,', 'Who Is Hiding?'], theme='title')

LEAF, LEAFD = (95, 180, 70), (55, 125, 40)
STEM = (125, 80, 45)


def _leaf(d, x, y, w, h, ang=0):
    d.ellipse([x - w, y - h, x + w, y + h], fill=LEAF, outline=LEAFD, width=7)
    d.line([(x - w * 0.7, y), (x + w * 0.7, y)], fill=LEAFD, width=6)


def apple(mouth_open=False, blink=False, size=440):
    """Round red apple with a stem, a leaf and a white shine."""
    S = 880; im, d = canvas(S); c = S / 2
    R, RD = (225, 50, 50), (165, 25, 30)
    d.ellipse([c - S * 0.38, c - S * 0.28, c + S * 0.02, c + S * 0.40], fill=R, outline=RD, width=8)
    d.ellipse([c - S * 0.02, c - S * 0.28, c + S * 0.38, c + S * 0.40], fill=R, outline=RD, width=8)
    d.ellipse([c - S * 0.34, c - S * 0.24, c + S * 0.34, c + S * 0.37], fill=R)
    d.rounded_rectangle([c - S * 0.025, c - S * 0.42, c + S * 0.025, c - S * 0.22], radius=12, fill=STEM)
    _leaf(d, c + S * 0.12, c - S * 0.36, S * 0.10, S * 0.05)
    d.ellipse([c - S * 0.26, c - S * 0.16, c - S * 0.16, c - S * 0.02], fill=(255, 190, 190))
    face(d, c, c + S * 0.08, S * 0.19, mouth_open, blink)
    return finish(im, size)


def banana(mouth_open=False, blink=False, size=440):
    """Curved yellow banana (thick crescent) with brown tips."""
    S = 880; im, d = canvas(S); c = S / 2
    Y, YD = (255, 215, 60), (205, 150, 20)
    pts_o, pts_i = [], []
    for k in range(41):
        a = math.radians(200 + k * 140 / 40)
        w = math.sin(math.pi * k / 40)
        ro = S * 0.42
        ri = S * 0.42 - S * 0.30 * (0.2 + 0.8 * w)
        pts_o.append((c + ro * math.cos(a), c - S * 0.12 - ro * math.sin(a)))
        pts_i.append((c + ri * math.cos(a), c - S * 0.12 - ri * math.sin(a)))
    poly = pts_o + pts_i[::-1]
    d.polygon(poly, fill=Y, outline=YD)
    d.line(poly + [poly[0]], fill=YD, width=8, joint='curve')
    for p in (pts_o[0], pts_o[-1]):
        d.ellipse([p[0] - 18, p[1] - 18, p[0] + 18, p[1] + 18], fill=STEM)
    face(d, c, c + S * 0.16, S * 0.15, mouth_open, blink)
    return finish(im, size)


def strawberry(mouth_open=False, blink=False, size=440):
    """Plump red strawberry (rounded heart) with yellow seeds and a green leafy cap."""
    S = 880; im, d = canvas(S); c = S / 2
    R, RD = (235, 55, 85), (175, 30, 55)
    body = []
    for k in range(120):
        a = 2 * math.pi * k / 120
        sn = math.sin(a)
        body.append((c + S * 0.37 * math.cos(a) * (1 - 0.62 * max(0.0, sn) ** 1.6), c + S * 0.02 + S * 0.38 * sn))
    d.polygon(body, fill=R)
    d.line(body + [body[0]], fill=RD, width=8, joint='curve')
    for (dx, dy) in ((-0.24, -0.12), (0.24, -0.12), (-0.28, 0.06), (0.28, 0.06), (-0.12, 0.22), (0.12, 0.22), (0, 0.31), (-0.08, -0.22), (0.08, -0.22)):
        x, y = c + dx * S, c + dy * S
        d.ellipse([x - 9, y - 13, x + 9, y + 13], fill=(255, 230, 110))
    for k in range(5):
        a = math.radians(-90 + (k - 2) * 38)
        x, y = c + S * 0.16 * math.cos(a) * 1.4, c - S * 0.30 + S * 0.10 * math.sin(a) * 0.6
        d.polygon([(c, c - S * 0.30), (x - 30, y), (x + 30, y)], fill=LEAF, outline=LEAFD)
    d.ellipse([c - S * 0.10, c - S * 0.36, c + S * 0.10, c - S * 0.24], fill=LEAF, outline=LEAFD, width=6)
    d.rounded_rectangle([c - S * 0.02, c - S * 0.44, c + S * 0.02, c - S * 0.33], radius=10, fill=LEAFD)
    face(d, c, c + S * 0.02, S * 0.17, mouth_open, blink)
    return finish(im, size)


def pear(mouth_open=False, blink=False, size=440):
    """Green pear: small top circle on a big round bottom, stem and leaf."""
    S = 880; im, d = canvas(S); c = S / 2
    G, GD = (170, 215, 80), (110, 155, 40)
    d.ellipse([c - S * 0.18, c - S * 0.34, c + S * 0.18, c + S * 0.02], fill=G, outline=GD, width=8)
    d.ellipse([c - S * 0.34, c - S * 0.12, c + S * 0.34, c + S * 0.42], fill=G, outline=GD, width=8)
    d.ellipse([c - S * 0.16, c - S * 0.32, c + S * 0.16, c + S * 0.00], fill=G)
    d.polygon([(c - S * 0.16, c - S * 0.12), (c + S * 0.16, c - S * 0.12), (c + S * 0.30, c + S * 0.06), (c - S * 0.30, c + S * 0.06)], fill=G)
    d.rounded_rectangle([c - S * 0.02, c - S * 0.44, c + S * 0.025, c - S * 0.30], radius=12, fill=STEM)
    _leaf(d, c + S * 0.11, c - S * 0.40, S * 0.09, S * 0.045)
    d.ellipse([c - S * 0.24, c + S * 0.00, c - S * 0.15, c + S * 0.12], fill=(225, 245, 170))
    face(d, c, c + S * 0.16, S * 0.18, mouth_open, blink)
    return finish(im, size)


GUESTS = {'apple': apple, 'banana': banana, 'strawberry': strawberry, 'pear': pear}

if __name__ == '__main__':
    sheet = Image.new('RGBA', (1800, 480), (230, 245, 215, 255))
    for k, f in enumerate([apple, banana, strawberry, pear]):
        sheet.alpha_composite(f(k % 2 == 0, False, 440), (k * 450, 20))
    sheet.convert('RGB').save('guests.jpg', quality=88)
