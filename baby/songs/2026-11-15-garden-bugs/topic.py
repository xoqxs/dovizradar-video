"""Topic file for ONE song: "Tiny Bugs in My Garden" (garden bugs)."""
import math
from PIL import Image, ImageDraw
from chars import canvas, face, finish

TITLE = 'Tiny Bugs in My Garden'
TOPIC = 'garden bugs'
VOICE = 'af_heart'
INTRO_LINE = "Hi friends! It's Tavo! I'm drawing flowers in the garden, and I hear tiny bugs. Who is hiding there?"
OUTRO_LINE = "Bye bye, friends! See you next time with Tavo!"
CHORUS_TITLE = 'In the garden!'
OUTRO_TITLE = 'Bye, garden bugs!'

GARDEN = dict(top=(160, 215, 255), bot=(232, 248, 255), col=(56, 142, 60), scene='garden')
THEMES = {
    'title':     GARDEN,
    'bee':       dict(GARDEN, col=(225, 140, 0)),
    'ladybug':   dict(GARDEN, col=(214, 40, 40)),
    'cricket':   dict(GARDEN, col=(46, 140, 50)),
    'butterfly': dict(GARDEN, col=(150, 70, 200)),
    'garden':    GARDEN,
    'end':       GARDEN,
}

VERSES = [
    dict(guest='bee', word='BEE', theme='bee', motion='fly'),
    dict(guest='ladybug', word='LADYBUG', theme='ladybug', motion='walk'),
    dict(guest='cricket', word='CRICKET', theme='cricket', motion='hop'),
    dict(guest='butterfly', word='BUTTERFLY', theme='butterfly', motion='fly'),
]

THUMB = dict(lines=['Tiny Bugs', 'in My Garden'], theme='title')

INKB = (50, 40, 45)


