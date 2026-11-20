"""Topic file for ONE song: "Boom, Ding, Who Can Play?" (music instruments)."""
import math
from PIL import Image, ImageDraw
from chars import canvas, face, finish

TITLE = 'Boom, Ding, Who Can Play?'
TOPIC = 'music instruments'
VOICE = 'af_heart'
INTRO_LINE = "Hi friends! It's Tavo! We're making a little band in the park today. Who will come and play? Let's sing!"
OUTRO_LINE = "Bye bye, friends! What a happy band! See you next time with Tavo!"
CHORUS_TITLE = 'Our band!'
OUTRO_TITLE = 'What a band!'

PARK = dict(top=(150, 210, 250), bot=(205, 235, 255), col=(70, 170, 90), scene='park')
THEMES = {
    'title':   PARK,
    'drum':    dict(PARK, col=(225, 65, 60)),
    'trumpet': dict(PARK, col=(235, 170, 30)),
    'xylo':    dict(PARK, col=(130, 90, 220)),
    'maracas': dict(PARK, col=(240, 120, 40)),
    'band':    PARK,
    'end':     PARK,
}

VERSES = [
    dict(guest='drum', word='DRUM', theme='drum', motion='hop'),
    dict(guest='trumpet', word='TRUMPET', theme='trumpet', motion='fly'),
    dict(guest='xylo', word='XYLOPHONE', theme='xylo', motion='walk'),
    dict(guest='maracas', word='MARACAS', theme='maracas', motion='bounce'),
]

THUMB = dict(lines=['Boom, Ding,', 'Who Can Play?'], theme='title')


def drum(mouth_open=False, blink=False, size=440):
    """Round red drum with white top, gold zigzag cord and two sticks."""
    S = 880; im, d = canvas(S); c = S / 2
    R, RD = (225, 65, 60), (165, 35, 35)
    w = S * 0.36; top = c - S * 0.14; bot = c + S * 0.30
    d.rectangle([c - w, top, c + w, bot], fill=R)
    d.ellipse([c - w, bot - S * 0.10, c + w, bot + S * 0.10], fill=R, outline=RD, width=10)
    d.line([(c - w, top), (c - w, bot)], fill=RD, width=10)
    d.line([(c + w, top), (c + w, bot)], fill=RD, width=10)
    pts = []
    for k in range(9):
        x = c - w + k * (2 * w / 8)
        pts.append((x, top + S * 0.06 if k % 2 == 0 else bot - S * 0.02))
    d.line(pts, fill=(255, 210, 60), width=12, joint='curve')
    d.ellipse([c - w, top - S * 0.10, c + w, top + S * 0.10], fill=(250, 248, 240), outline=RD, width=10)
    for sx in (-1, 1):
        d.line([(c + sx * S * 0.10, top - S * 0.02), (c + sx * S * 0.32, top - S * 0.30)], fill=(200, 150, 90), width=22)
        d.ellipse([c + sx * S * 0.32 - 26, top - S * 0.30 - 26, c + sx * S * 0.32 + 26, top - S * 0.30 + 26], fill=(245, 235, 215))
    d.rounded_rectangle([c - S * 0.17, c + S * 0.00, c + S * 0.17, c + S * 0.24], radius=40, fill=(250, 248, 240))
    face(d, c, c + S * 0.12, S * 0.20, mouth_open, blink)
    return finish(im, size)


