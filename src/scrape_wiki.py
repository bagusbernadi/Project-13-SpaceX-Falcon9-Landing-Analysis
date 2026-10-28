"""Baca tabel peluncuran Falcon 9 dari HTML revisi Wikipedia yang tersimpan di data/raw/.

Input : data/raw/*.html (Save as HTML only dari halaman Wikipedia, revisi 1382396504)
Output: data/clean/wiki_rows.csv  (satu baris per peluncuran Falcon 9 dengan kolom landing)
        outputs/cleaning_log.csv  (setiap baris yang dibuang, diubah, atau diisi)
Aturan: hanya tabel dengan kolom 'Booster landing' (tabel 'Launch history').
Baris detail (sel digabung colspan, berisi deskripsi misi) dibuang.
"""
import csv
import glob
import io
import os
import re
import sys

import pandas as pd

RAW_DIR = "data/raw"
OUT_CSV = "data/clean/wiki_rows.csv"
LOG_CSV = "outputs/cleaning_log.csv"


def find_html():
    files = sorted(glob.glob(os.path.join(RAW_DIR, "*.html")))
    if not files:
        sys.exit("Tidak ada berkas .html di data/raw/. Ekstrak zip dari DataCenter dulu.")
    return files[0]


def is_detail_row(row):
    """Baris detail: semua sel selain nomor penerbangan berisi teks yang sama (colspan)."""
    vals = [str(v) for v in row.values[1:] if str(v) != "nan"]
    return len(vals) > 0 and len(set(vals)) == 1


def parse_landing(raw):
    """Pisahkan hasil dan jenis landing dari teks sel, mis. 'Success (ASOG)'."""
    s = str(raw)
    if s == "nan" or s.strip() == "":
        return "unknown", "unknown", ""
    m = re.match(r"^\s*([A-Za-z ]+?)\s*(?:\((.*)\))?\s*$", s)
    outcome = m.group(1).strip() if m else s
    place = m.group(2).strip() if m and m.group(2) else ""
    return outcome, place, s


def landing_type(place, outcome):
    p = place.upper()
    if outcome.lower() == "no attempt" or outcome.lower().startswith("not attempted"):
        return "Tidak dicoba"
    if p.startswith("LZ") or p.startswith("LZ-") or "LANDING ZONE" in p:
        return "RTLS (darat)"
    if p in {"ASOG", "JRTI", "OCISLY", "ASDS"} or p.startswith("JRTI") or p.startswith("ASOG"):
        return "ASDS (kapal drone)"
    if "OCEAN" in p:
        return "Ocean (uji di laut)"
    if p == "":
        return "Tidak dicoba"
    return "Lainnya"


def main():
    os.makedirs("data/clean", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    path = find_html()
    with open(path, encoding="utf-8") as f:
        html = f.read()
    tables = pd.read_html(io.StringIO(html))
    launch_tables = [t for t in tables if "Booster landing" in t.columns]
    log = []
    rows = []
    for ti, t in enumerate(launch_tables):
        for idx, r in t.iterrows():
            if is_detail_row(r):
                log.append([f"table{ti}", idx, "dibuang", "baris detail (colspan)"])
                continue
            flight = str(r["Flight No."]).strip()
            if not re.fullmatch(r"\d+", flight):
                log.append([f"table{ti}", idx, "dibuang", f"Flight No. bukan angka: {flight}"])
                continue
            rows.append(
                {
                    "src_table": ti,
                    "flight_no": int(flight),
                    "date_raw": str(r["Date and time (UTC)"]),
                    "version_raw": str(r["Version, booster[i]"]),
                    "site_raw": str(r["Launch site"]),
                    "payload_raw": str(r["Payload mass"]),
                    "orbit_raw": str(r["Orbit"]),
                    "customer_raw": str(r["Customer"]),
                    "outcome_raw": str(r["Launch outcome"]),
                    "landing_raw": str(r["Booster landing"]),
                }
            )
    df = pd.DataFrame(rows)
    # Tie-breaker: flight_no lalu src_table agar urutan stabil.
    df = df.sort_values(["flight_no", "src_table"], kind="mergesort").reset_index(drop=True)
    # Flight yang muncul lebih dari sekali: simpan baris pertama, catat sisanya.
    # Sisa baris biasanya payload kedua (misi dua muatan) atau salinan baris yang sama.
    dup = df.duplicated(subset=["flight_no"], keep="first")
    for _, r in df[dup].iterrows():
        log.append([f"table{int(r.src_table)}", int(r.flight_no), "dibuang",
                    f"flight_no ganda; payload={r.payload_raw}"])
    df = df[~dup].reset_index(drop=True)
    df.to_csv(OUT_CSV, index=False, quoting=csv.QUOTE_MINIMAL)
    log = sorted(log, key=lambda x: (str(x[0]), str(x[1]), str(x[2]), str(x[3])))
    with open(LOG_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sumber", "baris_asal", "aksi", "alasan"])
        w.writerows(log)
    print(f"sumber: {path}")
    print(f"tabel peluncuran: {len(launch_tables)}")
    print(f"baris peluncuran: {len(df)}")
    print(f"baris log: {len(log)}")
    print(f"flight_no unik: {df['flight_no'].nunique()}")
    print(f"flight_no ganda: {(df.groupby('flight_no').size() > 1).sum()}")


if __name__ == "__main__":
    main()
