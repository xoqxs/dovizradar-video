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
if __name__=="__main__":
    if sys.argv[1]=="s": print("\n".join(search(sys.argv[2])))
    else:
        i=info(sys.argv[2]); print(json.dumps(i,ensure_ascii=False))
        if len(sys.argv)>3: subprocess.run(["curl","-s","-m","40","-A",UA,"-o",sys.argv[3],i['url']])