def bee(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    for sx in (-1, 1):  # wings
        d.ellipse([c + sx * S * 0.05 - S * 0.13, c - S * 0.36, c + sx * S * 0.05 + S * 0.13, c - S * 0.12] if sx < 0 else
                  [c + S * 0.05 - S * 0.13 + S * 0.08, c - S * 0.36, c + S * 0.05 + S * 0.13 + S * 0.08, c - S * 0.12],
                  fill=(225, 245, 255, 235), outline=(140, 190, 230), width=8)
    d.polygon([(c + S * 0.36, c + S * 0.06), (c + S * 0.46, c + S * 0.10), (c + S * 0.36, c + S * 0.14)], fill=INKB)  # stinger
    d.ellipse([c - S * 0.36, c - S * 0.20, c + S * 0.38, c + S * 0.32], fill=(255, 205, 40), outline=(215, 160, 20), width=8)
    box = [c - S * 0.36, c - S * 0.20, c + S * 0.38, c + S * 0.32]
    st = Image.new('RGBA', (S, S), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    for x in (0.08, 0.22):
        sd.rectangle([c + S * x, 0, c + S * (x + 0.07), S], fill=INKB + (255,))
    m = Image.new('L', (S, S), 0); ImageDraw.Draw(m).ellipse(box, fill=255)
    im.paste(st, (0, 0), Image.composite(st.split()[3], Image.new('L', (S, S), 0), m))
    d = ImageDraw.Draw(im, 'RGBA')
    d.ellipse(box, outline=(215, 160, 20), width=8)
    for sx in (-1, 1):  # antennae
        d.line([c - S * 0.14 + sx * S * 0.07, c - S * 0.16, c - S * 0.14 + sx * S * 0.13, c - S * 0.34], fill=INKB, width=10)
        x = c - S * 0.14 + sx * S * 0.13
        d.ellipse([x - 16, c - S * 0.34 - 16, x + 16, c - S * 0.34 + 16], fill=INKB)
    face(d, c - S * 0.12, c + S * 0.02, S * 0.27, mouth_open, blink)
    return finish(im, size)


def ladybug(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    d.ellipse([c - S * 0.17, c - S * 0.40, c + S * 0.17, c - S * 0.14], fill=INKB)  # head
    for sx in (-1, 1):
        d.line([c + sx * S * 0.06, c - S * 0.36, c + sx * S * 0.15, c - S * 0.46], fill=INKB, width=10)
        x = c + sx * S * 0.15
        d.ellipse([x - 16, c - S * 0.46 - 16, x + 16, c - S * 0.46 + 16], fill=INKB)
        for k in range(3):
            y = c - S * 0.05 + k * S * 0.13
            d.line([c + sx * S * 0.30, y, c + sx * S * 0.42, y + S * 0.04], fill=INKB, width=14)
    d.ellipse([c - S * 0.36, c - S * 0.26, c + S * 0.36, c + S * 0.42], fill=(226, 40, 40), outline=(170, 25, 25), width=8)
    d.line([c, c - S * 0.25, c, c - S * 0.12], fill=INKB, width=10)
    d.line([c, c + S * 0.28, c, c + S * 0.41], fill=INKB, width=10)
    for x, y, r in [(-0.24, -0.06, 0.06), (0.24, -0.06, 0.06), (-0.27, 0.16, 0.055), (0.27, 0.16, 0.055),
                    (-0.14, 0.31, 0.05), (0.14, 0.31, 0.05)]:
        d.ellipse([c + (x - r) * S, c + (y - r) * S, c + (x + r) * S, c + (y + r) * S], fill=INKB)
    face(d, c, c + S * 0.06, S * 0.24, mouth_open, blink)
    return finish(im, size)


def cricket(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    G, GD, GL = (110, 195, 70), (70, 145, 45), (170, 225, 120)
    for sx, w in ((1, 16), (-1, 16)):  # antennae
        d.line([c - S * 0.22, c - S * 0.18, c - S * 0.22 + sx * S * 0.10, c - S * 0.44], fill=GD, width=w - 6)
    # big back leg (bent)
    d.line([c + S * 0.10, c + S * 0.08, c + S * 0.34, c - S * 0.16], fill=GD, width=34)
    d.line([c + S * 0.34, c - S * 0.16, c + S * 0.40, c + S * 0.26], fill=GD, width=24)
    d.ellipse([c + S * 0.36, c + S * 0.23, c + S * 0.46, c + S * 0.29], fill=GD)
    for x in (-0.18, 0.0):  # small legs
        d.line([c + S * x, c + S * 0.15, c + S * (x - 0.05), c + S * 0.30], fill=GD, width=16)
    d.ellipse([c - S * 0.20, c - S * 0.06, c + S * 0.40, c + S * 0.22], fill=G, outline=GD, width=8)  # body
    d.polygon([(c - S * 0.05, c - S * 0.04), (c + S * 0.42, c + S * 0.02), (c + S * 0.30, c + S * 0.12)], fill=GD)  # wing
    d.ellipse([c - S * 0.42, c - S * 0.26, c - S * 0.02, c + S * 0.14], fill=GL, outline=GD, width=8)  # head
    face(d, c - S * 0.22, c - S * 0.08, S * 0.25, mouth_open, blink)
    return finish(im, size)


def butterfly(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    for sx in (-1, 1):
        d.ellipse([c + sx * S * 0.05 - (S * 0.38 if sx < 0 else 0), c - S * 0.40,
                   c + sx * S * 0.05 + (0 if sx < 0 else S * 0.38), c + S * 0.02], fill=(255, 120, 170), outline=(215, 60, 120), width=8)
        d.ellipse([c + sx * S * 0.05 - (S * 0.28 if sx < 0 else 0), c - S * 0.02,
                   c + sx * S * 0.05 + (0 if sx < 0 else S * 0.28), c + S * 0.36], fill=(255, 175, 60), outline=(220, 130, 30), width=8)
        x = c + sx * S * 0.25
        d.ellipse([x - S * 0.07, c - S * 0.26, x + S * 0.07, c - S * 0.12], fill=(255, 230, 90))
        x = c + sx * S * 0.19
        d.ellipse([x - S * 0.05, c + S * 0.12, x + S * 0.05, c + S * 0.22], fill=(255, 245, 200))
    d.rounded_rectangle([c - S * 0.05, c - S * 0.10, c + S * 0.05, c + S * 0.38], radius=30, fill=(130, 70, 190))
    for sx in (-1, 1):
        d.line([c + sx * S * 0.04, c - S * 0.30, c + sx * S * 0.13, c - S * 0.45], fill=INKB, width=10)
        x = c + sx * S * 0.13
        d.ellipse([x - 15, c - S * 0.45 - 15, x + 15, c - S * 0.45 + 15], fill=INKB)
    r = S * 0.15
    d.ellipse([c - r, c - S * 0.20 - r, c + r, c - S * 0.20 + r], fill=(160, 100, 215), outline=(110, 55, 160), width=7)
    face(d, c, c - S * 0.21, r * 1.15, mouth_open, blink)
    return finish(im, size)


GUESTS = {'bee': bee, 'ladybug': ladybug, 'cricket': cricket, 'butterfly': butterfly}

if __name__ == '__main__':
    sheet = Image.new('RGBA', (1800, 480), (200, 235, 200, 255))
    for k, f in enumerate([bee, ladybug, cricket, butterfly]):
        sheet.alpha_composite(f(k % 2 == 0, False, 440), (k * 450, 20))
    sheet.convert('RGB').save('guests.jpg', quality=88)
