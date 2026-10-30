# 📄 LAPORAN TAHAP 2: DATA CLEANING & PREPROCESSING (PEMBERSIHAN DATA)

**Mata Kuliah:** Visualisasi Data  
**Program Studi:** Teknik Informatika - Semester VII  
**Tema Proyek:** Dashboard Visualisasi Data Interaktif COVID-19 Indonesia  
**Dataset:** COVID-19 Indonesia Time Series  

---

## 1. PENANGANAN MISSING VALUES (NILAI HILANG)
Pengecekan missing values dilakukan secara sistematis menggunakan fungsi `df.isnull().sum()`.
* **Kolom Demografi Spesifik Kota (`City or Regency`, `Special Status`):**
  * *Temuan:* Pada dataset mentah, kolom kabupaten/kota memiliki missing values > 30.000 records karena data berupa agregat level provinsi.
  * *Aksi:* Kolom dilepas (*dropped*) dari dataset analitis utama karena tidak relevan pada agregasi level provinsi.
* **Kolom Agregat Nasional (`Province` pada level 'Country'):**
  * *Temuan:* 896 baris memiliki nilai `Province` bernilai `NaN` karena mewakili total nasional.
  * *Aksi:* Baris dipisahkan dari tabel level provinsi untuk menghindari perhitungan ganda (*double-counting* / overestimation) pada analisis per provinsi.
* **Kolom Rasio & Metrik (`Growth Factor`, `Case Fatality Rate`):**
  * *Temuan:* Nilai `NaN` pada hari-hari awal pencatatan (sebelum ada kasus aktif atau riwayat kematian).
  * *Aksi:* Nilai null diisi (*imputation*) dengan nilai `0.0` atau dihitung ulang secara deterministik menggunakan rumus `(total_deaths / total_cases) * 100`.

---

## 2. DUPLICATE DATA (PENANGANAN DUPLIKASI)
* **Pengecekan Duplikat:** Menggunakan `df.duplicated().sum()`.
* **Hasil Deteksi:** 0 baris duplikasi mutlak pada tabel mentah.
* **Redundansi Tingkat Wilayah:** Ditemukan potensi duplikasi semantik antara baris `Location Level == 'Country'` (total Indonesia) dan baris `Location Level == 'Province'`.
* **Aksi Penanganan:** Dilakukan isolasi rekaman provinsi sebanyak 34 entitas resmi (`df[df['Location Level'] == 'Province']`) sehingga data bersih memiliki integritas referensial dan bebas redundansi.

---

## 3. DATA TYPE CORRECTIONS (KOREKSI TIPE DATA)

| Nama Kolom | Tipe Data Asli | Tipe Data Baru | Metode Transformasi | Alasan & Manfaat |
| :--- | :--- | :--- | :--- | :--- |
| `Date` | `object` (string M/D/YYYY) | `datetime64[ns]` | `pd.to_datetime(..., format='%m/%d/%Y')` | Memungkinkan operasi filter rentang tanggal, pemotongan mingguan (`week`), dan time-series indexing. |
| `New Cases` | `float64` / `int64` | `int64` | `.clip(lower=0).fillna(0).astype(int)` | Kasus riil manusia adalah bilangan bulat non-negatif. |
| `New Deaths` | `float64` / `int64` | `int64` | `.clip(lower=0).fillna(0).astype(int)` | Mortalitas harian berupa bilangan bulat non-negatif. |
| `New Recovered` | `float64` / `int64` | `int64` | `.clip(lower=0).fillna(0).astype(int)` | Pasien sembuh harian berupa bilangan bulat non-negatif. |
| `Province` | `object` | `string / category` | `.str.strip()` | Mempercepat operasi perbandingan string dan agregasi `groupby`. |
| `CFR` | `object` (e.g. `'2.34%'`) | `float64` | Dihitung ulang via formula `np.where` | Memungkinkan operasi statistik matematis (mean, median, IQR, boxplot). |

