"""Topic file for ONE song: "Who Can Move With Me?" (body parts / moving)."""
import math
from PIL import Image, ImageDraw
from chars import canvas, face, finish

TITLE = 'Who Can Move With Me?'
TOPIC = 'body parts / moving'
VOICE = 'af_heart'
INTRO_LINE = "Good morning, friends! It's Tavo! I just woke up and my body wants to wiggle. Who can move with me? Let's sing!"
OUTRO_LINE = "Bye bye, friends! Great wiggling! See you next time with Tavo!"
CHORUS_TITLE = "Let's move!"
OUTRO_TITLE = 'Great moving!'

ROOM = dict(top=(255, 236, 214), bot=(250, 218, 196), col=(240, 120, 90), scene='room')
THEMES = {
    'title': ROOM,
    'hand':  dict(ROOM, col=(235, 120, 60)),
    'foot':  dict(ROOM, col=(70, 150, 220)),
    'nose':  dict(ROOM, col=(225, 80, 120)),
    'ear':   dict(ROOM, col=(120, 90, 210)),
    'move':  ROOM,
    'end':   ROOM,
}

VERSES = [
    dict(guest='hand', word='HANDS', theme='hand', motion='bounce'),
    dict(guest='foot', word='FEET', theme='foot', motion='hop'),
    dict(guest='nose', word='NOSE', theme='nose', motion='walk'),
    dict(guest='ear', word='EARS', theme='ear', motion='bounce'),
]

THUMB = dict(lines=['Who Can Move', 'With Me?'], theme='title')

SKIN, SKIND = (255, 205, 160), (215, 150, 105)


def hand(mouth_open=False, blink=False, size=440):
    """Chubby open hand with four fingers and a thumb, orange wristband."""
    S = 880; im, d = canvas(S); c = S / 2
    d.rounded_rectangle([c - S * 0.12, c + S * 0.28, c + S * 0.12, c + S * 0.46], radius=30, fill=(240, 120, 60))
    d.rounded_rectangle([c - S * 0.26, c - S * 0.08, c + S * 0.26, c + S * 0.34], radius=110, fill=SKIN, outline=SKIND, width=8)
    for k in range(4):
        x = c - S * 0.21 + k * S * 0.14
        h = S * (0.30 if k in (1, 2) else 0.25)
        d.rounded_rectangle([x - S * 0.06, c - S * 0.06 - h, x + S * 0.06, c + S * 0.02], radius=50, fill=SKIN, outline=SKIND, width=8)
    d.rounded_rectangle([c + S * 0.18, c + S * 0.02, c + S * 0.42, c + S * 0.14], radius=50, fill=SKIN, outline=SKIND, width=8)
    d.rounded_rectangle([c - S * 0.24, c - S * 0.06, c + S * 0.24, c + S * 0.30], radius=100, fill=SKIN)
    face(d, c, c + S * 0.12, S * 0.18, mouth_open, blink)
    return finish(im, size)


def foot(mouth_open=False, blink=False, size=440):
    """Round little foot with five toes and a blue sock cuff."""
    S = 880; im, d = canvas(S); c = S / 2
    d.rounded_rectangle([c - S * 0.30, c - S * 0.40, c + S * 0.02, c - S * 0.10], radius=40, fill=(70, 150, 220), outline=(40, 100, 170), width=8)
    d.line([(c - S * 0.28, c - S * 0.30), (c, c - S * 0.30)], fill=(255, 255, 255), width=14)
    d.ellipse([c - S * 0.34, c - S * 0.18, c + S * 0.38, c + S * 0.34], fill=SKIN, outline=SKIND, width=8)
    for k, r in enumerate((0.075, 0.062, 0.056, 0.050, 0.044)):
        x = c + S * (0.30 - k * 0.0) if False else c + S * 0.36 - k * S * 0.04
        y = c - S * 0.10 + k * S * 0.10
        rr = S * r
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=SKIN, outline=SKIND, width=6)
    face(d, c - S * 0.02, c + S * 0.10, S * 0.18, mouth_open, blink)
    return finish(im, size)


def nose(mouth_open=False, blink=False, size=440):
    """Round pink button nose with two nostrils and a shine."""
    S = 880; im, d = canvas(S); c = S / 2
    P, PD = (245, 150, 165), (200, 95, 115)
    d.ellipse([c - S * 0.38, c - S * 0.06, c - S * 0.10, c + S * 0.30], fill=P, outline=PD, width=8)
    d.ellipse([c + S * 0.10, c - S * 0.06, c + S * 0.38, c + S * 0.30], fill=P, outline=PD, width=8)
    d.rounded_rectangle([c - S * 0.22, c - S * 0.42, c + S * 0.22, c + S * 0.28], radius=160, fill=P, outline=PD, width=8)
    d.ellipse([c - S * 0.36, c - S * 0.04, c - S * 0.12, c + S * 0.28], fill=P)
    d.ellipse([c + S * 0.12, c - S * 0.04, c + S * 0.36, c + S * 0.28], fill=P)
    d.rounded_rectangle([c - S * 0.20, c - S * 0.40, c + S * 0.20, c + S * 0.26], radius=150, fill=P)
    for sx in (-1, 1):
        d.ellipse([c + sx * S * 0.24 - S * 0.05, c + S * 0.16, c + sx * S * 0.24 + S * 0.05, c + S * 0.24], fill=PD)
    d.ellipse([c - S * 0.12, c - S * 0.34, c - S * 0.02, c - S * 0.22], fill=(255, 225, 230))
    face(d, c, c - S * 0.02, S * 0.17, mouth_open, blink)
    return finish(im, size)


def ear(mouth_open=False, blink=False, size=440):
    """Big friendly ear shape with a soft inner swirl and purple music notes."""
    S = 880; im, d = canvas(S); c = S / 2
    d.ellipse([c - S * 0.28, c - S * 0.42, c + S * 0.28, c + S * 0.30], fill=SKIN, outline=SKIND, width=8)
    d.ellipse([c - S * 0.10, c + S * 0.14, c + S * 0.14, c + S * 0.42], fill=SKIN, outline=SKIND, width=8)
    d.ellipse([c - S * 0.26, c - S * 0.40, c + S * 0.26, c + S * 0.28], fill=SKIN)
    d.arc([c - S * 0.20, c - S * 0.34, c + S * 0.20, c + S * 0.10], 180, 360, fill=(240, 165, 140), width=20)
    for (dx, dy) in ((0.36, -0.30), (-0.38, -0.20)):
        x, y = c + dx * S, c + dy * S
        d.ellipse([x - 26, y + 30, x + 18, y + 64], fill=(120, 90, 210))
        d.line([(x + 14, y + 46), (x + 14, y - 40)], fill=(120, 90, 210), width=10)
        d.line([(x + 14, y - 40), (x + 44, y - 20)], fill=(120, 90, 210), width=10)
    face(d, c, c + S * 0.04, S * 0.17, mouth_open, blink)
    return finish(im, size)


GUESTS = {'hand': hand, 'foot': foot, 'nose': nose, 'ear': ear}

if __name__ == '__main__':
    sheet = Image.new('RGBA', (1800, 480), (250, 225, 200, 255))
    for k, f in enumerate([hand, foot, nose, ear]):
        sheet.alpha_composite(f(k % 2 == 0, False, 440), (k * 450, 20))
    sheet.convert('RGB').save('guests.jpg', quality=88)
