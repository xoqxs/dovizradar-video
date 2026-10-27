import json,subprocess,sys
out=sys.argv[1]; tail=1.2
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
    fr=int(d*25)+5; mv=MOVES[(i+OFF)%len(MOVES)].format(fr=fr)
    run(['ffmpeg','-y','-loglevel','error','-loop','1','-i',f's{i}.png','-t',str(d),'-vf',f"scale=1188:2112,{mv}:d={fr}:s=1080x1920:fps=25,fade=t=in:st=0:d=0.12,fade=t=out:st={d-0.12}:d=0.12,format=yuv420p",'-c:v','libx264','-preset','veryfast','-crf','20',f'c{i}.mp4'])
    run(['ffmpeg','-y','-loglevel','error','-i',f'n{i}.wav','-af','adelay=60|60,apad','-t',str(d),'-ar','44100','-ac','1',f'p{i}.wav'])
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
