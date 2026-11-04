# Geçmiş kur verisi (dovizradar.com)

`YYYY.json` dosyaları Avrupa Merkez Bankası (ECB) euro referans kurlarıdır (EUR bazlı, iş günleri, 1999–bugün; 1999–2004 TRY = eski TL ÷ 1.000.000).
Biçim: `{"base":"EUR","c":[para birimleri],"d":{"YYYY-AA-GG":[oranlar | null]}}`. X/TRY = TRY ÷ X.

- Site teması bu dosyaları birincil kaynak olarak okur (jsDelivr, yedek raw.githubusercontent).
- Dosyadaki son tarihten sonraki günler canlı ECB API'sinden (data-api.ecb.europa.eu), o da çalışmazsa frankfurter.dev'den tamamlanır.
- `.github/workflows/kur-guncelle.yml` hafta içi her gün ECB dosyasını indirip `olustur.py` ile günceller.
