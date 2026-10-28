# Döviz Radar video hattı (otomatik görevler için)

Çalışma klasörü: `mkdir -p /home/claude/work && cp pipeline/* /home/claude/work/ && cd /home/claude/work`
Gereken: `pip install --break-system-packages -q pillow` (PIL yoksa); playwright ve ffmpeg ortamda hazır.
Azure anahtarı: gizli depo `xoqxs/dovizradar-ayarlar` → `/home/claude/dovizradar-ayarlar/azure.txt` (1. satır anahtar, 2. satır bölge = eastus). Anahtarı ASLA yazdırma/loglama.

## scenes.json (çalışma klasöründe)
Liste; her sahne: `k` rozet, `t` başlık (<b> yeşil vurgu, <br>), `s` alt satır, `c` rozet rengi (#60a5fa piyasa, #fbbf24 altın/akaryakıt, #14b8a6 kripto/kapanış, #f87171 HABER), `n` seslendirme metni (sayıları YAZIYLA yaz: "kırk dokuz lira yetmiş kuruş"; "dovizradar.com" yerine "Döviz Radar nokta kom").
İsteğe bağlı görsel alanları:
- `photo`: arka plan fotoğrafı (img/....jpg, üst 900px), `person`: {"img": "img/...jpg (kare)", "name": "Unvan Ad Soyad"}, `flag`: "us" | "tr"
- ya da `img`: "fed" | "tcmb" | "us" | "tr" | "pump" (kendi çizimimiz)

## Komutlar
1. `python3 tts.py tr-TR-AhmetNeural` (prosody +15%, sahne arası 0,15 sn) → n*.wav, scenes_d.json
2. `node make.js` → s*.png (kontrol: en az 2 PNG'yi Read ile aç, taşma var mı)
3. `python3 assemble.py CIKTI.mp4` (müzik 0.30, son cümle sonrası 1,2 sn)

## Fotoğraf (Wikimedia Commons, wm.py)
- `python3 wm.py s "arama"` → dosya adları; `python3 wm.py i "File:..." img/ad.jpg` → lisans + indirme.
- Yalnızca lisansı Public domain, CC0, CC BY veya CC BY-SA olanları kullan. CC BY/BY-SA ise YouTube açıklamasına "Görsel: <Yazar>, <Lisans>, Wikimedia Commons" ekle.
- Kişi fotoğrafı: o kişinin o makamda OLDUĞUNU önce iki kaynakla doğrula (ör. Fed Başkanı, TCMB Başkanı). Emin değilsen kişi fotoğrafı koyma.
- Büyük fotoğrafı PIL ile küçült (arka plan 1400px, kişi kare 600px).
Hazır doğrulanmış görseller (25 Ekim 2026): Fed binası "File:Eccles Building (26088200676).jpg" (PD), Fed Başkanı Kevin Warsh "File:Federal Reserve Chair Kevin Warsh delivers remarks at his swearing-in ceremony in the East Room of the White House, Friday, May 22, 2026. (Cropped).jpg" (PD).

## Görsel yoğunluğu (Kadir Bey isteği, 25 Ekim 2026)
Sahnelerin ÇOĞUNDA gerçek fotoğraf olsun (`photo` alanı; `person` ve `flag` isteğe bağlı). Öneriler: dolar sahnesi → ABD doları banknot fotoğrafı; euro → euro banknotları veya AB bayrağı; altın → altın külçe/çeyrek altın fotoğrafı; Bitcoin → fiziksel Bitcoin madeni para fotoğrafı; akaryakıt → akaryakıt pompası/istasyon; kanca sahnesi → İstanbul/borsa/para fotoğrafı; haberler → kurum binası + kurum başkanı + bayrak. Kapanış sahnesi fotoğrafsız kalabilir. Commons lisans kuralları aynen geçerli; uygun lisanslı fotoğraf bulunamazsa o sahne fotoğrafsız kalır.

## Kapanış (KISA, ~4 sn)
k "DÖVİZ RADAR", t "Canlı kurlar:<br><b>dovizradar.com</b>", s "Bilgilendirme amaçlıdır, yatırım tavsiyesi değildir.", n "Güncel kurlar Döviz Radar nokta kom'da. Abone olmayı unutmayın!"

## Veri alma (ÖNEMLİ — otomatik görevlerde WebFetch kullanma)
Zamanlanmış görevlerde WebFetch adres onayı isteyip başarısız olur. Sırayla dene:
1. Kabuk: `curl -s -m 15 <url>` (alan adı izinli listedeyse çalışır).
2. Olmazsa uygulama içi tarayıcı: tabs_create ile kendi sekmeni aç, `navigate` ile JSON adresine git, `get_page_text` ile JSON'u oku (Blogger sekmesine dokunma).
Adresler: https://open.er-api.com/v6/latest/USD · https://api.gold-api.com/price/XAU · https://api.coinbase.com/v2/prices/BTC-USD/spot · (haftalık) https://api.frankfurter.dev/v1/<baş>..<bit>?base=USD&symbols=TRY,EUR , https://api.coinbase.com/v2/prices/BTC-USD/spot?date=YYYY-MM-DD
Haberler: WebSearch serbest; haber sayfasını açman gerekirse yine tarayıcıda navigate + get_page_text kullan (WebFetch değil). Her haber iki bağımsız kaynakla doğrulanır.
Azure TTS (eastus.tts.speech.microsoft.com) ve Wikimedia kabuktan çalışır.

## ÖZGÜNLÜK VE KALİTE (Kadir Bey isteği, 27 Ekim 2026 — TÜM video görevleri için zorunlu)
Amaç: her video elle hazırlanmış gibi farklı ve kaliteli olsun; YouTube'un "tekrarlayan/şablon içerik" algısına düşmesin.
**Bol ve her seferinde farklı görsel**
- Kapanış hariç HER sahnede en az bir gerçek fotoğraf; sahnelerin en az yarısında ikinci fotoğraf (`photo2`, çerçeveli küçük görsel). Bir videoda aynı fotoğraf iki kez kullanılmaz.
- `pipeline/kullanilan-gorseller.txt` son 120 görselin kaydıdır. `python3 wm.py s "arama" 15` kullanılmışları "[KULLANILDI]" diye işaretler; `wm.py i` kullanılmış görseli indirmeyi reddeder ("TEKRAR"). Daima kullanılmamış görsel seç; aramayı çeşitlendir (farklı açı, farklı nesne: ör. altın için külçe, çeyrek altın, kuyumcu vitrini, bilezik, altın madeni, Kapalıçarşı). Yalnızca kurum binası/kurum başkanı gibi haber için zorunlu ve alternatifi olmayan görselde `TEKRAR=1` serbesttir (önce aynı kişinin/binanın başka fotoğrafını ara).
- Video bitince kullanilan-gorseller.txt'yi de commit et (wm.py indirirken otomatik yazar).
**Görünüm her videoda farklı**
- make.js her videoda farklı renk teması seçer; assemble.py sahne başına farklı kamera hareketi; music.py her videoda farklı tempo/ton/akor dizisi üretir (tohum: tarih-saat; elle `VSEED` verme).
- En az 1–2 sahnede `"layout":"full"` (tam ekran fotoğraf) kullan; düzenleri karıştır (full, üst fotoğraf, fotoğraf+photo2, kişi, çizim).
**Metin her seferinde yeni**
- Kanca cümlesi, sahne sırası, rozet (`k`) metinleri ve seslendirme her videoda yeniden yazılır; önceki videolarda kullanılan kalıp cümleleri tekrar etme (kapanış hariç). Rakamları sadece okumak yerine kısa bir yorum/bağlam ver ("geçen haftaya göre", "bunun anlamı şu"), soru sor, merak uyandır.
- Başlık kalıbını da çeşitlendir (her gün aynı başlık yapısı olmasın); son 5 videonun başlığına YouTube Studio içerik listesinden bak ve benzemesin.
- İlk 2 saniye çok önemli: kanca sahnesi tam ekran çarpıcı fotoğraf + kısa, merak uyandıran soru.
**Kalite kontrol (yüklemeden önce)**
- Tüm PNG'lere bak (Read): metin taşması, okunmayan yazı, kötü kırpılmış fotoğraf yok. Sorun varsa düzelt ve yeniden üret.
- Seslendirmede sayıların doğru okunduğunu ve son cümlenin kesilmediğini kontrol et (son sahne süresi + 1,2 sn kuyruk).
- Kendine sor: "Bu video dünkü videonun aynısı gibi mi görünüyor?" Evetse fotoğrafları/kancayı/düzeni değiştir.

## YOUTUBE SEO VE SPAM GÖRÜNMEME (Kadir Bey isteği, 28 Ekim 2026 — TÜM video görevleri için zorunlu)
Amaç: her video aramada bulunsun (YouTube SEO) ve kanal "otomatik/tekrarlayan içerik" gibi görünmesin.
**0) Önce günlüğü oku:** `pipeline/video-gunlugu.md` (son 15 video: tarih, tür, başlık, açı, biçim, kanca, ana anahtar kelime). Yeni video bu son 15 kayıttan başlık kalıbı, açı, biçim ve kanca cümlesi bakımından FARKLI olmalı. Video yayınlanınca günlüğe 1 satır ekle ve commit et.
**1) Günün açısı (piyasa ve uzun videolarda zorunlu):** Rakamları sırayla okumak yerine her videonun tek bir ana hikâyesi olsun (ör. "Fed kararı dolar/TL'yi nasıl etkiler?", "Altın neden rekor kırdı?", "Maaşın dolar karşılığı bu yıl ne oldu?", "Akaryakıt zammı cebe etkisi"). Rakamlar bu hikâyeyi destekler. Biçimi dönüşümlü seç ve son 3 videoda kullanılanı tekrarlama: (a) 3 soru–3 cevap, (b) "bugün bilmen gereken 3 şey", (c) karşılaştırma (dün/geçen hafta/geçen yıl), (d) "bunun cebine etkisi" örnek hesap, (e) haber önce, rakam sonra, (f) mini sözlük (bir terimi açıklayıp rakama bağla).
**2) Başlık (aranan ifadeyle başlasın):** Ana anahtar kelimeyi başa koy (ör. "Dolar Kaç TL? …", "Gram Altın Bugün …", "Fed Faiz Kararı …"). Hangi ifadenin arandığına YouTube arama kutusunun önerilerinden (studio dışında youtube.com arama kutusuna yazıp öneri listesini oku) ve sitenin Search Console sorgularından bak. 40–70 karakter, doğal Türkçe, tarih gerekiyorsa sonda. BÜYÜK HARF bağırma, yanıltıcı/abartılı ifade ("ŞOK", "çöküş geliyor"), emoji yığını YOK. Son 15 başlıkla aynı kalıbı kullanma (günlükten kontrol et).
**3) Açıklama (her video için yeniden yazılır):** 1. satır araç bağlantısı (görev talimatındaki gibi). 2–4. satırlar: o videoya ÖZGÜ 2–3 cümlelik özet; ana anahtar kelime ve 1–2 yan ifade doğal biçimde geçsin. Ardından kaynaklar, görsel atıfları, uyarı. Sabit kalıp metin yalnızca en alttaki kısa uyarı + kanal satırı olabilir; geri kalan her şey o güne özgü olmalı. 3–5 hashtag: konuya göre değişsin (her gün aynı 5 hashtag YOK; #shorts kısa videolarda kalabilir).
**4) Etiketler (Studio'da "Daha fazla göster" → Etiketler):** 6–12 alakalı etiket, videoya göre değişen (ör. "dolar kuru bugün, fed faiz kararı, gram altın fiyatı"); marka etiketi "döviz radar" bir kez. Alakasız/popüler etiket doldurma YOK. Etiket kutusu bulunamazsa bu adımı atla, yayını engelleme.
**5) Oynatma listeleri:** Videoyu türüne göre listeye ekle (Studio yükleme ekranındaki "Oynatma listeleri" seçimi): "Günlük Piyasa Özeti" (kısa piyasa), "Haftalık ve Gündem Özetleri" (uzun), "30 Saniyede Finans Bilgisi" (bilgi). Liste yoksa o adla oluştur. Liste açıklaması bir kez, özgün 2 cümle.
**6) Dil ve kategori:** Video dili Türkçe, kategori "Eğitim" (bilgi videoları) veya "Haberler ve Politika"/"Kişiler ve Bloglar" yerine uygun olan; bulunamazsa varsayılan bırak.
**7) Spam sinyalleri – YAPMA:** Aynı gün aynı türden 2 video; başka kanalların videosunu/ses/müziğini kullanmak; açıklamaya alakasız bağlantı veya çok sayıda bağlantı (en fazla 2 site bağlantısı); yorumlara otomatik yorum/beğeni; abone olun ricasını 1'den fazla tekrar etmek; aynı seslendirme cümlesini her videoda kullanmak (kapanış cümlesini de 4–5 farklı varyant arasından döndür: ör. "Güncel kurlar Döviz Radar nokta kom'da. Abone olmayı unutmayın!", "Hesaplama araçları Döviz Radar nokta kom'da, kanala abone olun.", "Detaylar ve canlı kurlar Döviz Radar nokta kom'da.", "Kendi hesabınızı Döviz Radar nokta kom'da yapın; görüşmek üzere.").
**8) Son kontrol (yüklemeden önce kendine sor):** "Bu başlık/açıklama/kanca son 15 videodan birine benziyor mu?" Evetse değiştir. "Biri bu videoyu izleyince yeni ne öğreniyor?" Cevap yoksa açıyı güçlendir.
