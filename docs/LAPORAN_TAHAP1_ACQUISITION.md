# 📄 LAPORAN TAHAP 1: DATA ACQUISITION (PENGUMPULAN DATA)

**Mata Kuliah:** Visualisasi Data  
**Program Studi:** Teknik Informatika - Semester VII  
**Tema Proyek:** Dashboard Visualisasi Data Interaktif COVID-19 Indonesia  
**Penyusun:** Mahasiswa Teknik Informatika  

---

## 1. SUMBER DATA
* **URL / Repositori Data Utama:**  
  `https://raw.githubusercontent.com/rhmdziz/visualiasi-data-covid-19-indonesia/main/covid_19_indonesia_time_series_all.csv`  
  *(Data agregasi resmi harian dari KawalCOVID19 & Kementerian Kesehatan Republik Indonesia / Kaggle Repository)*
* **Sumber Data Sekunder (Vaksinasi):**  
  `https://vaksin.kemkes.go.id/` & *Our World in Data (OWID)* COVID-19 Dataset Indonesia
* **Tanggal Akses:** 2 Oktober 2026
* **Metode Akuisisi:** HTTP GET Request otomatis via Python (`urllib.request` / `pandas.read_csv`) disimpan ke `data/raw_data.csv`
* **Lisensi Data:** CC0: Public Domain / Open Data Kemenkes RI

---

## 2. DESKRIPSI DATASET
* **Nama Dataset:** COVID-19 Indonesia Time Series (Provincial & National Aggregation)
* **Periode Pencatatan:** 1 Maret 2020 s.d. 16 September 2022 (Mencakup rentang waktu 2,5 tahun / > 30 bulan)
* **Jumlah Records (Baris Data):** 31.822 baris data
* **Jumlah Kolom (Fitur):** 38 kolom pada dataset mentah
* **Cakupan Wilayah:** 34 Provinsi di seluruh Indonesia + 1 Agregat Nasional (Country Level)

---

## 3. STRUKTUR DATA UTAMA (DATA SCHEMA)

| Kolom | Tipe Data Awal | Deskripsi |
| :--- | :--- | :--- |
| `Date` | string (object) | Tanggal pencatatan kasus (format M/D/YYYY) |
| `Location ISO Code` | string (object) | Kode standar ISO 3166-2 wilayah (contoh: ID-JK, ID-JB, ID-JT) |
| `Location` | string (object) | Nama wilayah administratif (Provinsi atau "Indonesia") |
| `New Cases` | integer / float | Jumlah penambahan kasus positif terkonfirmasi harian |
| `New Deaths` | integer / float | Jumlah penambahan kasus kematian harian |
| `New Recovered` | integer / float | Jumlah penambahan pasien sembuh harian |
| `New Active Cases` | integer / float | Penambahan/perubahan kasus aktif harian (`New Cases - New Recovered - New Deaths`) |
| `Total Cases` | integer | Akumulasi total kasus konfirmasi sejak awal pandemi |
| `Total Deaths` | integer | Akumulasi total pasien meninggal sejak awal pandemi |
| `Total Recovered` | integer | Akumulasi total pasien sembuh sejak awal pandemi |
| `Total Active Cases` | integer | Akumulasi pasien yang masih menjalani perawatan/isolasi |
| `Location Level` | string (object) | Tingkatan data administrasi: `'Country'` (Nasional) atau `'Province'` (Provinsi) |
| `Province` | string (object) | Nama provinsi (bernilai NaN jika baris adalah level nasional) |
| `Island` | string (object) | Gugus kepulauan (Jawa, Sumatera, Kalimantan, Sulawesi, Bali, Nusa Tenggara, Maluku, Papua) |
| `Time Zone` | string (object) | Zona waktu wilayah (UTC+07:00, UTC+08:00, UTC+09:00) |
| `Population` | integer | Estimasi jumlah penduduk di wilayah terkait |
| `Population Density` | float | Kepadatan penduduk per kilometer persegi (jiwa/km²) |
| `Longitude` | float | Koordinat garis bujur wilayah |
| `Latitude` | float | Koordinat garis lintang wilayah |
| `Case Fatality Rate` | string (object) | Rasio kematian terhadap kasus positif dalam format persentase teks (e.g. `'2.54%'`) |
| `Case Recovered Rate` | string (object) | Rasio kesembuhan terhadap kasus positif dalam format persentase teks (e.g. `'95.12%'`) |
| `Growth Factor of New Cases` | float | Faktor laju pertumbuhan kasus harian |

---

## 4. KONDISI DATA AWAL SEBELUM PREPROCESSING
1. **Missing Values (Nilai Hilang):**
   * **Ya**, ditemukan pada atribut demografi kabupaten/kota (`City or Regency` 100% NaN pada level provinsi karena data agregat provinsi).
   * Pada baris agregat nasional (`Location Level == 'Country'`), kolom `Province` bernilai `NaN`.
   * Pada kolom `Growth Factor`, terdapat nilai missing di hari-hari awal pencatatan sebelum ada data pembanding hari sebelumnya.

2. **Duplikasi Data:**
   * Tidak ditemukan duplikasi baris mentah persis sama (0 duplikat absolut), namun terdapat pencampuran antara level agregat `'Country'` (Nasional) dan `'Province'` yang berisiko menyebabkan *double-counting* jika langsung dijumlahkan.

3. **Anomali & Format Inkonsistensi:**
   * **Format Tanggal:** Kolom `Date` masih berstatus string campuran format Amerika Serikat (`M/D/YYYY`), belum berstandar ISO 8601 (`YYYY-MM-DD`).
   * **Tipe Data Persentase:** Kolom `Case Fatality Rate` dan `Case Recovered Rate` bertipe `object` karena memiliki simbol `%`.
   * **Fluktuasi Nilai:** Terdapat pencatatan kasus baru nol (`0`) dan *negative active cases* pada hari-hari ketika angka kesembuhan lebih tinggi dibandingkan kasus baru harian.

---

## 5. RENCANA AKSI TAHAP PEMBERSIHAN DATA (DATA CLEANING)
1. Memisahkan atau memfilter level data agar agregasi analitis provinsi dan nasional dilakukan secara presisi tanpa redundansi.
2. Mengonversi kolom `Date` menjadi tipe data `datetime64[ns]`.
3. Mengonversi nilai rasio teks persentase menjadi `float` numerik standar.
4. Menambahkan atribut waktu turunan: `Year`, `Month`, `Week`, `YearMonth` untuk memudahkan agregasi mingguan dan bulanan.
5. Mengintegrasikan atribut metrik vaksinasi (`vaccination_rate`) untuk analisis hubungan vaksinasi dan mitigasi pandemi.
6. Menyimpan hasil olahan ke dalam `data/data_cleaned.csv`.
