"""Sing with Tavo – weekly compilation builder (Sunday video).

  python3 compile.py OUT.mp4 "Compilation title" SONG1.mp4 "Song 1 title" [SONG2.mp4 "Song 2 title" ...]
  python3 compile.py --thumb OUT.jpg "Compilation title" SONG1_THUMB_GUEST...  (see thumb())

Builds: Tavo intro card (~6 s, signature sting + hello) -> song 1 -> "Next song" card (~3 s) -> song 2 ... -> bye card (~5 s).
Songs must be the finished 1920x1080 long videos. Total must be >= 8:00 (exit code 2 otherwise: add more songs).
Needs chars.py + Fredoka-Bold.ttf next to it; Kokoro model in /home/claude/tts (falls back to sting only).
"""
import math, os, sys, subprocess, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import soundfile as sf
import chars as C

W, H, FPS, SR = 1920, 1080, 30, 48000
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = next(p for p in ['Fredoka-Bold.ttf', os.path.join(HERE, 'Fredoka-Bold.ttf')] if os.path.exists(p))
_fc = {}


def font(sz):
    sz = max(6, int(sz))
    if sz not in _fc:
        _fc[sz] = ImageFont.truetype(FONT, sz)
    return _fc[sz]


def text(d, x, y, s, sz, fill, stroke=10):
    d.text((x, y), s, font=font(sz), fill=fill, anchor='mm', stroke_width=stroke, stroke_fill='white')


def ease_back(u):
    u = min(max(u, 0.0), 1.0); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (u - 1) ** 3 + c1 * (u - 1) ** 2


_BG = None


def bg():
    global _BG
    if _BG is None:
        y = np.linspace(0, 1, H)[:, None, None]
        arr = (np.array((170, 222, 255)) * (1 - y) + np.array((232, 248, 255)) * y) * np.ones((1, W, 1))
        im = Image.fromarray(arr.astype(np.uint8))
        d = ImageDraw.Draw(im, 'RGBA')
        cols = [(244, 67, 54), (255, 152, 0), (255, 235, 59), (76, 175, 80), (33, 150, 243), (103, 58, 183)]
        for i, cl in enumerate(cols):
            r = 900 - i * 48
            d.ellipse([960 - r, 980 - r, 960 + r, 980 + r], fill=cl + (255,))
        r = 900 - 6 * 48
        m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).ellipse([960 - r, 980 - r, 960 + r, 980 + r], fill=255)
        im.paste(Image.fromarray(arr.astype(np.uint8)), (0, 0), m)
        d = ImageDraw.Draw(im, 'RGBA')
        d.ellipse([-300, 760, W + 300, 1500], fill=(115, 190, 80))
        d.ellipse([-200, 790, W + 200, 1500], fill=(140, 215, 105))
        _BG = im.convert('RGBA')
    return _BG


_S = {}


def spr(name, mo, bl, size, **kw):
    k = (name, mo, bl, size, tuple(sorted(kw.items())))
    if k not in _S:
        _S[k] = C.CREW[name](mo, bl, size, **kw)
    return _S[k]


def paste(base, im, cx, cy, s=1.0):
    if s <= 0.02:
        return
    if abs(s - 1) > 1e-3:
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def wrap(s, n=22):
    words, lines, cur = s.split(), [], ''
    for w in words:
        if len(cur) + len(w) + 1 > n and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + ' ' + w).strip()
    lines.append(cur)
    return lines[:2]


