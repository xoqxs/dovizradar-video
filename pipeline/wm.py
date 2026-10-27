import json,sys,urllib.parse,subprocess
UA="DovizRadarBot/1.0 (https://www.dovizradar.com; akadirpars@gmail.com)"
def api(params):
    u="https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode({**params,"format":"json"})
    import time
    for k in range(8):
        out=subprocess.run(["curl","-s","-m","25","-A",UA,u],capture_output=True,text=True).stdout
        try: return json.loads(out)
        except Exception: time.sleep(10+k*5)
    raise SystemExit("wikimedia rate limit")
def search(q,n=6):
    return [x['title'] for x in api({"action":"query","list":"search","srnamespace":6,"srlimit":n,"srsearch":q})['query']['search']]
def info(title,width=1080):
    p=api({"action":"query","titles":title,"prop":"imageinfo","iiprop":"url|extmetadata","iiurlwidth":width})['query']['pages']
    ii=list(p.values())[0]['imageinfo'][0]; m=ii['extmetadata']
    g=lambda k:(m.get(k,{}).get('value','') or '')
    import re; strip=lambda s:re.sub('<[^>]+>','',s).strip()
    u=ii.get("thumburl") or ii["url"]
    if "thumb.wikimedia" in u: u=ii["url"]
    return {"url":u,"license":strip(g('LicenseShortName')),"artist":strip(g('Artist'))[:80],"attr":g('AttributionRequired')}
import os,datetime
LOG=os.path.join(os.path.dirname(os.path.abspath(__file__)),'kullanilan-gorseller.txt')
def used():
    # depo kopyasındaki kayıt (görevler commit eder); son 120 kayıt "yakın zamanda kullanıldı" sayılır
    for f in [LOG,'/home/claude/dovizradar-video/pipeline/kullanilan-gorseller.txt']:
        if os.path.exists(f): return [l.split('\t',1)[1].strip() for l in open(f,encoding='utf-8').read().splitlines() if '\t' in l][-120:]
    return []
def mark(title):
    for f in ['/home/claude/dovizradar-video/pipeline/kullanilan-gorseller.txt',LOG]:
        if os.path.exists(os.path.dirname(f)):
            open(f,'a',encoding='utf-8').write(datetime.date.today().isoformat()+'\t'+title+'\n'); return
if __name__=="__main__":
    if sys.argv[1]=="s":
        u=set(used()); r=search(sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 10)
        print("\n".join(("[KULLANILDI] " if t in u else "")+t for t in r))
    else:
        if sys.argv[2] in used() and os.environ.get('TEKRAR')!='1':
            raise SystemExit("TEKRAR: bu gorsel son videolarda kullanildi, baska gorsel sec ("+sys.argv[2]+")")
        i=info(sys.argv[2]); print(json.dumps(i,ensure_ascii=False))
        if len(sys.argv)>3:
            subprocess.run(["curl","-sL","-m","60","-A",UA,"-o",sys.argv[3],"https://commons.wikimedia.org/w/thumb.php?"+urllib.parse.urlencode({"w":1400,"f":sys.argv[2].split(":",1)[1]})]); mark(sys.argv[2])  # upload.wikimedia.org 429 veriyor; thumb.php calisiyor (27.10.2026)
