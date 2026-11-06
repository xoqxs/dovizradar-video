/* Döviz Radar – hafif kur widget'ı (https://www.dovizradar.com/p/kur-widget.html)
   Kullanım: <div class="dovizradar-widget" data-tur="liste"></div>
             <script async src="https://cdn.jsdelivr.net/gh/xoqxs/dovizradar-video@main/widget/dz-widget.js"></script>
   data-tur: liste | doviz | altin | kripto    data-tema: acik | koyu | oto (varsayılan oto)
   Fiyatlar bilgilendirme amaçlıdır, yatırım tavsiyesi değildir. */
(function () {
  "use strict";
  if (window.__dzWidget) { window.__dzWidget(); return; }
  var TR = "https://finans.truncgil.com/v4/today.json",
      CG = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,ripple,tether&vs_currencies=try&include_24hr_change=true",
      SITE = "https://www.dovizradar.com",
      L = {
        liste: { b: "Canlı piyasalar", k: [["USD", "Dolar", "/p/dolar-kac-tl.html"], ["EUR", "Euro", "/p/euro-kac-tl.html"], ["GBP", "Sterlin", "/p/sterlin-kac-tl.html"], ["GRA", "Gram altın", "/p/altin-hesaplama.html"], ["CEYREKALTIN", "Çeyrek altın", "/p/altin-hesaplama.html"], ["c:bitcoin", "Bitcoin", "/"]] },
        doviz: { b: "Döviz kurları", k: [["USD", "ABD doları"], ["EUR", "Euro"], ["GBP", "İngiliz sterlini"], ["CHF", "İsviçre frangı"], ["SAR", "Suudi riyali"], ["AED", "BAE dirhemi"], ["RUB", "Rus rublesi"], ["JPY", "Japon yeni"]] },
        altin: { b: "Altın fiyatları", k: [["GRA", "Gram altın"], ["CEYREKALTIN", "Çeyrek altın"], ["YARIMALTIN", "Yarım altın"], ["TAMALTIN", "Tam altın"], ["CUMHURIYETALTINI", "Cumhuriyet altını"], ["14AYARALTIN", "14 ayar (gram)"], ["GUMUS", "Gram gümüş"]] },
        kripto: { b: "Kripto paralar", k: [["c:bitcoin", "Bitcoin"], ["c:ethereum", "Ethereum"], ["c:solana", "Solana"], ["c:ripple", "XRP"], ["c:tether", "Tether (USDT)"]] }
      },
      CSS = ":host{all:initial;display:block;font:14px/1.35 system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif}" +
        ".w{--bg:#fff;--fg:#0f172a;--mu:#64748b;--ln:#e2e8f0;--up:#15803d;--dn:#b91c1c;--ac:#0e7490;background:var(--bg);color:var(--fg);border:1px solid var(--ln);border-radius:10px;overflow:hidden}" +
        ".w.k{--bg:#0f172a;--fg:#e2e8f0;--mu:#94a3b8;--ln:#1e293b;--up:#4ade80;--dn:#f87171;--ac:#5eead4}" +
        "@media (prefers-color-scheme:dark){.w.o{--bg:#0f172a;--fg:#e2e8f0;--mu:#94a3b8;--ln:#1e293b;--up:#4ade80;--dn:#f87171;--ac:#5eead4}}" +
        ".h{display:flex;justify-content:space-between;align-items:baseline;padding:9px 12px;border-bottom:1px solid var(--ln);font-weight:700}" +
        ".h small{font-weight:400;color:var(--mu);font-size:11px}" +
        "table{width:100%;border-collapse:collapse}td{padding:7px 12px;border-bottom:1px solid var(--ln);white-space:nowrap}" +
        "tr:last-child td{border-bottom:0}td.v{text-align:right;font-variant-numeric:tabular-nums;font-weight:600}" +
        "td.c{text-align:right;width:62px;font-variant-numeric:tabular-nums;font-size:12px}.u{color:var(--up)}.d{color:var(--dn)}" +
        "a{color:inherit;text-decoration:none}a:hover{text-decoration:underline}.f{padding:6px 12px;font-size:11px;color:var(--mu);border-top:1px solid var(--ln)}" +
        ".f a{color:var(--ac);font-weight:600}.e{padding:14px 12px;color:var(--mu)}";
  var cache = { t: 0, tr: null, cg: null }, inflight = null;

  function get(u, ms) {
    return new Promise(function (ok, no) {
      var done = false, t = setTimeout(function () { done = true; no("zaman"); }, ms || 8000);
      fetch(u, { cache: "no-store" }).then(function (r) { if (!r.ok) throw r.status; return r.text(); }).then(pj)
        .then(function (j) { if (!done) { clearTimeout(t); ok(j); } }, function (e) { if (!done) { clearTimeout(t); no(e); } });
    });
  }
  /* Kaynak bazen JSON'u eksik kapanışla gönderir: onarmayı dene */
  function pj(t) {
    t = String(t).trim();
    try { return JSON.parse(t); } catch (e) {}
    for (var s = "}", i = 0; i < 2; i++, s += "}") { try { return JSON.parse(t + s); } catch (e) {} }
    var k = t.lastIndexOf("},\"");
    if (k > 0) { try { return JSON.parse(t.slice(0, k + 1) + "}"); } catch (e) {} }
    throw "json";
  }
  function load(needCg) {
    if (Date.now() - cache.t < 55000 && cache.tr && (!needCg || cache.cg)) return Promise.resolve(cache);
    if (inflight) return inflight;
    inflight = Promise.all([
      get(TR).catch(function () { return cache.tr; }),
      needCg ? get(CG).catch(function () { return cache.cg; }) : Promise.resolve(cache.cg)
    ]).then(function (a) { cache.tr = a[0]; cache.cg = a[1]; cache.t = Date.now(); inflight = null; return cache; },
            function () { inflight = null; return cache; });
    return inflight;
  }
  function fmt(n) {
    var d = n >= 10000 ? 0 : n >= 100 ? 2 : n >= 1 ? 4 : 6;
    try { return n.toLocaleString("tr-TR", { minimumFractionDigits: d, maximumFractionDigits: d }); } catch (e) { return String(n); }
  }
  function pc(c) {
    if (!isFinite(c)) return "";
    var s = (c > 0 ? "+" : c < 0 ? "−" : "") + Math.abs(c).toLocaleString("tr-TR", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    return '<span class="' + (c > 0 ? "u" : c < 0 ? "d" : "") + '">%' + s + "</span>";
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function val(C, key) {
    if (key.indexOf("c:") === 0) { var g = C.cg && C.cg[key.slice(2)]; return g ? { v: g["try"], c: g.try_24h_change } : null; }
    var x = C.tr && C.tr[key]; return x && x.Selling > 0 ? { v: +x.Selling, c: +x.Change } : null;
  }
  function draw(el) {
    var tur = L[el.getAttribute("data-tur")] ? el.getAttribute("data-tur") : "liste", D = L[tur],
        tema = el.getAttribute("data-tema") || "oto", R = el.__dzR;
    var needCg = D.k.some(function (k) { return k[0].indexOf("c:") === 0; });
    return load(needCg).then(function (C) {
      var rows = "", n = 0;
      D.k.forEach(function (k) {
        var x = val(C, k[0]); if (!x) return; n++;
        var ad = k[2] ? '<a href="' + SITE + k[2] + '" target="_blank" rel="noopener">' + esc(k[1]) + "</a>" : esc(k[1]);
        rows += "<tr><td>" + ad + '</td><td class="v">' + fmt(x.v) + ' ₺</td><td class="c">' + pc(x.c) + "</td></tr>";
      });
      var up = C.tr && C.tr.Update_Date ? String(C.tr.Update_Date).slice(11, 16) : "";
      R.innerHTML = "<style>" + CSS + '</style><div class="w ' + (tema === "koyu" ? "k" : tema === "acik" ? "" : "o") + '"><div class="h">' + esc(D.b) +
        "<small>" + (up ? "Güncelleme " + up : "") + "</small></div>" +
        (n ? "<table>" + rows + "</table>" : '<div class="e">Fiyatlar şu an yüklenemedi.</div>') +
        '<div class="f">Satış fiyatı · <a href="' + SITE + '/" target="_blank" rel="noopener">Döviz Radar</a> · yatırım tavsiyesi değildir</div></div>';
    });
  }
  function init() {
    var els = document.querySelectorAll(".dovizradar-widget:not([data-dz-on])");
    Array.prototype.forEach.call(els, function (el) {
      el.setAttribute("data-dz-on", "1");
      el.__dzR = el.attachShadow ? el.attachShadow({ mode: "open" }) : el;
      draw(el);
      setInterval(function () { if (!document.hidden) draw(el); }, 60000);
    });
  }
  window.__dzWidget = init;
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
