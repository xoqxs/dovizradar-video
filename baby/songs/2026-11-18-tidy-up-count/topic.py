"""Topic file for ONE song: "Tidy Up and Count!" (counting 1-4 with toys)."""
import math
from PIL import Image, ImageDraw
from chars import canvas, face, finish

TITLE = 'Tidy Up and Count!'
TOPIC = 'counting 1-4 with toys'
VOICE = 'af_heart'
INTRO_LINE = "Hi friends! It's Tavo! Oh no, my toys are everywhere! Let's find them, count them, and sing!"
OUTRO_LINE = "Bye bye, friends! My room is tidy. See you next time with Tavo!"
CHORUS_TITLE = 'Tidy up!'
OUTRO_TITLE = 'All tidy!'

ROOM = dict(top=(220, 238, 255), bot=(195, 222, 248), col=(80, 170, 120), scene='room')
THEMES = {
    'title': ROOM,
    'ball':  dict(ROOM, col=(230, 70, 60)),
    'block': dict(ROOM, col=(70, 130, 230)),
    'car':   dict(ROOM, col=(240, 140, 40)),
    'duck':  dict(ROOM, col=(245, 200, 40)),
    'tidy':  ROOM,
    'end':   ROOM,
}

VERSES = [
    dict(guest='ball', word='BALL', theme='ball', motion='bounce'),
    dict(guest='block', word='BLOCK', theme='block', motion='hop'),
    dict(guest='car', word='CAR', theme='car', motion='drive'),
    dict(guest='duck', word='DUCK', theme='duck', motion='swim'),
]

THUMB = dict(lines=['Tidy Up', 'and Count!'], theme='title')


def ball(mouth_open=False, blink=False, size=440):
    """Round red play ball with a white stripe and star."""
    S = 880; im, d = canvas(S); c = S / 2
    r = S * 0.40
    d.ellipse([c - r, c - r, c + r, c + r], fill=(230, 70, 60), outline=(170, 40, 35), width=10)
    d.chord([c - r + 6, c - r + 6, c + r - 6, c + r - 6], 200, 340, fill=(255, 240, 230))
    d.ellipse([c - r * 0.62, c - r * 0.62, c - r * 0.30, c - r * 0.30], fill=(255, 255, 255, 120))
    face(d, c, c + S * 0.06, S * 0.30, mouth_open, blink)
    return finish(im, size)


def block(mouth_open=False, blink=False, size=440):
    """Blue toy block with a yellow number frame."""
    S = 880; im, d = canvas(S); c = S / 2
    h = S * 0.36
    d.polygon([(c - h, c - h + 40), (c - h + 80, c - h - 30), (c + h + 80, c - h - 30), (c + h, c - h + 40)], fill=(120, 170, 245))
    d.polygon([(c + h, c - h + 40), (c + h + 80, c - h - 30), (c + h + 80, c + h - 70), (c + h, c + h)], fill=(45, 95, 190))
    d.rounded_rectangle([c - h, c - h + 40, c + h, c + h], radius=26, fill=(70, 130, 230), outline=(40, 85, 170), width=10)
    d.rounded_rectangle([c - h + 40, c - h + 80, c + h - 40, c + h - 40], radius=22, outline=(255, 215, 60), width=14)
    face(d, c, c + S * 0.06, S * 0.28, mouth_open, blink)
    return finish(im, size)


def car(mouth_open=False, blink=False, size=440):
    """Little orange toy car with round windows and big wheels."""
    S = 880; im, d = canvas(S); c = S / 2
    O, OD = (245, 145, 45), (190, 100, 25)
    d.rounded_rectangle([c - S * 0.24, c - S * 0.30, c + S * 0.20, c - S * 0.02], radius=60, fill=O, outline=OD, width=10)
    d.rounded_rectangle([c - S * 0.18, c - S * 0.25, c - S * 0.04, c - S * 0.08], radius=20, fill=(190, 230, 255))
    d.rounded_rectangle([c + S * 0.00, c - S * 0.25, c + S * 0.14, c - S * 0.08], radius=20, fill=(190, 230, 255))
    d.rounded_rectangle([c - S * 0.42, c - S * 0.08, c + S * 0.42, c + S * 0.22], radius=60, fill=O, outline=OD, width=10)
    d.ellipse([c + S * 0.32, c - S * 0.02, c + S * 0.40, c + S * 0.06], fill=(255, 240, 150))
    for x in (-0.25, 0.25):
        d.ellipse([c + x * S - S * 0.11, c + S * 0.14, c + x * S + S * 0.11, c + S * 0.36], fill=(55, 50, 60))
        d.ellipse([c + x * S - S * 0.045, c + S * 0.205, c + x * S + S * 0.045, c + S * 0.295], fill=(210, 210, 220))
    face(d, c, c + S * 0.06, S * 0.22, mouth_open, blink)
    return finish(im, size)


def duck(mouth_open=False, blink=False, size=440):
    """Yellow bath-toy duck with an orange beak."""
    S = 880; im, d = canvas(S); c = S / 2
    Y, YD = (255, 212, 50), (215, 165, 20)
    d.ellipse([c - S * 0.40, c - S * 0.02, c + S * 0.36, c + S * 0.40], fill=Y, outline=YD, width=10)
    d.polygon([(c - S * 0.30, c + S * 0.08), (c - S * 0.48, c - S * 0.06), (c - S * 0.38, c + S * 0.20)], fill=Y, outline=YD)
    d.ellipse([c - S * 0.28, c - S * 0.40, c + S * 0.12, c + S * 0.02], fill=Y, outline=YD, width=10)
    d.ellipse([c - S * 0.04, c + S * 0.10, c + S * 0.26, c + S * 0.28], fill=(240, 190, 30))
    d.ellipse([c + S * 0.06, c - S * 0.22, c + S * 0.26, c - S * 0.12], fill=(245, 130, 40))
    d.ellipse([c + S * 0.06, c - S * 0.16, c + S * 0.24, c - S * 0.07], fill=(225, 105, 30))
    face(d, c - S * 0.10, c - S * 0.20, S * 0.16, mouth_open, blink, mouth_dy=S * 0.06)
    return finish(im, size)


GUESTS = {'ball': ball, 'block': block, 'car': car, 'duck': duck}

if __name__ == '__main__':
    sheet = Image.new('RGBA', (1800, 480), (210, 230, 250, 255))
    for k, f in enumerate([ball, block, car, duck]):
        sheet.alpha_composite(f(k % 2 == 0, False, 440), (k * 450, 20))
    sheet.convert('RGB').save('guests.jpg', quality=88)
