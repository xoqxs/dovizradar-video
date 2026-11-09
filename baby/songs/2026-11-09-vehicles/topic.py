"""Topic file for ONE song: "Beep Beep, Who Is Here?" (vehicles + sounds)."""
from PIL import ImageDraw
from chars import canvas, face, finish

TITLE = 'Beep Beep, Who Is Here?'
TOPIC = 'vehicles'
VOICE = 'af_heart'
INTRO_LINE = "Hi friends! It's Tavo! Let's sing about things that go!"
OUTRO_LINE = "Bye bye, friends! See you next time with Tavo!"
CHORUS_TITLE = "Let's all ride!"
OUTRO_TITLE = 'Bye, riders!'

SKY = dict(top=(176, 226, 255), bot=(236, 246, 200), col=(226, 80, 40), rainbow=True)
THEMES = {
    'title': SKY,
    'car':   dict(top=(255, 238, 232), bot=(255, 204, 190), col=(214, 50, 50)),
    'train': dict(top=(232, 242, 255), bot=(186, 214, 250), col=(40, 90, 190)),
    'boat':  dict(top=(228, 246, 255), bot=(150, 220, 236), col=(0, 130, 150)),
    'plane': dict(top=(226, 240, 255), bot=(250, 236, 214), col=(110, 80, 190)),
    'road':  SKY,
    'end':   SKY,
}

VERSES = [
    dict(guest='car', word='CAR', theme='car'),
    dict(guest='train', word='TRAIN', theme='train'),
    dict(guest='boat', word='BOAT', theme='boat'),
    dict(guest='plane', word='PLANE', theme='plane'),
]

THUMB = dict(lines=['Beep Beep,', 'Who Is Here?'], theme='title')

INK = (70, 70, 90)
def wheel(d, x, y, r):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(60, 60, 75))
    d.ellipse([x - r * .45, y - r * .45, x + r * .45, y + r * .45], fill=(235, 235, 240))


def car(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    d.rounded_rectangle([c - 210, c - 250, c + 210, c + 60], radius=90, fill=(232, 62, 62), outline=(170, 40, 40), width=7)
    d.rounded_rectangle([c - 165, c - 210, c + 165, c + 30], radius=60, fill=(214, 240, 255), outline=(170, 40, 40), width=6)
    d.rounded_rectangle([c - 350, c - 20, c + 350, c + 190], radius=80, fill=(240, 72, 70), outline=(170, 40, 40), width=7)
    for sx in (-1, 1):
        wheel(d, c + sx * 215, c + 200, 88)
        d.ellipse([c + sx * 300 - 34, c + 50, c + sx * 300 + 34, c + 118], fill=(255, 226, 110), outline=(200, 150, 40), width=4)
    face(d, c, c - 125, 175, mouth_open, blink, blush=True)
    return finish(im, size)


def train(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    d.rounded_rectangle([c - 70, c - 390, c + 70, c - 200], radius=20, fill=(70, 70, 90))
    d.rounded_rectangle([c - 100, c - 410, c + 100, c - 350], radius=24, fill=(250, 196, 50), outline=(190, 140, 20), width=5)
    for sx in (-1, 1):
        d.rounded_rectangle([c + sx * 300 - 40, c - 40, c + sx * 300 + 40, c + 260], radius=16, fill=(60, 60, 75))
    d.ellipse([c - 300, c - 260, c + 300, c + 300], fill=(58, 122, 226), outline=(30, 80, 170), width=8)
    d.ellipse([c - 225, c - 190, c + 225, c + 230], fill=(226, 240, 255), outline=(30, 80, 170), width=6)
    d.polygon([(c - 260, c + 380), (c + 260, c + 380), (c + 170, c + 270), (c - 170, c + 270)], fill=(250, 196, 50), outline=(190, 140, 20))
    face(d, c, c - 10, 240, mouth_open, blink, blush=True)
    return finish(im, size)


def boat(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    d.rounded_rectangle([c - 12, c - 400, c + 12, c + 40], radius=10, fill=(150, 100, 60))
    d.polygon([(c + 22, c - 380), (c + 280, c - 20), (c + 22, c - 20)], fill=(255, 255, 255), outline=(190, 190, 205))
    d.polygon([(c - 22, c - 320), (c - 240, c - 20), (c - 22, c - 20)], fill=(255, 208, 60), outline=(205, 160, 30))
    d.chord([c - 370, c - 240, c + 370, c + 360], 0, 180, fill=(255, 150, 60), outline=(205, 105, 30), width=7)
    d.rectangle([c - 370, c + 40, c + 370, c + 62], fill=(255, 255, 255))
    for k in range(-3, 4):
        x = c + k * 130
        d.ellipse([x - 90, c + 300, x + 90, c + 400], fill=(90, 190, 230))
    face(d, c, c + 150, 200, mouth_open, blink, blush=True)
    return finish(im, size)


def plane(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    d.polygon([(c - 40, c - 400), (c + 40, c - 400), (c + 70, c - 150), (c - 70, c - 150)], fill=(150, 110, 226), outline=(105, 75, 180))
    d.rounded_rectangle([c - 425, c - 20, c + 425, c + 90], radius=55, fill=(150, 110, 226), outline=(105, 75, 180), width=7)
    for sx in (-1, 1):
        d.ellipse([c + sx * 340 - 40, c + 75, c + sx * 340 + 40, c + 175], fill=(250, 196, 50), outline=(190, 140, 20), width=5)
    d.ellipse([c - 235, c - 245, c + 235, c + 275], fill=(226, 232, 244), outline=(120, 130, 155), width=8)
    d.ellipse([c - 170, c - 190, c + 170, c + 190], fill=(250, 252, 255))
    wheel(d, c, c + 325, 60)
    face(d, c, c - 10, 205, mouth_open, blink, blush=True)
    return finish(im, size)


GUESTS = {'car': car, 'train': train, 'boat': boat, 'plane': plane}
