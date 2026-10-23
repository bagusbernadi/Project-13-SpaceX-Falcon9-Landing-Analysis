[← Back to portfolio](https://bagusbernadi.github.io/)

# Project 13: SpaceX Falcon 9 Landing Analysis

**Status: Design (rancangan).** Halaman rancangan ada di [`index.html`](index.html). Analisis, dashboard, dan angka hasil belum dikerjakan, sehingga bagian Analysis, Recommendation, dan Impact di bawah masih kosong.

**Tujuan:** membangun pipeline data dan dashboard dari data publik peluncuran Falcon 9 yang menunjukkan faktor misi yang paling terkait dengan keberhasilan landing first stage, beserta estimasi nilai reuse-nya.

| | |
|---|---|
| Kategori | Antariksa (Tech / Energi) |
| Tingkat | Mudah |
| Data | SpaceX API + tabel Wikipedia |
| Tools | DuckDB + SQL, Python (requests, pandas, BeautifulSoup) script .py, Streamlit + Plotly. scikit-learn opsional |

## 1. Problem

**Pertanyaan utama:** Faktor apa (orbit, payload, launch site, versi booster, reuse, tahun) yang paling terkait dengan keberhasilan landing first stage Falcon 9, dan bagaimana tren success rate-nya?

Rancangan memecahnya menjadi 14 pertanyaan (9 Utama, 4 Pendukung, 1 Tambahan) dalam tema tren, kondisi misi, pemulihan dan reuse booster, dampak, dan validitas data. Daftar lengkap ada di bagian 2 halaman rancangan.

## 2. Data

- Sumber data (SpaceX API): [here](https://github.com/r-spacex/SpaceX-API) (Versi: 4.0.0, Tanggal akses: 23 Oktober 2026)
- Sumber data (Wikipedia): [here](https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches) (Versi: revisi halaman saat diakses, Tanggal akses: 24 Oktober 2026)
- Ukuran (perkiraan, **belum diverifikasi**): ±200 peluncuran Falcon 9, 2010 sampai ±2022.
- Memperbarui repo capstone lama (notebook kursus) menjadi pipeline .py.
- Rencana tabel: `launches`, `boosters`, `dim_site`, `launches_wiki`.
- Lisensi dan sitasi: dicek di halaman sumber sebelum project dipublikasikan.
- Data mentah tidak di-commit ke repository.

## 3. Analysis

Belum dikerjakan. Rencana langkah (12 langkah, tahap A sampai D) ada di bagian 6 halaman rancangan. Semua angka nanti dihitung dari data dengan SQL dan dicek silang.

Hipotesis yang akan diuji (belum terbukti):
1. Success rate naik tajam sejak ±2016.
2. Block 5 hampir selalu berhasil.
3. GTO dan payload berat lebih jarang berhasil.
4. Booster reuse sama andalnya.
5. RTLS lebih sering berhasil daripada ASDS.

## 4. Recommendation

Belum dikerjakan. Output yang direncanakan: kondisi misi dengan peluang landing tertinggi.

## 5. Impact

Belum dikerjakan. Rumus yang akan dipakai (semua hasil diberi label `estimated`):

```
Nilai reuse = landing sukses × biaya booster (asumsi US$40 juta, label estimated)
```

## Batasan yang sudah diketahui

- Faktor saling terkait (tahun, versi, reuse).
- Jumlah data kecil per kelompok.
- SpaceX API dikelola komunitas dan berhenti diperbarui.

## Struktur repository

```
index.html   Halaman rancangan project (bisa dibuka di browser atau lewat GitHub Pages)
README.md    Dokumen ini
```

Folder `docs/`, `data/`, `scripts/`, `sql/`, `notebooks/`, `dashboard/`, dan `outputs/` ditambahkan saat pengerjaan dimulai.