def card_frame(kind, t, title, env):
    base = bg().copy()
    talk = env is not None and int(t * FPS) < len(env) and env[int(t * FPS)] > 0.12
    b = abs(math.sin(math.pi * t * 1.8))
    blink = (t % 3.1) < 0.12
    if kind == 'intro':
        paste(base, spr('tavo', talk, blink, 560, case_open=t > 1.2, wave=t < 1.2), 960, 610 - b * 14)
        for k, (nm, x, y, s) in enumerate([('rosy', 470, 690, 320), ('rubbo', 1450, 720, 300), ('lino', 1700, 650, 330)]):
            paste(base, spr(nm, False, blink, s), x, y - b * 10, ease_back((t - 1.3 - 0.3 * k) / 0.6))
        d = ImageDraw.Draw(base, 'RGBA')
        text(d, 960, 80, 'Sing with Tavo', 60 * ease_back(t / 0.8), (30, 120, 220))
        for k, ln in enumerate(wrap(title, 26)):
            text(d, 960, 175 + k * 105, ln, 96 * ease_back((t - 0.3) / 0.9), (216, 27, 96), stroke=14)
    elif kind == 'next':
        paste(base, spr('tavo', talk, blink, 520, case_open=True), 560, 600 - b * 14)
        d = ImageDraw.Draw(base, 'RGBA')
        text(d, 1250, 330, 'Next song!', 110 * ease_back(t / 0.6), (30, 120, 220), stroke=12)
        for k, ln in enumerate(wrap(title, 20)):
            text(d, 1250, 480 + k * 110, ln, 100 * ease_back((t - 0.25) / 0.7), (216, 27, 96), stroke=14)
    else:  # bye
        paste(base, spr('tavo', talk, blink, 520, wave=True), 960, 590)
        for k, (nm, x, y) in enumerate([('rosy', 300, 700), ('rubbo', 560, 730), ('lino', 1400, 700)]):
            paste(base, spr(nm, False, blink, 300), x, y - b * 10)
        d = ImageDraw.Draw(base, 'RGBA')
        text(d, 960, 170, 'Bye bye!', 170 * ease_back(t / 1.0), (216, 27, 96), stroke=14)
        text(d, 960, 965, 'See you next time!', 80 * ease_back((t - 0.8) / 1.0), (30, 120, 220))
    return base.convert('RGB')


# ---------------------------------------------------------------- audio
def glock(midi, dur=1.2):
    n = int(dur * SR); t = np.arange(n) / SR
    fr = 440 * 2 ** ((midi + 12 - 69) / 12)
    return (np.sin(2 * np.pi * fr * t) * np.exp(-t * 4) + 0.3 * np.sin(2 * np.pi * fr * 2.76 * t) * np.exp(-t * 12)) * np.minimum(t / 0.002, 1)


def sting(beat=0.55):
    out = np.zeros(int(4 * beat * SR + 1.3 * SR))
    for b0, m in [(0, 79), (1, 76), (2, 79), (2.5, 84)]:
        g = glock(m); i = int(b0 * beat * SR)
        out[i:i + len(g)] += g[:len(out) - i]
    return out


_K = None


def tts(textline):
    global _K
    try:
        if _K is None:
            from kokoro_onnx import Kokoro
            _K = Kokoro('/home/claude/tts/kokoro-v1.0.onnx', '/home/claude/tts/voices-v1.0.bin')
        s, sr = _K.create(textline, voice='af_heart', speed=1.0, lang='en-us')
        from scipy.signal import resample_poly
        s = resample_poly(s, 2, 1)  # 24k -> 48k
        return s / (np.abs(s).max() + 1e-9)
    except Exception as e:  # no voice available: sting only
        print('tts unavailable:', e)
        return None


