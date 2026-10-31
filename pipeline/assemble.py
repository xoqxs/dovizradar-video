import json,subprocess,sys
out=sys.argv[1]; tail=1.0
sc=json.load(open('scenes_d.json')); sc[-1]['d']=round(sc[-1]['d']+tail,2); L=open('l.txt','w'); A=open('a.txt','w')
run=lambda a:subprocess.run(a,check=True)
import os,datetime,hashlib
# Her sahnede farklı kamera hareketi; sıra her videoda farklı başlar
MOVES=["zoompan=z='min(zoom+0.0005,1.05)'",
 "zoompan=z='if(eq(on,0),1.06,max(zoom-0.0005,1.0))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
 "zoompan=z='1.05':x='(iw-iw/zoom)*on/{fr}':y='ih/2-(ih/zoom/2)'",
 "zoompan=z='1.05':x='(iw-iw/zoom)*(1-on/{fr})':y='ih/2-(ih/zoom/2)'",
 "zoompan=z='min(zoom+0.0004,1.05)':x='iw/2-(iw/zoom/2)':y='0'"]
OFF=int(hashlib.md5((os.environ.get('VSEED') or datetime.datetime.now().strftime('%Y%m%d%H%M')).encode()).hexdigest()[:4],16)
for i,x in enumerate(sc):
    d=x['d']
    # Sahnede birden fazla görsel (shots) varsa süre eşit bölünür: görüntü 2-3 sn'de bir değişir
    shots=[f's{i}.png']+sorted(f for f in os.listdir('.') if f.startswith(f's{i}_') and f.endswith('.png'))
    sd=round(d/len(shots),3); parts=[]
    for j,img in enumerate(shots):
        dj=sd if j<len(shots)-1 else round(d-sd*(len(shots)-1),3)
        fr=int(dj*25)+5; mv=MOVES[(i*3+j+OFF)%len(MOVES)].format(fr=fr)
        # İlk sahnenin ilk karesi SİYAH OLMAMALI: TikTok/YouTube kapağı ilk kareden alır (Kadir Bey 31 Ekim 2026)
        fi='fade=t=in:st=0:d=0.08,' if (j==0 and i>0) else ''
        fo=f',fade=t=out:st={dj-0.08}:d=0.08' if j==len(shots)-1 else ''
        run(['ffmpeg','-y','-loglevel','error','-loop','1','-i',img,'-t',str(dj),'-vf',f"scale=1188:2112,{mv}:d={fr}:s=1080x1920:fps=25,{fi}format=yuv420p{fo}",'-c:v','libx264','-preset','veryfast','-crf','20',f'c{i}_{j}.mp4'])
        parts.append(f'c{i}_{j}.mp4')
    if len(parts)==1: os.replace(parts[0],f'c{i}.mp4')
    else:
        open(f'cl{i}.txt','w').write(''.join(f"file '{q}'\n" for q in parts))
        run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',f'cl{i}.txt','-c','copy',f'c{i}.mp4'])
    run(['ffmpeg','-y','-loglevel','error','-i',f'n{i}.wav','-af','apad','-t',str(d),'-ar','44100','-ac','1',f'p{i}.wav'])
    L.write(f"file 'c{i}.mp4'\n"); A.write(f"file 'p{i}.wav'\n")
L.close(); A.close()
run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','l.txt','-c','copy','v.mp4'])
run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','a.txt','-c','copy','voice.wav'])
D=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','v.mp4'],capture_output=True,text=True).stdout.strip()
run(['python3','music.py',D,'m.wav'])
run(['ffmpeg','-y','-loglevel','error','-i','voice.wav','-af','loudnorm=I=-16:TP=-1.5','-ar','44100','-ac','1','voiceN.wav'])
run(['ffmpeg','-y','-loglevel','error','-i','voiceN.wav','-i','m.wav','-filter_complex','[1:a]volume=0.30[m];[0:a][m]amix=inputs=2:duration=longest:normalize=0,apad[a]','-map','[a]','-t',D,'-ar','44100','mix.wav'])
run(['ffmpeg','-y','-loglevel','error','-i','v.mp4','-i','mix.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','160k','-t',D,out])
print(out,D)
