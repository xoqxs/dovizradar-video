"""Topic file for ONE song: "Splash, Who Is in the Sea?" (ocean animals)."""
from PIL import ImageDraw
from chars import canvas, face, finish

TITLE = 'Splash, Who Is in the Sea?'
TOPIC = 'ocean animals'
VOICE = 'af_heart'
INTRO_LINE = "Hi friends! It's Tavo! Let's sing about animals in the sea!"
OUTRO_LINE = "Bye bye, friends! See you next time with Tavo!"
CHORUS_TITLE = "Splash and play!"
OUTRO_TITLE = 'Bye, swimmers!'

SEA = dict(top=(190, 236, 255), bot=(150, 214, 236), col=(0, 110, 170), rainbow=True)
THEMES = {
    'title':   SEA,
    'fish':    dict(top=(255, 244, 226), bot=(255, 214, 170), col=(226, 110, 20)),
    'crab':    dict(top=(255, 240, 236), bot=(255, 206, 196), col=(206, 50, 50)),
    'octopus': dict(top=(246, 236, 255), bot=(220, 200, 250), col=(130, 70, 200)),
    'whale':   dict(top=(230, 244, 255), bot=(176, 214, 250), col=(30, 90, 190)),
    'sea':     SEA,
    'end':     SEA,
}

VERSES = [
    dict(guest='fish', word='FISH', theme='fish'),
    dict(guest='crab', word='CRAB', theme='crab'),
    dict(guest='octopus', word='OCTOPUS', theme='octopus'),
    dict(guest='whale', word='WHALE', theme='whale'),
]

THUMB = dict(lines=['Splash! Who Is', 'in the Sea?'], theme='title')


def fish(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    d.polygon([(c + 230, c), (c + 420, c - 190), (c + 420, c + 190)], fill=(255, 170, 40), outline=(205, 115, 20))
    d.polygon([(c - 60, c - 190), (c + 90, c - 330), (c + 140, c - 170)], fill=(255, 196, 70), outline=(205, 115, 20))
    d.ellipse([c - 360, c - 230, c + 300, c + 230], fill=(255, 150, 40), outline=(205, 105, 20), width=8)
    for k in (0, 1):
        x = c + 20 + k * 110
        d.arc([x - 60, c - 180, x + 60, c + 180], 300, 60, fill=(255, 220, 140), width=14)
    d.polygon([(c - 20, c + 120), (c + 110, c + 240), (c + 120, c + 110)], fill=(255, 196, 70), outline=(205, 115, 20))
    face(d, c - 150, c - 10, 170, mouth_open, blink, blush=True)
    return finish(im, size)


def crab(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    LC = (180, 40, 40)
    for sx in (-1, 1):
        for k in range(3):
            y = c + 60 + k * 70
            d.line([(c + sx * 200, y), (c + sx * 360, y + 60)], fill=LC, width=26)
        d.line([(c + sx * 220, c - 40), (c + sx * 320, c - 200)], fill=LC, width=30)
        x, y = c + sx * 330, c - 270
        d.ellipse([x - 95, y - 95, x + 95, y + 95], fill=(236, 70, 60), outline=LC, width=7)
        d.polygon([(x, y), (x + sx * 40 - 50, y - 110), (x + sx * 40 + 50, y - 110)], fill=(255, 255, 255, 0))
        d.pieslice([x - 100, y - 100, x + 100, y + 100], 245 if sx < 0 else 255, 295 if sx < 0 else 305, fill=(0, 0, 0, 0))
    d.ellipse([c - 270, c - 180, c + 270, c + 230], fill=(240, 78, 66), outline=LC, width=8)
    face(d, c, c + 10, 190, mouth_open, blink, blush=True)
    return finish(im, size)


def octopus(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    P, PO = (168, 110, 230), (115, 70, 180)
    for k in range(8):
        x = c - 315 + k * 90
        d.rounded_rectangle([x - 36, c + 20, x + 36, c + 340 + (k % 2) * 40], radius=36, fill=P, outline=PO, width=6)
        d.ellipse([x - 14, c + 250 + (k % 2) * 40, x + 14, c + 278 + (k % 2) * 40], fill=(226, 200, 255))
    d.ellipse([c - 300, c - 360, c + 300, c + 190], fill=P, outline=PO, width=8)
    d.ellipse([c - 200, c - 300, c - 110, c - 230], fill=(200, 160, 245))
    face(d, c, c - 70, 210, mouth_open, blink, blush=True)
    return finish(im, size)


def whale(mouth_open=False, blink=False, size=440):
    S = 880; im, d = canvas(S); c = S / 2
    B, BO = (70, 140, 230), (35, 90, 170)
    for sx in (-1, 1):
        d.ellipse([c + sx * 70 - 60, c - 400, c + sx * 70 + 60, c - 300], fill=(150, 210, 255))
    d.rounded_rectangle([c - 18, c - 340, c + 18, c - 200], radius=18, fill=(150, 210, 255))
    d.polygon([(c + 270, c + 40), (c + 430, c - 120), (c + 430, c + 200)], fill=B, outline=BO)
    d.ellipse([c - 400, c - 220, c + 320, c + 290], fill=B, outline=BO, width=8)
    d.chord([c - 330, c - 20, c + 250, c + 270], 0, 180, fill=(214, 236, 255))
    face(d, c - 80, c - 30, 200, mouth_open, blink, blush=True)
    return finish(im, size)


GUESTS = {'fish': fish, 'crab': crab, 'octopus': octopus, 'whale': whale}
