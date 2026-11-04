/* DZ-MVBANKA: mevduat varsayılan oranı banka tablosundan (4 Kasım 2026) */
  function mvOrt(){var tb=$("dzBanka");if(!tb)return null;var a=[].map.call(tb.querySelectorAll("tr[data-std]"),function(r){return parseFloat(r.getAttribute("data-std"))}).filter(function(x){return isFinite(x)&&x>0});if(!a.length)return null;var r0=tb.querySelector("tr[data-tarih]");return {o:Math.round(a.reduce(function(s,x){return s+x},0)/a.length*100)/100,n:a.length,t:r0?r0.getAttribute("data-tarih"):""}}
  function mvDef(){var m=mvOrt();return m?String(m.o):"40"}
  function mvBanka(){var m=mvOrt(),tb=$("dzBanka"),el=$("dzMevduat");if(!m||!tb||!el||$("mvBn"))return;
    var AY=["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"],d=/^\d{4}-\d{2}-\d{2}$/.test(m.t||"")?(+m.t.slice(8))+" "+AY[+m.t.slice(5,7)-1]+" "+m.t.slice(0,4):"";
    var kf=el.querySelector(".dz-kf");if(kf)kf.insertAdjacentHTML("afterend",'<div class="dz-note" id="mvBn">Faiz kutusundaki oran, aşağıdaki tabloda yer alan '+m.n+' bankanın 32 günlük standart oranlarının ortalamasıdır (%'+fmt(m.o,2)+(d?", "+d:"")+'). Tablodaki bir bankanın satırına dokunarak o bankanın oranıyla hesaplayabilirsin; kampanya hücresine dokunursan kampanya oranı kullanılır.</div>');
    [].forEach.call(tb.querySelectorAll("tr[data-std]"),function(r){r.style.cursor="pointer";r.title="Bu oranla hesapla";r.setAttribute("tabindex","0");
      var go=function(ev){var t=ev&&ev.target;if(t&&t.closest&&t.closest("a"))return;var td=t&&t.closest?t.closest("td"):null,ix=td?[].indexOf.call(r.cells,td):-1,k=parseFloat(r.getAttribute("data-kamp")),o=(ix===2&&isFinite(k)&&k>0)?k:parseFloat(r.getAttribute("data-std"));if(!isFinite(o))return;
        var F=$("mvF");F.value=F.type==="number"?String(o):String(o).replace(".",",");F.dispatchEvent(new Event("input",{bubbles:true}));
        var g=$("mvG"),gd=parseInt(r.getAttribute("data-gun"),10);if(g&&gd>0&&pnum(g.value)!==gd){g.value=String(gd);g.dispatchEvent(new Event("input",{bubbles:true}))}
        el.scrollIntoView({behavior:"smooth",block:"center"})};
      r.addEventListener("click",go);r.addEventListener("keydown",function(e){if(e.key==="Enter")go(e)})})}
  /* DZ-INTRO: mobilde hesaplayıcıyı yukarı almak için giriş paragrafını 3 satıra kısalt (4 Kasım 2026) */
  function dzIntro(){try{if(window.innerWidth>700)return;var b=document.querySelector(".post-body");if(!b)return;var p=b.firstElementChild;if(!p||p.tagName!=="P"||p.classList.contains("dz-cl"))return;var nx=p.nextElementSibling;if(!nx||!nx.querySelector||!nx.querySelector(".dz-tool"))return;if(p.getBoundingClientRect().height<80)return;
    p.classList.add("dz-cl");var a=document.createElement("button");a.type="button";a.className="dz-clb";a.textContent="Devamını oku";a.setAttribute("aria-expanded","false");
    a.addEventListener("click",function(){var k=p.classList.toggle("dz-cl");a.textContent=k?"Devamını oku":"Daha az göster";a.setAttribute("aria-expanded",k?"false":"true")});p.parentNode.insertBefore(a,nx)}catch(e){}}
