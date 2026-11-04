import numpy as np, subprocess, soundfile as sf, os
from kokoro_onnx import Kokoro
from scipy.signal import resample_poly
from song import *

SR = 44100
k = Kokoro('/home/claude/tts/kokoro-v1.0.onnx', '/home/claude/tts/voices-v1.0.bin')
try:
    import topic as _T
except Exception:
    _T = None
VOICE = getattr(_T, 'VOICE', 'af_heart')
INTRO_LINE = getattr(_T, 'INTRO_LINE', "Hi friends! It's Tavo! Let's sing!")
OUTRO_LINE = getattr(_T, 'OUTRO_LINE', 'Bye bye, friends! See you next time with Tavo!')
total = TOTAL_BEATS * BEAT + 2.5
out = np.zeros(int(total * SR))

def tts(text, speed=1.0):
    s, sr = k.create(text, voice=VOICE, speed=speed, lang='en-us')
    s = resample_poly(s, 147, 80)  # 24k -> 44.1k
    a = np.abs(s); th = a.max() * 0.03
    idx = np.where(a > th)[0]
    s = s[max(0, idx[0] - 200): idx[-1] + 2000]
    return s / (np.abs(s).max() + 1e-9)

def stretch(x, ratio):
    # ratio > 1 -> longer. atempo = 1/ratio (pitch preserved)
    sf.write('/tmp/in.wav', x, SR)
    tempo = 1 / ratio
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', '/tmp/in.wav', '-af', f'atempo={tempo:.4f}', '/tmp/out.wav'], check=True)
    y, _ = sf.read('/tmp/out.wav')
    return y

def place(x, t0, gain=1.0):
    i = int(t0 * SR); j = min(len(out), i + len(x))
    out[i:j] += x[:j - i] * gain

# intro + outro narration
place(tts(INTRO_LINE, 1.0), 4.3 * BEAT)
end = [s for s in SECTIONS if s['kind'] == 'end'][0]
place(tts(OUTRO_LINE, 1.0), end['start'] * BEAT + 0.3)

def chunks(line):
    # list of (text, first_beat, end_beat) grouped by words, split at punctuation / long phrases
    pos = 0; notes = []
    for p, d in line['notes']:
        if p != 'r': notes.append((pos, d))
        pos += d
    words = []; cur = []
    for i, sy in enumerate(line['syl']):
        cur.append(i)
        if sy.endswith('_') or i == len(line['syl']) - 1:
            words.append(cur); cur = []
    groups = []; g = []
    for w in words:
        g.append(w)
        txt = line['syl'][w[-1]].rstrip('_')
        if txt[-1] in ',?!':
            groups.append(g); g = []
    if g: groups.append(g)
    res = []
    for g in groups:
        nsyl = sum(len(w) for w in g)
        parts = [g]
        if nsyl > 5 and len(g) > 2:
            cut = len(g) // 2
            parts = [g[:cut], g[cut:]]
        for pt in parts:
            idx = [i for w in pt for i in w]
            text = ''.join(line['syl'][i].replace('_', ' ') for i in idx).strip()
            b0 = notes[idx[0]][0]; b1 = notes[idx[-1]][0] + notes[idx[-1]][1] * 0.8
            res.append((text, b0, b1))
    return res

cache = {}
for s in SECTIONS:
    for li, line in enumerate(s['lines']):
        b = s['start'] + 8 * li
        for text, b0, b1 in chunks(line):
            target = (b1 - b0) * BEAT
            key = (text, round(target, 2))
            if key not in cache:
                x0 = tts(text, 0.9)
                need = target / (len(x0) / SR)
                sp = float(np.clip(0.9 / need, 0.62, 1.1))
                cache[key] = x0 if abs(sp - 0.9) < 0.05 else tts(text, sp)
            x = cache[key]
            ratio = float(np.clip(target / (len(x) / SR), 0.85, 1.2))
            if abs(ratio - 1) > 0.03: x = stretch(x, ratio)
            place(x, (b + b0) * BEAT - 0.04)
            print(f'{text:28s} target {target:.2f}  raw {len(cache[key])/SR:.2f}  r {ratio:.2f}')

out /= np.abs(out).max() + 1e-9
sf.write('voice.wav', out * 0.95, SR)
# mouth envelope at 30 fps
hop = SR // 30
n = len(out) // hop
rms = np.array([np.sqrt(np.mean(out[i * hop:(i + 1) * hop] ** 2)) for i in range(n)])
np.save('voice_env.npy', rms / rms.max())
