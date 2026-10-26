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
