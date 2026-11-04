"""Topic: "Look Up at the Sky" (weather)."""
import math
from PIL import Image, ImageDraw
from chars import canvas, face, finish

TITLE = 'Look Up at the Sky'
TOPIC = 'weather'
VOICE = 'af_heart'
INTRO_LINE = "Hi friends! It's Tavo! Let's sing about the weather!"
OUTRO_LINE = "Bye bye, friends! See you next time with Tavo!"
CHORUS_TITLE = 'Hello, sky!'
OUTRO_TITLE = 'Bye bye, sky!'

THEMES = {
    'title': dict(top=(170, 222, 255), bot=(232, 248, 255), col=(216, 27, 96), rainbow=True),
    'sunny': dict(top=(255, 246, 205), bot=(255, 214, 130), col=(226, 120, 0)),
    'rainy': dict(top=(214, 228, 245), bot=(165, 196, 232), col=(30, 100, 190)),
    'windy': dict(top=(226, 248, 236), bot=(170, 226, 200), col=(20, 135, 110)),
    'snowy': dict(top=(238, 240, 255), bot=(198, 208, 245), col=(90, 80, 200)),
    'sky':   dict(top=(170, 222, 255), bot=(232, 248, 255), col=(216, 27, 96), rainbow=True),
    'end':   dict(top=(170, 222, 255), bot=(232, 248, 255), col=(216, 27, 96), rainbow=True),
}

VERSES = [
    dict(guest='sunny', word='SUNNY', theme='sunny'),
    dict(guest='raindrop', word='RAINY', theme='rainy'),
    dict(guest='breeze', word='WINDY', theme='windy'),
    dict(guest='snowflake', word='SNOWY', theme='snowy'),
]
THUMB = dict(lines=['Look Up at', 'the Sky'], theme='title')


def sunny(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2; r = S * 0.25
    for k in range(10):
        a = k * math.pi / 5
        p = [(c + S * 0.46 * math.cos(a), c + S * 0.46 * math.sin(a)),
             (c + S * 0.29 * math.cos(a + .24), c + S * 0.29 * math.sin(a + .24)),
             (c + S * 0.29 * math.cos(a - .24), c + S * 0.29 * math.sin(a - .24))]
        d.polygon(p, fill=(255, 150, 30))
    d.ellipse([c - r * 1.15, c - r * 1.15, c + r * 1.15, c + r * 1.15], fill=(255, 205, 40), outline=(240, 150, 20), width=8)
    face(d, c, c - r * 0.1, r * 1.05, mouth_open, blink)
    return finish(im, size)


def raindrop(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    col, ln = (120, 140, 175), (85, 105, 140)
    for ox, oy, rr in [(-.22, -.1, .17), (.22, -.1, .17), (0, -.2, .22)]:
        x, y, r = c + ox * S, c + oy * S, rr * S
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    d.rounded_rectangle([c - S * .36, c - S * .15, c + S * .36, c + S * .1], radius=70, fill=col)
    face(d, c, c - S * .1, S * .2, mouth_open, blink)
    for ox, oy in [(-.26, .2), (0, .3), (.26, .2)]:
        x, y, r = c + ox * S, c + oy * S, S * .05
        d.polygon([(x, y - r * 2.1), (x - r * .85, y - r * .2), (x + r * .85, y - r * .2)], fill=(40, 130, 230))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(40, 130, 230))
    return finish(im, size)


def breeze(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    col, w = (60, 170, 150), int(S * .05)
    for y0, x1, rr in [(-.26, .3, .08), (.28, .24, .07)]:
        y = c + y0 * S; x = c + x1 * S; r = rr * S
        d.line([c - S * .44, y, x, y], fill=col, width=w)
        d.arc([x - r, y - 2 * r, x + r, y], -90, 90, fill=col, width=w) if y0 < 0 else d.arc([x - r, y, x + r, y + 2 * r], -90, 90, fill=col, width=w)
    r = S * .24
    d.ellipse([c - r, c - r, c + r, c + r], fill=(150, 232, 210), outline=col, width=9)
    face(d, c, c - r * .1, r * 1.0, mouth_open, blink)
    return finish(im, size)


def snowflake(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    col = (90, 120, 225)
    for k in range(6):
        a = k * math.pi / 3
        ca, sa = math.cos(a), math.sin(a)
        d.line([c, c, c + S * .46 * ca, c + S * .46 * sa], fill=col, width=int(S * .035))
        bx, by = c + S * .36 * ca, c + S * .36 * sa
        for t in (.7, -.7):
            d.line([bx, by, bx + S * .1 * math.cos(a + t), by + S * .1 * math.sin(a + t)], fill=col, width=int(S * .03))
    r = S * .23
    d.ellipse([c - r, c - r, c + r, c + r], fill='white', outline=col, width=9)
    face(d, c, c - r * .1, r * 1.0, mouth_open, blink)
    return finish(im, size)


GUESTS = {'sunny': sunny, 'raindrop': raindrop, 'breeze': breeze, 'snowflake': snowflake}