---

## 4. OUTLIERS (DETEKSI & PENANGANAN PENCILAN)
* **Metode Deteksi:**
  * Metode *Interquartile Range* (IQR) dengan ambang batas $Q1 - 1.5 \times IQR$ dan $Q3 + 1.5 \times IQR$.
  * Visualisasi sebaran menggunakan Box Plot kasus harian dan CFR.
* **Temuan Outlier:**
  * Lonjakan kasus harian sangat tinggi ditemukan pada puncak gelombang Delta (Juli–Agustus 2021) di DKI Jakarta (>14.000 kasus/hari) dan Jawa Barat (>10.000 kasus/hari).
  * Pada fase penyesuaian data (*data audit backlog*) oleh Dinas Kesehatan, terdapat satu hari pencatatan angka kematian rapel.
* **Aksi Penanganan:**
  * **Dipertahankan (*Keep*):** Nilai puncak gelombang (Delta dan Omicron) dipertahankan karena merupakan fenomena epidemiologis riil (*true historical peaks*) yang esensial untuk visualisasi kurva pandemi.
  * Nilai negatif akibat koreksi input sistem masa lalu di-*clipping* menjadi `0` agar tidak merusak akumulasi kasus.

---

## 5. INCONSISTENCIES FIXED (STANDARDISASI DATA)
1. **Nama Entitas Provinsi:**
   * Menyeragamkan penamaan provinsi dengan standar BPS / Kemendagri:
     * Menghilangkan *trailing/leading whitespaces* (`.str.strip()`).
     * Standardisasi penulisan `DKI Jakarta` dan `Daerah Istimewa Yogyakarta`.
2. **Standardisasi Format Tanggal:**
   * Seluruh tanggal dikonversi ke format standar ISO 8601 (`YYYY-MM-DD`).
3. **Penyelarasan Atribut Tambahan:**
   * Menambahkan atribut `year` (tahun: 2020, 2021, 2022).
   * Menambahkan atribut `month` (format YYYY-MM).
   * Menambahkan atribut `week` (format YYYY-Www) untuk agregasi periodik mingguan.
   * Menambahkan atribut `vaccination_rate` (%) dan `cases_decline` (%) untuk analisis komparatif vaksinasi.

---

## 6. DATA STATISTICS BEFORE-AFTER (PERBANDINGAN SEBELUM & SESUDAH)

| Metrik Evaluasi | Kondisi Mentah (Sebelum) | Kondisi Bersih (Sesudah) | Keterangan Perubahan |
| :--- | :--- | :--- | :--- |
| **Total Records (Baris)** | 31.822 baris | 30.926 baris | 896 baris agregat nasional dipisahkan khusus untuk analisis provinsi |
| **Total Kolom (Fitur)** | 38 kolom | 22 kolom relevan | Membuang kolom kosong/tidak relevan dan menyisipkan fitur rekayasa waktu |
| **Missing Values Total** | > 100.000 sel kosong | 0 sel kosong (100% lengkap) | Nilai hilang telah ditangani dengan eliminasi kolom kosong & imputasi rasional |
| **Duplikasi Data** | 0 duplikat identik | 0 duplikat identik | Integritas baris data terverifikasi unik per provinsi per tanggal |
| **Konsistensi Tipe Data** | Campuran string & numerik | Terstruktur tipe presisi | Tanggal berupa Datetime, kasus berupa Integer, rasio berupa Float |
| **Nilai Kasus Negatif** | Ditemukan anomali < 0 | Dieliminasi (Min: 0) | Nilai di-cap pada batas bawah non-negatif |

---
**Kesimpulan Tahap 2:**  
Dataset `data/data_cleaned.csv` telah melewati proses pembersihan data komprehensif, terbebas dari inkonsistensi tipe data, missing values, dan siap digunakan untuk tahapan Exploratory Data Analysis (EDA) serta visualisasi interaktif pada dashboard web.
