/* Param ne olurdu – sayfaya gömülecek aylık veriyi üretir (tarayıcıda çalışır).
   fx: ayın ilk iş günü ECB referans kuru, TL cinsinden [USD, EUR, GBP] (1999–2004 eski TL ÷ 1.000.000)
   g : ons altın (USD) – freegoldapi (Dünya Bankası aylık ortalaması), bittiği yerden sonra Binance PAXG aylık açılış
   b : Bitcoin (USD) – Binance BTCUSDT aylık açılış (Eylül 2017'den)
   Kullanım: const V = await pnoGomulu(); */
async function pnoGomulu(){
  const RAW="https://raw.githubusercontent.com/xoqxs/dovizradar-video/main/veri/kur/";
  const n=new Date(),Y=n.getUTCFullYear(),M=n.getUTCMonth();const pm=new Date(Date.UTC(Y,M-1,1)).toISOString().slice(0,7);
  const fx={};
  for(let y=1999;y<=Y;y++){const j=await fetch(RAW+y+".json?x="+Date.now()).then(r=>r.json());const c=j.c,iU=c.indexOf("USD"),iT=c.indexOf("TRY"),iG=c.indexOf("GBP");
    for(const d of Object.keys(j.d).sort()){const m=d.slice(0,7);if(m>pm||fx[m])continue;const v=j.d[d];if(v[iT]==null||v[iU]==null||v[iG]==null)continue;
      fx[m]=[+(v[iT]/v[iU]).toPrecision(6),+(+v[iT]).toPrecision(6),+(v[iT]/v[iG]).toPrecision(6)]}}
  const ms=Object.keys(fx).sort();
  const gl=await fetch("https://freegoldapi.com/data/latest.json").then(r=>r.json());const lastD=gl[gl.length-1].date;
  const kl=async(sym,from)=>{const t=Date.parse(from+"-01T00:00:00Z");const a=await fetch("https://data-api.binance.vision/api/v3/klines?symbol="+sym+"&interval=1M&startTime="+t+"&limit=500").then(r=>r.json());const o={};a.forEach(x=>{o[new Date(x[0]).toISOString().slice(0,7)]=+(+x[1]).toFixed(2)});return o};
  const g={};for(const m of ms){const t=m+"-01";if(t>lastD)continue;let b=null;for(const x of gl){if(x.date<=t)b=x;else break}if(b&&Date.parse(t)-Date.parse(b.date)<4e9)g[m]=+(+b.price).toFixed(2)}
  const firstMissing=ms.find(m=>!(m in g));if(firstMissing){const P=await kl("PAXGUSDT",firstMissing);for(const m of ms)if(!(m in g)&&m in P)g[m]=P[m]}
  const B=await kl("BTCUSDT","2017-09"),b={};for(const m of ms)if(m in B)b[m]=B[m];
  return {v:1,t:n.toISOString().slice(0,10),son:pm,fx:fx,g:g,b:b};
}
