import numpy as np, wave, sys
sr=44100; dur=float(sys.argv[1]) if len(sys.argv)>1 else 24; out=sys.argv[2] if len(sys.argv)>2 else 'muzik.wav'
t=np.arange(int(sr*dur))/sr
bpm=100; beat=60/bpm
chords=[[220.0,261.63,329.63],[174.61,220.0,261.63],[261.63,329.63,392.0],[196.0,246.94,293.66]]  # Am F C G
y=np.zeros_like(t)
bar=beat*4
for i,tt in enumerate(t):
    pass
idx=(t//bar).astype(int)%4
for ci,ch in enumerate(chords):
    m=(idx==ci)
    ph=(t%bar)/bar
    env=np.minimum(1,ph*6)*np.minimum(1,(1-ph)*6)
    for f in ch:
        y+=m*env*(np.sin(2*np.pi*f*t)*0.5+np.sin(2*np.pi*f*2*t)*0.15)*0.18
    # bass
    y+=m*env*np.sin(2*np.pi*(ch[0]/2)*t)*0.25
# soft pulse (hi-hat-like noise on 8ths) and kick on beats
rng=np.random.default_rng(1)
b=(t%beat)/beat
kick=np.sin(2*np.pi*(55+90*np.exp(-b*18)*1.0)*(t%beat))*np.exp(-b*7)*0.5
y+=kick
h=(t%(beat/2))/(beat/2)
y+=rng.standard_normal(len(t))*np.exp(-h*30)*0.04
y=y/np.max(np.abs(y))*0.55
f=int(sr*1.0); y[:f]*=np.linspace(0,1,f); y[-f:]*=np.linspace(1,0,f)
w=wave.open(out,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((y*32767).astype(np.int16).tobytes()); w.close()
