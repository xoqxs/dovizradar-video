import json,subprocess,sys
out=sys.argv[1]; tail=1.2
sc=json.load(open('scenes_d.json')); sc[-1]['d']=round(sc[-1]['d']+tail,2); L=open('l.txt','w'); A=open('a.txt','w')
run=lambda a:subprocess.run(a,check=True)
for i,x in enumerate(sc):
    d=x['d']
    run(['ffmpeg','-y','-loglevel','error','-loop','1','-i',f's{i}.png','-t',str(d),'-vf',f"scale=1188:2112,zoompan=z='min(zoom+0.0005,1.05)':d={int(d*25)+5}:s=1080x1920:fps=25,fade=t=in:st=0:d=0.12,fade=t=out:st={d-0.12}:d=0.12,format=yuv420p",'-c:v','libx264','-preset','veryfast','-crf','20',f'c{i}.mp4'])
    run(['ffmpeg','-y','-loglevel','error','-i',f'n{i}.wav','-af','adelay=60|60,apad','-t',str(d),'-ar','44100','-ac','1',f'p{i}.wav'])
    L.write(f"file 'c{i}.mp4'\n"); A.write(f"file 'p{i}.wav'\n")
L.close(); A.close()
run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','l.txt','-c','copy','v.mp4'])
run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i','a.txt','-c','copy','voice.wav'])
D=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','v.mp4'],capture_output=True,text=True).stdout.strip()
run(['python3','music.py',D,'m.wav'])
run(['ffmpeg','-y','-loglevel','error','-i','voice.wav','-af','loudnorm=I=-16:TP=-1.5','-ar','44100','-ac','1','voiceN.wav'])
run(['ffmpeg','-y','-loglevel','error','-i','voiceN.wav','-i','m.wav','-filter_complex','[1:a]volume=0.20[m];[0:a][m]amix=inputs=2:duration=longest:normalize=0,apad[a]','-map','[a]','-t',D,'-ar','44100','mix.wav'])
run(['ffmpeg','-y','-loglevel','error','-i','v.mp4','-i','mix.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','160k','-t',D,out])
print(out,D)
