/* DZ-FX: geçmiş kur verisi (4 Kasım 2026). Sıra: 1) kendi arşivimiz (ECB referans kurları, GitHub/jsDelivr), 2) canlı ECB API, 3) frankfurter.dev (yedek). frankfurter adresine yapılan istekleri aynı JSON biçimiyle karşılar. */
(function(){
if(!window.fetch||window.__dzFx)return;window.__dzFx=1;
if(/\/p\/veri-kaynaklari\.html$/.test(location.pathname))return;
var OF=window.fetch.bind(window),Y={},
CDN=["https://cdn.jsdelivr.net/gh/xoqxs/dovizradar-video@main/veri/kur/","https://raw.githubusercontent.com/xoqxs/dovizradar-video/main/veri/kur/"];
function tmo(p,ms){return Promise.race([p,new Promise(function(a,b){setTimeout(function(){b("zaman")},ms)})])}
function gj(u,ms){return tmo(OF(u),ms).then(function(r){if(!r.ok)throw r.status;return r.json()})}
function yil(y){if(!Y[y]){Y[y]=gj(CDN[0]+y+".json",7000).catch(function(){return gj(CDN[1]+y+".json",7000)}).catch(function(e){delete Y[y];throw e})}return Y[y]}
function iso(t){return new Date(t).toISOString().slice(0,10)}
function gun(s,n){return iso(Date.parse(s+"T00:00:00Z")+n*864e5)}
/* kendi arşiv: [s,e] aralığı için {tarih:{KUR:EURoranı}} */
function arsiv(s,e){var a=+s.slice(0,4),b=+e.slice(0,4),ps=[];for(var y=Math.max(a,1999);y<=b;y++)ps.push(yil(y).catch(function(){return null}));
 return Promise.all(ps).then(function(js){var o={},son="",ok=0;js.forEach(function(j){if(!j)return;ok++;var c=j.c;Object.keys(j.d).forEach(function(d){if(d>son)son=d;if(d<s||d>e)return;var v=j.d[d],m={EUR:1};for(var i=0;i<c.length;i++)if(v[i]!=null)m[c[i]]=v[i];o[d]=m})});if(!ok)throw "arsiv";return {o:o,son:son}})}
/* canlı ECB: [s,e] */
function ecb(s,e,syms){var cs=syms.filter(function(x){return x!=="EUR"});var q=cs.length?cs.join("+"):"";
 var u="https://data-api.ecb.europa.eu/service/data/EXR/D."+q+".EUR.SP00.A?startPeriod="+s+"&endPeriod="+e+"&format=csvdata";
 return tmo(OF(u),9000).then(function(r){if(r.status===404)return "";if(!r.ok)throw r.status;return r.text()}).then(function(t){var o={};if(!t)return o;var L=t.trim().split(/\r?\n/),H=L[0].split(","),ic=H.indexOf("CURRENCY"),it=H.indexOf("TIME_PERIOD"),iv=H.indexOf("OBS_VALUE");
  for(var i=1;i<L.length;i++){var a=L[i].split(","),v=parseFloat(a[iv]);if(!isFinite(v))continue;(o[a[it]]=o[a[it]]||{EUR:1})[a[ic]]=v}return o})}
function cevir(m,base,syms,amt){if(!m||m[base]==null)return null;var r={},ks=syms.length?syms:Object.keys(m),n=0;
 ks.forEach(function(k){if(k===base||m[k]==null)return;r[k]=+((m[k]/m[base])*amt).toPrecision(6);n++});return n?r:null}
function cevap(url){
 var U=new URL(url),p=U.pathname.replace(/^\/v1/,"").replace(/^\//,""),q=U.searchParams;
 var base=(q.get("base")||q.get("from")||"EUR").toUpperCase(),sy=(q.get("symbols")||q.get("to")||"").toUpperCase(),syms=sy?sy.split(","):[],amt=+(q.get("amount")||1)||1;
 var bugun=iso(Date.now()),tek,s,e;
 if(p==="latest"||p===""){tek=1;s=gun(bugun,-12);e=bugun}
 else{var m=p.match(/^(\d{4}-\d{2}-\d{2})(\.\.(\d{4}-\d{2}-\d{2})?)?$/);if(!m)throw "bicim";
  if(m[2]){s=m[1];e=m[3]||bugun;tek=0}else{tek=1;e=m[1];s=gun(e,-12)}}
 if(e>bugun)e=bugun;var e2=tek?gun(e,10):e;if(e2>bugun)e2=bugun;
 var need=syms.length?syms.concat([base]):[];
 var eksik=false;
 return arsiv(s,e2).then(function(A){
   if(A.son&&A.son<e){var gs=gun(A.son,1);return ecb(gs,e,need.length?need:[]).then(function(B){for(var d in B)A.o[d]=B[d];return A.o}).catch(function(){eksik=true;return A.o})}
   return A.o
  },function(){return ecb(s,e2,need.length?need:[])})
 .then(function(o){var ds=Object.keys(o).sort();if(!ds.length)throw "bos";
   if(tek){var i,r;for(i=ds.length-1;i>=0;i--){if(ds[i]>e)continue;r=cevir(o[ds[i]],base,syms,amt);if(r)return {eksik:eksik,j:{amount:amt,base:base,date:ds[i],rates:r}}}
    for(i=0;i<ds.length;i++){if(ds[i]<=e)continue;r=cevir(o[ds[i]],base,syms,amt);if(r)return {eksik:eksik,j:{amount:amt,base:base,date:ds[i],rates:r}}}throw "bos"}
   var R={},f="",l="";ds.forEach(function(d){var r=cevir(o[d],base,syms,amt);if(r){R[d]=r;if(!f)f=d;l=d}});if(!f)throw "bos";
   return {eksik:eksik,j:{amount:amt,base:base,start_date:f,end_date:l,rates:R}}})}
function yanit(j){return new Response(JSON.stringify(j),{status:200,headers:{"Content-Type":"application/json"}})}
window.fetch=function(inp,init){var url=typeof inp==="string"?inp:(inp&&inp.url)||"";
 if(url.indexOf("//api.frankfurter.")<0)return OF(inp,init);
 var sig=init&&init.signal;
 var P=cevap(url).then(function(x){if(!x.eksik)return yanit(x.j);
    return tmo(OF(url),8000).then(function(r){if(!r.ok)throw 0;return r}).catch(function(){return yanit(x.j)})},
   function(){return tmo(OF(url),9000)});
 if(!sig)return P;
 return new Promise(function(res,rej){if(sig.aborted)return rej(new DOMException("Aborted","AbortError"));sig.addEventListener("abort",function(){rej(new DOMException("Aborted","AbortError"))});P.then(res,rej)})};
})();