def make_card(kind, title, dur, path, line=None):
    n = int(dur * SR)
    music = np.zeros(n)
    st = sting(); music[:min(n, len(st))] += st[:n] * 0.6
    voice = np.zeros(n)
    v = tts(line) if line else None
    if v is not None:
        i = int(1.0 * SR); j = min(n, i + len(v)); voice[i:j] += v[:j - i]
    mixd = music * 0.7 + voice
    mixd = mixd / (np.abs(mixd).max() + 1e-9) * 0.8
    fade = int(0.25 * SR); mixd[-fade:] *= np.linspace(1, 0, fade)
    sf.write(path + '.wav', np.stack([mixd, mixd], 1), SR)
    hop = SR // FPS
    env = np.array([np.sqrt(np.mean(voice[k * hop:(k + 1) * hop] ** 2)) for k in range(n // hop)])
    env = env / (env.max() + 1e-9) if env.max() > 0 else None
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', path + '.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '192k', '-ar', str(SR), '-ac', '2', '-shortest', path], stdin=subprocess.PIPE)
    for f in range(int(dur * FPS)):
        p.stdin.write(card_frame(kind, f / FPS, title, env).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise SystemExit('card failed')
    return path


def duration(p):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout
    return float(out.strip())


def build(out, comp_title, songs):
    parts = [make_card('intro', comp_title, 6.0, 'c_intro.mp4', "Hi friends! It's Tavo! Let's sing all our songs together!")]
    for k, (path, title) in enumerate(songs):
        if k > 0:
            parts.append(make_card('next', title, 3.0, f'c_next{k}.mp4', 'Next song!'))
        parts.append(path)
    parts.append(make_card('bye', '', 5.0, 'c_bye.mp4', 'Bye bye, friends! See you next time with Tavo!'))
    total = sum(duration(p) for p in parts)
    print(f'total {total / 60:.2f} min from {len(songs)} songs')
    if total < 480:
        print('ERROR: shorter than 8:00 – add more songs (older songs are fine).')
        sys.exit(2)
    ins, fl = [], []
    for i, p in enumerate(parts):
        ins += ['-i', p]
        fl.append(f'[{i}:v]scale={W}:{H},fps={FPS},format=yuv420p,setsar=1[v{i}];[{i}:a]aformat=sample_rates={SR}:channel_layouts=stereo[a{i}]')
    cat = ''.join(f'[v{i}][a{i}]' for i in range(len(parts))) + f'concat=n={len(parts)}:v=1:a=1[v][a]'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(fl) + ';' + cat, '-map', '[v]', '-map', '[a]',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '27', '-tune', 'animation', '-c:a', 'aac', '-b:a', '160k', '-ar', str(SR),
                    '-movflags', '+faststart', out], check=True)
    # keep under ~48 MB (GitHub warns above 50 MB): re-encode with a bitrate cap if needed
    if os.path.getsize(out) > 48e6:
        tot = duration(out); kbps = int((46e6 * 8 / tot - 160e3) / 1000)
        tmp = out + '.tmp.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-c:v', 'libx264', '-preset', 'veryfast', '-tune', 'animation',
                        '-b:v', f'{kbps}k', '-maxrate', f'{int(kbps * 1.4)}k', '-bufsize', f'{kbps * 2}k', '-pix_fmt', 'yuv420p',
                        '-c:a', 'copy', '-movflags', '+faststart', tmp], check=True)
        os.replace(tmp, out)
    print(f'size {os.path.getsize(out) / 1e6:.1f} MB')
    # chapters for the description: first at 0:00, each >= 10 s -> intro card folded into song 1,
    # every later chapter starts at its "Next song!" card
    t = 0.0; lines = []
    for k, (path, title) in enumerate(songs):
        if k == 0:
            lines.append(f'0:00 {title}'); t = duration(parts[0]) + duration(path)
        else:
            lines.append(f'{int(t // 60)}:{int(t % 60):02d} {title}')
            t += duration(parts[2 * k]) + duration(path)
    with open(out + '.chapters.txt', 'w') as fh:
        fh.write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


def thumb(out, comp_title, minutes):
    base = bg().copy()
    paste(base, spr('tavo', True, False, 680, case_open=True, wave=True), 450, 600)
    for nm, x, y, s in [('rosy', 1180, 760, 330), ('rubbo', 1440, 800, 300), ('lino', 1700, 740, 340)]:
        paste(base, spr(nm, False, False, s), x, y)
    d = ImageDraw.Draw(base, 'RGBA')
    for k, ln in enumerate(wrap(comp_title, 16)):
        text(d, 1300, 230 + k * 140, ln, 130, (216, 27, 96), stroke=16)
    d.rounded_rectangle([40, 36, 520, 126], radius=45, fill=(30, 120, 220, 255))
    d.text((280, 81), 'Sing with Tavo', font=font(56), fill='white', anchor='mm')
    d.rounded_rectangle([1560, 40, 1880, 140], radius=50, fill=(216, 27, 96, 255))
    d.text((1720, 90), f'{minutes} min', font=font(64), fill='white', anchor='mm')
    base.convert('RGB').resize((1280, 720), Image.LANCZOS).save(out, quality=92)


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[0] == '--thumb':
        thumb(a[1], a[2], int(a[3]))
    else:
        out, title, rest = a[0], a[1], a[2:]
        songs = [(rest[i], rest[i + 1]) for i in range(0, len(rest), 2)]
        build(out, title, songs)
