/* Param ne olurdu: sayfaya gömülü aylık veri (script#dzPnoVeri) önce okunur; yoksa ağdan (4 Kasım 2026) */
  function pnoV(){if(PNC.v===undefined){try{var e=document.getElementById("dzPnoVeri");PNC.v=e?JSON.parse(e.textContent):null}catch(x){PNC.v=null}}return PNC.v}
  function pnoBtc(d){var V=pnoV();if(V&&V.b&&V.b[d])return Promise.resolve(V.b[d]);return pnoKl("BTCUSDT",d)}
