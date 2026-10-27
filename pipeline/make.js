// Sahne PNG'leri. Tema her videoda değişir (THEME=0..5 ile sabitlenebilir).
// Sahne alanları: k,t,s,c,n + isteğe bağlı photo (üst fotoğraf), photo2 (küçük ikinci fotoğraf, çerçeveli),
// layout:"full" (fotoğraf tam ekran, metin altta), person{img,name}, flag "us"|"tr", img (çizim).
const {chromium}=require('playwright');const fs=require('fs');const crypto=require('crypto');const sc=require('./scenes_d.json');const A=require('./art.js');
const du=f=>'data:image/jpeg;base64,'+fs.readFileSync(f).toString('base64');
const lg='data:image/png;base64,'+fs.readFileSync('logo.png').toString('base64');
const TH=[{bg:'linear-gradient(160deg,#071a36,#0a2347 55%,#0d3b3a)',base:'#0a2347',ac:'#4ade80'},
{bg:'linear-gradient(170deg,#1a0f2e,#24164a 55%,#0f2b45)',base:'#24164a',ac:'#facc15'},
{bg:'linear-gradient(150deg,#06231f,#0b3a32 55%,#14324a)',base:'#0b3a32',ac:'#38bdf8'},
{bg:'linear-gradient(165deg,#2a0f14,#3b1420 50%,#1c1f3a)',base:'#3b1420',ac:'#fbbf24'},
{bg:'linear-gradient(155deg,#0c1424,#16243f 55%,#1f2f2a)',base:'#16243f',ac:'#f472b6'},
{bg:'linear-gradient(175deg,#111827,#1f2937 55%,#0e3a4a)',base:'#1f2937',ac:'#a3e635'}];
const seed=process.env.VSEED||new Date().toISOString().slice(0,16);
const T=TH[process.env.THEME!==undefined?+process.env.THEME:parseInt(crypto.createHash('md5').update(seed).digest('hex').slice(0,4),16)%TH.length];
const hx=h=>{const n=parseInt(h.slice(1),16);return `${n>>16&255},${n>>8&255},${n&255}`};
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(let i=0;i<sc.length;i++){const x=sc[i];let top='';let pad='90px';let jc='center';
 if(x.photo&&x.layout==='full'){top=`<div style="position:absolute;inset:0;background:url(${du(x.photo)}) center/cover"></div><div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.45) 0%,rgba(0,0,0,.05) 25%,rgba(${hx(T.base)},.55) 55%,${T.base} 82%)"></div>`;pad='0 90px 230px';jc='flex-end';}
 else if(x.photo){top=`<div style="position:absolute;top:0;left:0;right:0;height:900px;background:url(${du(x.photo)}) center/cover"></div><div style="position:absolute;top:0;left:0;right:0;height:900px;background:linear-gradient(180deg,rgba(0,0,0,.5) 0%,rgba(0,0,0,0) 30%,rgba(${hx(T.base)},.2) 60%,${T.base} 100%)"></div>`;pad='980px 90px 0';}
 else if(x.img){top=`<div style="position:absolute;top:330px;left:90px;right:90px">${A.art(x.img)}</div>`;pad='560px 90px 0';}
 if(x.photo2) top+=`<div style="position:absolute;top:${x.layout==='full'?300:560}px;right:80px;width:330px;height:330px;border-radius:28px;background:url(${du(x.photo2)}) center/cover;border:6px solid ${T.ac};box-shadow:0 14px 40px rgba(0,0,0,.55);transform:rotate(${i%2?3:-3}deg)"></div>`;
 if(x.person) top+=`<div style="position:absolute;top:640px;left:90px;display:flex;align-items:center;gap:28px"><img src="${du(x.person.img)}" style="width:250px;height:250px;border-radius:50%;object-fit:cover;border:6px solid ${T.ac};box-shadow:0 10px 40px rgba(0,0,0,.5)"><div style="font-size:40px;font-weight:700;text-shadow:0 2px 12px rgba(0,0,0,.6)">${x.person.name}</div></div>`;
 if(x.flag) top+=`<div style="position:absolute;top:250px;right:90px;transform:scale(.55);transform-origin:top right">${A.art(x.flag)}</div>`;
await p.setContent(`<body style="margin:0;width:1080px;height:1920px;background:${T.bg};font-family:Inter,sans-serif;color:#fff;display:flex;flex-direction:column;justify-content:${jc};padding:${pad};box-sizing:border-box;position:relative">${top}<div style="position:absolute;top:100px;left:90px;display:flex;align-items:center;gap:24px"><img src="${lg}" style="width:96px;height:96px;border-radius:50%"><span style="font-size:46px;font-weight:700;text-shadow:0 2px 10px rgba(0,0,0,.6)">Döviz Radar</span></div><div style="position:relative;display:inline-block;align-self:flex-start;background:${x.c};color:#08233a;font-weight:800;font-size:40px;padding:14px 32px;border-radius:999px;margin-bottom:44px">${x.k}</div><div style="position:relative;font-size:100px;line-height:1.12;font-weight:500;text-shadow:0 3px 14px rgba(0,0,0,.45)">${x.t.replace(/<b>/g,`<b style="font-weight:900;color:${T.ac}">`)}</div><div style="position:relative;font-size:44px;margin-top:40px;opacity:.9;line-height:1.35;text-shadow:0 2px 10px rgba(0,0,0,.5)">${x.s}</div><div style="position:absolute;bottom:140px;left:90px;right:90px;height:8px;background:rgba(255,255,255,.15);border-radius:4px"><div style="width:${Math.round((i+1)/sc.length*100)}%;height:100%;background:${T.ac};border-radius:4px"></div></div></body>`);
await p.screenshot({path:`s${i}.png`});}await b.close();console.log('tema',TH.indexOf(T));})();
