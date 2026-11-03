"""Mix music.wav + voice.wav -> final_audio.wav (voice on top, music ducked)."""
import numpy as np, soundfile as sf
from scipy.signal import fftconvolve
m, sr = sf.read('music.wav'); v, _ = sf.read('voice.wav')
n = min(len(m), len(v)); m = m[:n]; v = v[:n]
rng = np.random.default_rng(1); t = np.arange(int(0.6 * sr)) / sr
ir = rng.normal(0, 1, len(t)) * np.exp(-t * 9); ir /= np.abs(ir).sum() ** 0.5 * 8
vw = v + fftconvolve(v, ir)[:n] * 0.25
env = np.convolve(np.abs(v), np.ones(2205) / 2205, 'same'); duck = 1 - 0.35 * np.clip(env / 0.08, 0, 1)
mix = m * 0.7 * duck[:, None] + vw[:, None] * 1.0
mix /= np.abs(mix).max() / 0.89
sf.write('final_audio.wav', mix, sr)
