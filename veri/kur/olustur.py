#!/usr/bin/env python3
"""ECB referans kurlarından (EUR bazlı) yıllık JSON dosyaları üretir.
Kullanım: python3 olustur.py <eurofxref-hist.csv> [cikti_klasoru]
Biçim: {"base":"EUR","c":[para birimleri],"d":{"YYYY-AA-GG":[oranlar|null]}}
Kaynak: Avrupa Merkez Bankası (ECB) euro referans kurları."""
import csv, json, sys, os
src = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
KEEP = ["USD","JPY","BGN","CZK","DKK","GBP","HUF","PLN","RON","SEK","CHF","ISK","NOK","HRK","RUB","TRY",
        "AUD","BRL","CAD","CNY","HKD","IDR","ILS","INR","KRW","MXN","MYR","NZD","PHP","SGD","THB","ZAR"]
years = {}
with open(src, newline="") as f:
    r = csv.reader(f); head = [h.strip() for h in next(r)]
    idx = {h: i for i, h in enumerate(head)}
    for row in r:
        if not row or not row[0].strip(): continue
        d = row[0].strip()
        if d < "2005-01-01": continue
        vals = []
        for c in KEEP:
            v = row[idx[c]].strip() if c in idx and idx[c] < len(row) else "N/A"
            try: vals.append(float(v))
            except ValueError: vals.append(None)
        years.setdefault(d[:4], {})[d] = vals
for y, dd in years.items():
    # tamamen boş kolonları da korur (sabit sıra); tarihleri sırala
    obj = {"base": "EUR", "src": "ECB euro referans kurları", "c": KEEP, "d": dict(sorted(dd.items()))}
    with open(os.path.join(out, y + ".json"), "w") as f:
        json.dump(obj, f, separators=(",", ":"))
print("yıllar:", min(years), "-", max(years), "son tarih:", max(max(v) for v in years.values()))
