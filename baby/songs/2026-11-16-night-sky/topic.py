"""Topic file for ONE song: "Who Is Awake at Night?" (bedtime / night sky)."""
import math
from PIL import Image, ImageDraw
from chars import canvas, face, finish

TITLE = 'Who Is Awake at Night?'
TOPIC = 'bedtime / night sky'
VOICE = 'af_heart'
INTRO_LINE = "Hi friends! It's Tavo! It's bedtime, but I can't sleep. Who is still awake out there? Let's sing!"
OUTRO_LINE = "Good night, friends! Sweet dreams, and see you next time with Tavo!"
CHORUS_TITLE = 'Soft night song!'
OUTRO_TITLE = 'Good night!'

NIGHT = dict(top=(20, 30, 80), bot=(70, 70, 150), col=(255, 200, 60), scene='night')
THEMES = {
    'title': NIGHT,
    'moon':  dict(NIGHT, col=(255, 210, 70)),
    'star':  dict(NIGHT, col=(255, 160, 40)),
    'owl':   dict(NIGHT, col=(170, 110, 60)),
    'cloud': dict(NIGHT, col=(120, 160, 230)),
    'night': NIGHT,
    'end':   NIGHT,
}

VERSES = [
    dict(guest='moon', word='MOON', theme='moon', motion='fly'),
    dict(guest='star', word='STAR', theme='star', motion='bounce'),
    dict(guest='owl', word='OWL', theme='owl', motion='hop'),
    dict(guest='cloud', word='CLOUD', theme='cloud', motion='fly'),
]

THUMB = dict(lines=['Who Is Awake', 'at Night?'], theme='title')

INK = (50, 40, 60)


def moon(mouth_open=False, blink=False, size=440):
    """Round full moon with soft craters and a little nightcap."""
    S = 880; im, d = canvas(S); c = S / 2
    r = S * 0.36
    d.ellipse([c - r, c - r + 30, c + r, c + r + 30], fill=(255, 232, 130), outline=(225, 185, 60), width=10)
    for x, y, k in [(-0.2, -0.12, 0.06), (0.22, 0.2, 0.05), (0.2, -0.18, 0.035), (-0.24, 0.22, 0.04)]:
        rr = S * k
        d.ellipse([c + x * S - rr, c + y * S - rr + 30, c + x * S + rr, c + y * S + rr + 30], fill=(240, 205, 100))
    # nightcap (blue, droopy, with pompom)
    d.polygon([(c - S * 0.30, c - S * 0.18), (c + S * 0.26, c - S * 0.24), (c + S * 0.34, c - S * 0.44),
               (c - S * 0.02, c - S * 0.46)], fill=(90, 110, 210), outline=(60, 75, 160))
    d.rounded_rectangle([c - S * 0.33, c - S * 0.24, c + S * 0.29, c - S * 0.15], radius=24, fill=(240, 240, 255))
    d.ellipse([c + S * 0.30, c - S * 0.50, c + S * 0.42, c - S * 0.38], fill=(240, 240, 255))
    face(d, c, c + S * 0.08, S * 0.30, mouth_open, blink)
    return finish(im, size)


def star(mouth_open=False, blink=False, size=440):
    """Chubby five-point star."""
    S = 880; im, d = canvas(S); c = S / 2
    def pts(R, r, cy):
        p = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            rad = R if k % 2 == 0 else r
            p.append((c + rad * math.cos(a), cy + rad * math.sin(a)))
        return p
    cy = c + S * 0.03
    d.polygon(pts(S * 0.46, S * 0.24, cy), fill=(225, 160, 20))
    d.polygon(pts(S * 0.42, S * 0.21, cy), fill=(255, 210, 50))
    for x, y in [(-0.36, -0.36), (0.38, -0.30), (0.36, 0.36)]:  # sparkles
        sx, sy = c + x * S, c + y * S
        d.line([sx - 22, sy, sx + 22, sy], fill=(255, 250, 210), width=8)
        d.line([sx, sy - 22, sx, sy + 22], fill=(255, 250, 210), width=8)
    face(d, c, cy + S * 0.03, S * 0.24, mouth_open, blink)
    return finish(im, size)


