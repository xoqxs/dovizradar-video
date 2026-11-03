import numpy as np
from scipy.signal import lfilter, fftconvolve, butter
from scipy.io import wavfile
from song import *

SR = 44100
rng = np.random.default_rng(7)
total = TOTAL_BEATS * BEAT + 3.0
mix = {k: np.zeros(int(total * SR)) for k in ['lead', 'glock', 'uke', 'bass', 'drums', 'fx']}
f = lambda m: 440 * 2 ** ((m - 69) / 12)
CH = {'C': [60, 64, 67, 72], 'F': [60, 65, 69, 72], 'G': [62, 67, 71, 74], 'Am': [60, 64, 69, 72]}
ROOT = {'C': 36, 'F': 41, 'G': 43, 'Am': 45}

def put(buf, start_s, sig):
    i = int(start_s * SR)
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[:j - i]

def env(n, a, d, s, r, sus_len):
    t = np.arange(n) / SR
    e = np.where(t < a, t / a, s + (1 - s) * np.exp(-(t - a) / d))
    rel = np.clip((t - sus_len) / r, 0, 1)
    return e * (1 - rel)

# lead: warm "toy flute" (triangle + sine) with vibrato
def lead(midi, dur):
    n = int((dur + 0.25) * SR)
    t = np.arange(n) / SR
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.5 * t) * np.clip(t / 0.25, 0, 1)
    ph = 2 * np.pi * np.cumsum(f(midi) * vib) / SR
    tri = 2 / np.pi * np.arcsin(np.sin(ph))
    sig = 0.6 * tri + 0.5 * np.sin(ph) + 0.12 * np.sin(2 * ph)
    return sig * env(n, 0.02, 0.4, 0.75, 0.15, dur * 0.92)

def glock(midi):
    n = int(1.2 * SR); t = np.arange(n) / SR
    fr = f(midi + 12)
    return (np.sin(2*np.pi*fr*t) * np.exp(-t*4) + 0.3*np.sin(2*np.pi*fr*2.76*t)*np.exp(-t*12)) * np.minimum(t/0.002, 1)

pluck_cache = {}
def pluck(midi):
    if midi not in pluck_cache:
        p = int(round(SR / f(midi)))
        n = int(1.4 * SR)
        x = np.zeros(n); x[:p] = rng.uniform(-1, 1, p)
        x[:p] = lfilter([0.5, 0.5], [1], x[:p])
        a = np.zeros(p + 2); a[0] = 1; a[p] = -0.497; a[p + 1] = -0.497
        y = lfilter([1], a, x)
        pluck_cache[midi] = y / np.abs(y).max()
    return pluck_cache[midi]

def bass(midi, dur):
    n = int((dur + 0.05) * SR); t = np.arange(n) / SR
    s = np.sin(2*np.pi*f(midi)*t) + 0.25*np.sin(4*np.pi*f(midi)*t)
    return np.tanh(1.5 * s) * env(n, 0.005, 0.3, 0.6, 0.05, dur * 0.85)

def kick():
    n = int(0.35 * SR); t = np.arange(n) / SR
    fr = 50 + 90 * np.exp(-t * 30)
    return np.sin(2*np.pi*np.cumsum(fr)/SR) * np.exp(-t * 9)
def clap():
    n = int(0.25 * SR); t = np.arange(n) / SR
    b, a = butter(2, [900/(SR/2), 4000/(SR/2)], 'band')
    nz = lfilter(b, a, rng.uniform(-1, 1, n))
    e = np.exp(-t*25) + 0.6*np.exp(-np.maximum(t-0.012, 0)*40)*(t > 0.012)
    return nz * e * 1.8
def shaker():
    n = int(0.08 * SR); t = np.arange(n) / SR
    b, a = butter(2, 6000/(SR/2), 'high')
    return lfilter(b, a, rng.uniform(-1, 1, n)) * np.exp(-t*60) * np.minimum(t/0.01, 1)
def pop():
    n = int(0.18 * SR); t = np.arange(n) / SR
    fr = 300 + 900 * (1 - np.exp(-t * 40))
    return np.sin(2*np.pi*np.cumsum(fr)/SR) * np.exp(-t*25)
K, C, S, P = kick(), clap(), shaker(), pop()

notes, chords = events()
for b, d, m, sec, li, si in notes:
    s0 = b * BEAT
    put(mix['lead'], s0, lead(m, d * BEAT))
    if sec.startswith('ch') or sec == 'outro':
        put(mix['glock'], s0, glock(m) * 0.5)

for b, d, c in chords:
    s0 = b * BEAT
    # strum pattern within 2 beats: down on 0, up on 1, down on 1.5 (eighths)
    for off, vel, up in [(0, 1.0, False), (1, 0.6, True), (1.5, 0.75, False)]:
        tones = CH[c][::-1] if up else CH[c]
        for k, m in enumerate(tones):
            put(mix['uke'], (b + off) * BEAT + k * 0.012, pluck(m) * vel * 0.6)
    r = ROOT[c]
    put(mix['bass'], s0, bass(r, 0.9 * BEAT))
    put(mix['bass'], s0 + BEAT, bass(r + 7, 0.9 * BEAT) * 0.8)

last = TOTAL_BEATS - 8
for i in range(int(TOTAL_BEATS * 2)):
    b = i / 2
    if b >= last + 1:  # ending: single hit
        continue
    if b % 1 == 0:
        if b % 2 == 0: put(mix['drums'], b * BEAT, K)
        else: put(mix['drums'], b * BEAT, C * (0.6 if b < 16 else 1))
    put(mix['drums'], b * BEAT, S * (0.35 if b % 1 else 0.2))
# final hit
put(mix['drums'], last * BEAT, K * 1.2)
for m in CH['C']:
    put(mix['uke'], last * BEAT, pluck(m) * 0.9)
put(mix['glock'], last * BEAT, glock(84) * 0.8)
put(mix['bass'], last * BEAT, bass(36, 2.0))

# pop sound when a fruit appears (start of each verse) + glock sparkle in intro
for s in SECTIONS:
    if s['kind'] == 'verse':
        put(mix['fx'], s['start'] * BEAT - 0.05, P * 0.8)
for i, m in enumerate([72, 76, 79, 84, 79, 76, 72, 79]):
    put(mix['glock'], (2 * i) * BEAT, glock(m) * 0.35)

def norm(x): return x / (np.abs(x).max() + 1e-9)
ir_t = np.arange(int(1.6 * SR)) / SR
ir = rng.normal(0, 1, len(ir_t)) * np.exp(-ir_t * 3.5); ir[0] = 0
def verb(x, wet): return x + wet * norm(fftconvolve(x, ir)[:len(x)]) * np.abs(x).max()

out = (0.22 * verb(norm(mix['lead']), 0.25) + 0.13 * verb(norm(mix['glock']), 0.3)
       + 0.42 * verb(norm(mix['uke']), 0.2) + 0.5 * norm(mix['bass'])
       + 0.45 * norm(mix['drums']) + 0.4 * norm(mix['fx']))
# fade tail
end_i = int((TOTAL_BEATS * BEAT + 2.5) * SR)
out = out[:end_i]
out[-int(1.0*SR):] *= np.linspace(1, 0, int(1.0*SR))
out = out / np.abs(out).max() * 0.89
st = np.stack([out, np.roll(out, 0)], 1)
wavfile.write('music.wav', SR, (st * 32767).astype(np.int16))
print('duration', len(out) / SR)