def trumpet(mouth_open=False, blink=False, size=440):
    """Shiny golden trumpet with a big bell and three buttons."""
    S = 880; im, d = canvas(S); c = S / 2
    G, GD = (245, 190, 50), (190, 135, 20)
    d.rounded_rectangle([c - S * 0.40, c - S * 0.05, c + S * 0.12, c + S * 0.05], radius=30, fill=G, outline=GD, width=8)
    d.rounded_rectangle([c - S * 0.30, c + S * 0.02, c + S * 0.05, c + S * 0.16], radius=50, outline=GD, width=22)
    d.polygon([(c + S * 0.08, c - S * 0.06), (c + S * 0.44, c - S * 0.28), (c + S * 0.44, c + S * 0.28), (c + S * 0.08, c + S * 0.06)], fill=G, outline=GD)
    d.ellipse([c + S * 0.36, c - S * 0.30, c + S * 0.48, c + S * 0.30], fill=(255, 220, 110), outline=GD, width=8)
    d.rounded_rectangle([c - S * 0.46, c - S * 0.04, c - S * 0.38, c + S * 0.04], radius=10, fill=GD)
    for k in range(3):
        x = c - S * 0.20 + k * S * 0.10
        d.rectangle([x - 14, c - S * 0.16, x + 14, c - S * 0.05], fill=GD)
        d.ellipse([x - 26, c - S * 0.21, x + 26, c - S * 0.14], fill=(255, 235, 160), outline=GD, width=5)
    face(d, c + S * 0.24, c + S * 0.01, S * 0.15, mouth_open, blink)
    return finish(im, size)


def xylo(mouth_open=False, blink=False, size=440):
    """Little xylophone with rainbow bars on a wooden frame and a mallet."""
    S = 880; im, d = canvas(S); c = S / 2
    cols = [(230, 70, 60), (245, 145, 45), (250, 210, 50), (90, 190, 90), (70, 140, 230), (150, 95, 215)]
    d.rounded_rectangle([c - S * 0.42, c + S * 0.02, c + S * 0.42, c + S * 0.42], radius=40, fill=(185, 125, 70), outline=(130, 85, 45), width=8)
    for k, col in enumerate(cols):
        x = c - S * 0.36 + k * S * 0.135
        h = S * (0.30 - k * 0.025)
        d.rounded_rectangle([x, c + S * 0.10 - h, x + S * 0.11, c + S * 0.10], radius=18, fill=col, outline=(80, 60, 50), width=6)
    d.line([(c + S * 0.18, c - S * 0.40), (c + S * 0.42, c - S * 0.20)], fill=(200, 150, 90), width=18)
    d.ellipse([c + S * 0.12, c - S * 0.46, c + S * 0.24, c - S * 0.34], fill=(240, 80, 120))
    face(d, c, c + S * 0.26, S * 0.18, mouth_open, blink)
    return finish(im, size)


def maracas(mouth_open=False, blink=False, size=440):
    """Orange maraca with green and yellow stripes and a wooden handle."""
    S = 880; im, d = canvas(S); c = S / 2
    O, OD = (245, 125, 45), (190, 85, 25)
    d.rounded_rectangle([c - S * 0.05, c + S * 0.12, c + S * 0.05, c + S * 0.46], radius=24, fill=(200, 150, 90), outline=(150, 100, 55), width=6)
    d.ellipse([c - S * 0.30, c - S * 0.42, c + S * 0.30, c + S * 0.20], fill=O, outline=OD, width=10)
    d.arc([c - S * 0.30, c - S * 0.30, c + S * 0.30, c + S * 0.06], 200, 340, fill=(90, 190, 90), width=22)
    d.arc([c - S * 0.30, c - S * 0.22, c + S * 0.30, c + S * 0.14], 20, 160, fill=(255, 215, 60), width=22)
    for (dx, dy) in ((-0.38, -0.30), (0.38, -0.34), (-0.40, 0.02), (0.40, -0.02)):
        x, y = c + dx * S, c + dy * S
        d.arc([x - 30, y - 30, x + 30, y + 30], 300 if dx > 0 else 120, 60 if dx > 0 else 240, fill=(120, 90, 200), width=10)
    face(d, c, c - S * 0.12, S * 0.20, mouth_open, blink)
    return finish(im, size)


GUESTS = {'drum': drum, 'trumpet': trumpet, 'xylo': xylo, 'maracas': maracas}

if __name__ == '__main__':
    sheet = Image.new('RGBA', (1800, 480), (210, 230, 250, 255))
    for k, f in enumerate([drum, trumpet, xylo, maracas]):
        sheet.alpha_composite(f(k % 2 == 0, False, 440), (k * 450, 20))
    sheet.convert('RGB').save('guests.jpg', quality=88)
