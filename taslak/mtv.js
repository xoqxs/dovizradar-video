/* DZ-MTV: MTV hesaplama 2026 resmi / 2027 tahmini (13 Kasım 2026) */
function mtvCalc(){var el=$("dzMtv");if(!el||el.__on)return;el.__on=1;
  var C=[[[5750,4010,2238,1689,593],[6319,4409,2459,1861,655],[6902,4807,2693,2032,706]],[[10016,7510,4354,3077,1181],[11023,8264,4794,3375,1290],[12028,9012,5220,3685,1408]],[[19472,15226,8948,5458,2113],[21251,16600,9775,5964,2307]],[[30679,23625,13886,8264,3248],[33474,25784,15147,9012,3547]],[[46027,33413,20874,12465,4930],[50217,36448,22768,13606,5378]],[[64175,55837,34878,18758,6875],[70018,60905,38053,20466,7503]],[[97744,87954,52976,26443,9684],[106641,95940,57791,28839,10578]],[[153684,132712,78152,34878,13886],[167671,144770,85271,38053,15147]],[[251554,188627,111714,50206,19472],[274415,205781,121873,54769,21251]]],M=[[1069,799,589,362,136],[2214,1676,1069,589,362],[5719,3398,1676,1069,589],[13876,9167,5719,4540,2214]],TH={"2024":[[180600,316400],[180600,316400],[452800],[452800],[565500],[1131800],[1131800],[1811800],[2151400]],"2025":[[259900,455300],[259900,455300],[651700],[651700],[813900],[1628900],[1628900],[2607700],[3096500]],"2026":[[309100,541500],[309100,541500],[775100],[775100],[968100],[1937500],[1937500],[3101800],[3683200]],"2027":[[395100,692100],[395100,692100],[990800],[990800],[1237500],[2476700],[2476700],[3965000],[4708200]]},R27=0.2783,
    BL=["1300 cm³ ve altı","1301–1600 cm³","1601–1800 cm³","1801–2000 cm³","2001–2500 cm³","2501–3000 cm³","3001–3500 cm³","3501–4000 cm³","4001 cm³ ve üzeri"],
    KW=["70 kW'a kadar","70–85 kW","85–105 kW","105–120 kW","120–150 kW","150–180 kW","180–210 kW","210–240 kW","240 kW üzeri"],
    ML=["100–250 cm³","251–650 cm³","651–1200 cm³","1201 cm³ ve üzeri"],MK=["6–15 kW","15–40 kW","40–60 kW","60 kW üzeri"],
    AG=["1–3 yaş","4–6 yaş","7–11 yaş","12–15 yaş","16 yaş ve üzeri"],DN=["1. dilim (en düşük)","2. dilim","3. dilim (en yüksek)"],gT=0;
  function op(a,s){return a.map(function(x,i){return '<option value="'+i+'"'+(i===s?' selected':'')+'>'+x+'</option>'}).join("")}
  var my="";for(var y=2027;y>=1985;y--)my+='<option value="'+y+'"'+(y===2024?' selected':'')+'>'+y+'</option>';
  var gy='<option value="2017">2017 veya önce</option>';for(var y=2018;y<=2027;y++)gy+='<option value="'+y+'"'+(y===2024?' selected':'')+'>'+y+'</option>';
  el.innerHTML='<div class="dz-kf"><label>Vergi yılı<select id="mtY"><option value="2027" selected>2027 (tahmini)</option><option value="2026">2026 (resmi)</option></select></label>'+
   '<label>Araç türü<select id="mtT"><option value="o">Otomobil (benzin, dizel, LPG, hibrit)</option><option value="e">Tam elektrikli otomobil</option><option value="m">Motosiklet</option><option value="n">Tam elektrikli motosiklet</option></select></label>'+
   '<label><span id="mtBL">Motor silindir hacmi</span><select id="mtB"></select></label>'+
   '<label>Model yılı (ruhsatta yazan)<select id="mtM">'+my+'</select></label>'+
   '<label id="mtGw">İlk tescil yılı<select id="mtG">'+gy+'</select></label>'+
   '<label id="mtVw">İlk tescildeki taşıt değeri (₺) · isteğe bağlı<input type="text" id="mtV" inputmode="numeric" autocomplete="off" placeholder="Örn. 1.250.000"/></label>'+
   '<label id="mtDw">Değer dilimi<select id="mtD"></select></label></div><div class="dz-note" id="mtH"></div><div class="dz-kr" id="mtR"></div>';
  var Y=$("mtY"),T=$("mtT"),B=$("mtB"),Mo=$("mtM"),G=$("mtG"),V=$("mtV"),Dd=$("mtD"),R=$("mtR"),H=$("mtH");
  function tl(n){return fmt(n,0)+" ₺"}
  function band(){var t=T.value;B.innerHTML=op(t==="o"?BL:t==="e"?KW:t==="m"?ML:MK,+B.value||(t==="m"||t==="n"?0:1));$("mtBL").textContent=(t==="e"||t==="n")?"Motor gücü":"Motor silindir hacmi"}
  function dil(){var b=+B.value,n=C[b].length,s=Math.min(+Dd.value||0,n-1);Dd.innerHTML=op(n===3?DN:[DN[0],"2. dilim (en yüksek)"],s)}
  function auto(){var g=+G.value,b=+B.value,t=TH[g],v=+String(V.value).replace(/[^0-9]/g,"");H.innerHTML="";
    if(T.value==="m"||T.value==="n")return;
    if(g<=2017){H.innerHTML="2018'den önce tescil edilen araçlarda değer dilimi yoktur; vergi motor hacmi ve yaşa göre belirlenir.";return}
    if(!t){H.innerHTML="<b>"+g+"</b> yılında tescil edilen araçlar için değer sınırlarını sitede tutmuyoruz. Aracının dilimini bu yıl ödediğin MTV tutarından (e-Devlet veya GİB) bulup seçebilirsin.";return}
    var s=t[b],txt=s.length===2?"1. dilim: "+tl(s[0])+"'ye kadar · 2. dilim: "+tl(s[0])+" – "+tl(s[1])+" · 3. dilim: "+tl(s[1])+" üzeri":"1. dilim: "+tl(s[0])+"'ye kadar · 2. dilim: "+tl(s[0])+" üzeri";
    H.innerHTML="<b>"+g+"</b> tescilli araçlar için sınırlar"+(g===2027?" (tahmini)":"")+": "+txt+". Değer, ilk alımdaki ÖTV dahil, KDV hariç tutardır; bu dilim sonraki yıllarda değişmez.";
    if(v>0){var k=0;while(k<s.length&&v>s[k])k++;Dd.value=String(k)}}
  function calc(){var y=+Y.value,t=T.value,b=+B.value,m=+Mo.value,g=+G.value,mo=(t==="m"||t==="n"),el2=(t==="e"||t==="n");
    $("mtGw").style.display=mo?"none":"";$("mtVw").style.display=(mo||g<=2017||!TH[g])?"none":"";$("mtDw").style.display=(mo||g<=2017)?"none":"";
    auto();
    var age=y-m+1;if(age<1){R.innerHTML='<div class="dz-note">Model yılı vergi yılından sonra olamaz.</div>';return}
    var c=age<=3?0:age<=6?1:age<=11?2:age<=15?3:4,row=0,base;
    if(mo){base=M[b][c]}else{row=g<=2017?0:Math.min(+Dd.value||0,C[b].length-1);base=C[b][row][c]}
    if(el2)base=Math.floor(base*0.25);
    var t26=mo?M[b][c]:C[b][row][c],amt=y===2027?Math.floor(Math.floor(t26*(1+R27))*(el2?0.25:1)):base;
    var rw=[["Ocak taksiti",fmt(amt/2,2)+" ₺"],["Temmuz taksiti",fmt(amt/2,2)+" ₺"],["Araç yaşı ("+y+")",age+" · "+AG[c]+" grubu"],
      ["Uygulanan satır",(mo?(el2?MK:ML)[b]:(el2?KW:BL)[b])+(mo?"":(g<=2017?" · 2018 öncesi tescil (I/A tarifesi)":" · "+(C[b].length===3?DN:[DN[0],"2. dilim (en yüksek)"])[row]))]];
    if(el2)rw.push(["Elektrikli araç indirimi","Tarife tutarının %25'i"]);
    if(y===2027)rw.push(["2026'da ödenen (resmi)",tl(base)],["Artış",tl(amt-base)+" · yeniden değerleme oranı %27,83 varsayımıyla"]);
    R.innerHTML=big(y+" yılı MTV"+(y===2027?" (tahmini)":""),tl(amt))+rows(rw)+'<div class="dz-note">'+(y===2027?"2027 tutarları resmi değildir: 2026 tarifesine %27,83 yeniden değerleme oranı uygulanarak hesaplanmıştır. Cumhurbaşkanı bu oranı değiştirebilir; geçen yıl artış %18,95 ile sınırlanmıştı. Resmi tutarlar Aralık sonunda yayımlanınca güncellenecek.":"31 Aralık 2025 tarihli Resmî Gazete'de yayımlanan MTV Genel Tebliği (Seri No: 58) tutarlarıdır.")+' Kesin borcunu GİB Hazır Değer veya e-Devlet üzerinden sorgulayabilirsin.</div>'}
  function all(){band();dil();calc()}
  T.addEventListener("change",function(){B.value="";all()});B.addEventListener("change",function(){dil();calc()});
  Mo.addEventListener("change",function(){if(!gT){var m=+Mo.value;G.value=String(m<2018?2017:Math.min(m,2027))}calc()});
  G.addEventListener("change",function(){gT=1;calc()});[Y,Dd].forEach(function(e){e.addEventListener("change",calc)});
  V.addEventListener("input",function(){var n=+String(V.value).replace(/[^0-9]/g,"");V.value=n?fmt(n,0):"";calc()});
  all()}
