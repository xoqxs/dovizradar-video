import json,subprocess,sys,os,html
V=sys.argv[1] if len(sys.argv)>1 else 'tr-TR-AhmetNeural'; key,reg=[l.strip() for l in open('/home/claude/dovizradar-ayarlar/azure.txt').read().splitlines()[:2]]
sc=json.load(open('scenes.json'))
for i,x in enumerate(sc):
    ssml=f"<speak version='1.0' xml:lang='tr-TR'><voice name='{V}'><prosody rate='+22%'>{html.escape(x['n'])}</prosody></voice></speak>"
    r=subprocess.run(['curl','-s','-m','30','-o',f'n{i}.mp3','-w','%{http_code}','-X','POST',f'https://{reg}.tts.speech.microsoft.com/cognitiveservices/v1','-H',f'Ocp-Apim-Subscription-Key: {key}','-H','Content-Type: application/ssml+xml','-H','X-Microsoft-OutputFormat: audio-24khz-96kbitrate-mono-mp3','-H','User-Agent: dovizradar','--data-binary',ssml],capture_output=True,text=True)
    assert r.stdout=='200', r.stdout
    # baştaki ve sondaki sessizliği kırp: sahneler arası duraksama olmasın
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'n{i}.mp3','-af','silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse','-ar','44100','-ac','1',f'n{i}.wav'],check=True)
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'n{i}.wav'],capture_output=True,text=True).stdout)
    x['d']=round(d+0.08,2)
json.dump(sc,open('scenes_d.json','w'),ensure_ascii=False); print([x['d'] for x in sc], round(sum(x['d'] for x in sc),1))
