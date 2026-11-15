"""Tavo's voice (v3): spoken intro/outro + SUNG lyrics.

Every word is spoken by Kokoro (voice af_heart), analysed with WORLD (pyworld) and re-synthesised so that
  * each syllable sits exactly on its melody note (time), and
  * its pitch IS the melody note (one octave down = comfortable singing range) with a gentle vibrato.
Only voiced frames (vowels) are stretched, so consonants stay crisp.
Writes voice.wav (44.1 kHz) and voice_env.npy (30 fps mouth envelope).
"""
import numpy as np, soundfile as sf, os
import pyworld as pw
from kokoro_onnx import Kokoro
from scipy.signal import resample_poly
from song import *

SR = 44100
FP = 5.0                       # WORLD frame period (ms)
k = Kokoro('/home/claude/tts/kokoro-v1.0.onnx', '/home/claude/tts/voices-v1.0.bin')
try:
    import topic as _T
except Exception:
    _T = None
VOICE = getattr(_T, 'VOICE', 'af_heart')
INTRO_LINE = getattr(_T, 'INTRO_LINE', "Hi friends! It's Tavo! Let's sing!")
OUTRO_LINE = getattr(_T, 'OUTRO_LINE', 'Bye bye, friends! See you next time with Tavo!')
SING_SHIFT = getattr(_T, 'SING_SHIFT', -12)      # semitones relative to the melody
total = TOTAL_BEATS * BEAT + 2.5
out = np.zeros(int(total * SR))


def tts(text, speed=1.0):
    s, sr = k.create(text, voice=VOICE, speed=speed, lang='en-us')
    s = resample_poly(s, 147, 80)  # 24k -> 44.1k
    a = np.abs(s); th = a.max() * 0.03
    idx = np.where(a > th)[0]
    s = s[max(0, idx[0] - 200): idx[-1] + 1500]
    return s / (np.abs(s).max() + 1e-9)


def place(x, t0, gain=1.0):
    i = max(0, int(t0 * SR)); j = min(len(out), i + len(x))
    out[i:j] += x[:j - i] * gain


hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
_an = {}


def analyse(word):
    if word not in _an:
        x = tts(word, 0.95).astype(np.float64)
        f0, t = pw.harvest(x, SR, f0_floor=90, f0_ceil=600, frame_period=FP)
        sp = pw.cheaptrick(x, f0, t, SR)
        ap = pw.d4c(x, f0, t, SR)
        _an[word] = (f0, sp, ap)
    return _an[word]


def sing_word(word, notes):
    """notes: list of (midi, dur_sec) for this word's syllables -> audio."""
    f0, sp, ap = analyse(word)
    n = len(f0)
    voiced = f0 > 0
    if voiced.sum() < 3:
        voiced[:] = True
    vidx = np.where(voiced)[0]
    # split voiced frames into one group per syllable (by time)
    ns = len(notes)
    bounds = [vidx[0]] + [vidx[int(len(vidx) * q / ns)] for q in range(1, ns)] + [n]
    segs_sp, segs_ap, segs_f0 = [], [], []
    lead = bounds[0]                      # unvoiced onset (consonant) kept as is, sung on the first note
    for si, (m, dur) in enumerate(notes):
        a = 0 if si == 0 else bounds[si]
        b = bounds[si + 1]
        fr = np.arange(a, b)
        want = max(len(fr), int(dur * 1000 / FP * 0.92))
        # keep unvoiced frames, stretch voiced ones
        v = voiced[fr]
        nv = max(1, v.sum()); extra = want - len(fr)
        rep = np.ones(len(fr))
        if extra > 0:
            rep[v] += extra / nv
        cum = np.cumsum(rep); pos = np.searchsorted(cum, np.arange(want) + 0.5)
        pos = np.clip(pos, 0, len(fr) - 1)
        src = fr[pos]
        segs_sp.append(sp[src]); segs_ap.append(ap[src])
        tgt = np.full(want, hz(m + SING_SHIFT))
        tt = np.arange(want) * FP / 1000
        vib = np.where(tt > 0.22, 0.25 * np.sin(2 * np.pi * 5.5 * tt) * np.clip((tt - 0.22) / 0.2, 0, 1), 0)
        tgt = tgt * 2 ** (vib / 12)
        segs_f0.append(np.where(voiced[src], tgt, 0.0))
    F0 = np.concatenate(segs_f0)
    # 25 ms portamento between notes
    sm = np.convolve(np.where(F0 > 0, np.log(np.maximum(F0, 1)), 0), np.ones(5) / 5, 'same')
    F0 = np.where(F0 > 0, np.exp(np.where(sm > 0, sm, np.log(np.maximum(F0, 1)))), 0)
    y = pw.synthesize(np.ascontiguousarray(F0), np.ascontiguousarray(np.concatenate(segs_sp)),
                      np.ascontiguousarray(np.concatenate(segs_ap)), SR, FP)
    fade = min(len(y), int(0.012 * SR))
    y[-fade:] *= np.linspace(1, 0, fade)
    return y / (np.abs(y).max() + 1e-9), lead * FP / 1000


# spoken intro + outro (natural speech)
place(tts(INTRO_LINE, 1.0), 4.3 * BEAT)
end = [s for s in SECTIONS if s['kind'] == 'end'][0]
place(tts(OUTRO_LINE, 1.0), end['start'] * BEAT + 0.3)

# sung lyrics, word by word
for s in SECTIONS:
    for li, line in enumerate(s['lines']):
        b = s['start'] + 8 * li
        pos = 0.0; notes = []
        for p, d in line['notes']:
            if p != 'r':
                notes.append((b + pos, d, N[p]))
            pos += d
        words, cur = [], []
        for i, sy in enumerate(line['syl']):
            cur.append(i)
            if sy.endswith('_') or i == len(line['syl']) - 1:
                words.append(cur); cur = []
        for w in words:
            text = ''.join(line['syl'][i].replace('_', '') for i in w)
            clean = ''.join(ch for ch in text if ch.isalnum() or ch in "'-").strip("-'") or text
            nn = [(notes[i][2], notes[i][1] * BEAT) for i in w]
            y, lead = sing_word(clean, nn)
            place(y, notes[w[0]][0] * BEAT - lead)
        print(f"{s['name']:6s} {li}: {''.join(x.replace('_', ' ') for x in line['syl'])}")

out /= np.abs(out).max() + 1e-9
sf.write('voice.wav', out * 0.95, SR)
hop = SR // 30
n = len(out) // hop
rms = np.array([np.sqrt(np.mean(out[i * hop:(i + 1) * hop] ** 2)) for i in range(n)])
np.save('voice_env.npy', rms / rms.max())