def owl(mouth_open=False, blink=False, size=440):
    """Round brown owl with ear tufts, big eye discs and wings."""
    S = 880; im, d = canvas(S); c = S / 2
    B, BD, BL = (165, 110, 65), (115, 72, 40), (235, 205, 160)
    d.polygon([(c - S * 0.30, c - S * 0.22), (c - S * 0.36, c - S * 0.44), (c - S * 0.14, c - S * 0.30)], fill=BD)
    d.polygon([(c + S * 0.30, c - S * 0.22), (c + S * 0.36, c - S * 0.44), (c + S * 0.14, c - S * 0.30)], fill=BD)
    for sx in (-1, 1):  # wings
        d.ellipse([c + sx * S * 0.30 - S * 0.12, c - S * 0.02, c + sx * S * 0.30 + S * 0.12, c + S * 0.34], fill=BD)
    d.ellipse([c - S * 0.34, c - S * 0.34, c + S * 0.34, c + S * 0.42], fill=B, outline=BD, width=8)
    d.ellipse([c - S * 0.20, c + S * 0.06, c + S * 0.20, c + S * 0.38], fill=BL)  # belly
    for k in range(3):
        y = c + S * (0.14 + k * 0.08)
        d.arc([c - S * 0.06, y - S * 0.03, c + S * 0.06, y + S * 0.03], 0, 180, fill=B, width=6)
    for sx in (-1, 1):  # eye discs
        x = c + sx * S * 0.14
        d.ellipse([x - S * 0.13, c - S * 0.22, x + S * 0.13, c + S * 0.04], fill=(250, 240, 215), outline=BD, width=6)
    for sx in (-1, 1):  # feet
        x = c + sx * S * 0.10
        d.ellipse([x - S * 0.06, c + S * 0.38, x + S * 0.06, c + S * 0.45], fill=(245, 170, 50))
    face(d, c, c - S * 0.09, S * 0.26, mouth_open, blink, blush=False, mouth_dy=S * 0.06)
    d.polygon([(c - S * 0.035, c - S * 0.03), (c + S * 0.035, c - S * 0.03), (c, c + S * 0.02)], fill=(245, 170, 50))
    return finish(im, size)


def cloud(mouth_open=False, blink=False, size=440):
    """Fluffy sleepy cloud with a tiny pillow-puff."""
    S = 880; im, d = canvas(S); c = S / 2
    W, O = (250, 250, 255), (170, 185, 225)
    puffs = [(-0.24, 0.06, 0.18), (0.0, -0.06, 0.24), (0.24, 0.04, 0.19), (-0.10, 0.12, 0.17), (0.12, 0.13, 0.17)]
    for x, y, r in puffs:
        d.ellipse([c + (x - r) * S - 8, c + (y - r) * S - 8, c + (x + r) * S + 8, c + (y + r) * S + 8], fill=O)
    for x, y, r in puffs:
        d.ellipse([c + (x - r) * S, c + (y - r) * S, c + (x + r) * S, c + (y + r) * S], fill=W)
    for k, (x, y) in enumerate([(0.36, -0.22), (0.43, -0.32)]):  # little 'z' puffs
        rr = S * (0.035 + 0.015 * k)
        d.ellipse([c + x * S - rr, c + y * S - rr, c + x * S + rr, c + y * S + rr], fill=(220, 230, 255))
    face(d, c, c + S * 0.04, S * 0.27, mouth_open, blink)
    return finish(im, size)


GUESTS = {'moon': moon, 'star': star, 'owl': owl, 'cloud': cloud}

if __name__ == '__main__':
    sheet = Image.new('RGBA', (1800, 480), (40, 50, 110, 255))
    for k, f in enumerate([moon, star, owl, cloud]):
        sheet.alpha_composite(f(k % 2 == 0, False, 440), (k * 450, 20))
    sheet.convert('RGB').save('guests.jpg', quality=88)
