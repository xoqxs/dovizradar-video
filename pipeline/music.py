import numpy as np, wave, sys, os, datetime, hashlib
# Kullanım: python3 music.py SÜRE ÇIKTI.wav   (VSEED ortam değişkeni yoksa tarih+saat tohumu; her videoda farklı müzik)
sr=44100; dur=float(sys.argv[1]) if len(sys.argv)>1 else 24; out=sys.argv[2] if len(sys.argv)>2 else 'muzik.wav'
seed=os.environ.get('VSEED') or datetime.datetime.now().strftime('%Y%m%d%H%M')
rng=np.random.default_rng(int(hashlib.md5(seed.encode()).hexdigest()[:8],16))
t=np.arange(int(sr*dur))/sr
bpm=float(rng.integers(86,116)); beat=60/bpm; bar=beat*4
semi=2**(int(rng.integers(-4,5))/12)
N={'A':220.0,'B':246.94,'C':261.63,'D':293.66,'E':329.63,'F':174.61,'G':196.0}
def tri(r,m3,f5): return [r,r*m3,r*f5]
mi,ma,P5=2**(3/12),2**(4/12),2**(7/12)
progs=[[('A',mi),('F',ma),('C',ma),('G',ma)],[('C',ma),('G',ma),('A',mi),('F',ma)],[('D',mi),('B',mi),('G',ma),('A',ma)],[('F',ma),('G',ma),('E',mi),('A',mi)],[('A',mi),('D',mi),('G',ma),('C',ma)]]
prog=progs[int(rng.integers(len(progs)))]
chords=[[f*semi for f in tri(N[n],q,P5)] for n,q in prog]
h2=float(rng.uniform(.08,.25)); h3=float(rng.uniform(0,.1))
y=np.zeros_like(t); idx=(t//bar).astype(int)%4; ph=(t%bar)/bar
env=np.minimum(1,ph*6)*np.minimum(1,(1-ph)*6)
for ci,ch in enumerate(chords):
    m=(idx==ci)
    for f in ch: y+=m*env*(np.sin(2*np.pi*f*t)*0.5+np.sin(2*np.pi*f*2*t)*h2+np.sin(2*np.pi*f*3*t)*h3)*0.18
    y+=m*env*np.sin(2*np.pi*(ch[0]/2)*t)*0.25
    if rng.random()<0.9:  # arpej
        step=beat/2; k=((t%bar)//step).astype(int)%3; ae=np.exp(-((t%step)/step)*6)
        for j in range(3): y+=m*(k==j)*ae*np.sin(2*np.pi*ch[j]*2*t)*0.07
b=(t%beat)/beat
y+=np.sin(2*np.pi*(55+90*np.exp(-b*18))*(t%beat))*np.exp(-b*7)*float(rng.uniform(.35,.55))
hh=beat/2 if rng.random()<.6 else beat/4; h=(t%hh)/hh
y+=rng.standard_normal(len(t))*np.exp(-h*30)*0.04
y=y/np.max(np.abs(y))*0.55
f=int(sr); y[:f]*=np.linspace(0,1,f); y[-f:]*=np.linspace(1,0,f)
w=wave.open(out,'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((y*32767).astype(np.int16).tobytes()); w.close()
print('muzik',seed,int(bpm),prog)
