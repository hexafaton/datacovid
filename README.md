# 🦠 Dashboard Visualisasi Data Interaktif COVID-19 Indonesia
### Tugas Kuliah Visualisasi Data — Program Studi Teknik Informatika Semester VII

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License: CC0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg?style=for-the-badge)](https://creativecommons.org/publicdomain/zero/1.0/)

---

## 📌 1. Ringkasan Proyek
Proyek ini merupakan implementasi menyeluruh untuk tugas akhir mata kuliah **Visualisasi Data** pada jenjang S1 Teknik Informatika (Semester VII). Dashboard ini menyajikan visualisasi data interaktif, analitis, dan mendalam terkait dinamika pandemi COVID-19 di 34 provinsi Indonesia sepanjang kurun waktu Maret 2020 hingga September 2022 (>30.000 records).

Dashboard dibangun dengan prinsip **User Experience (UX) modern**, tipografi berbasis Google Font *Plus Jakarta Sans*, tata letak responsif, serta palet warna semantik standar epidemiologi.

---

## 🚀 2. Fitur Utama Dashboard
1. **Interactive KPI Metric Cards:** Menampilkan metrik utama (Total Kasus, Pasien Sembuh, Kematian, dan Rata-rata Vaksinasi Dosis Lengkap) secara dinamis sesuai filter aktif.
2. **6+ Visualisasi Interaktif (7 Jenis Chart Berbeda):**
   * 🗺️ **Visualisasi 1 (Geospatial Map):** Peta persebaran gelembung koordinat provinsi (Total Kasus & Case Fatality Rate).
   * 📊 **Visualisasi 2 (Horizontal Bar Chart):** Peringkat Top 10 Provinsi Kasus COVID-19 Tertinggi.
   * 📈 **Visualisasi 3 (Time Series Line Chart):** Tren kronologis harian nasional dengan *7-Day Moving Average* dan *Range Selector*.
   * 🔄 **Visualisasi 4 (Stacked Area Chart):** Komposisi status pasien mingguan (Kasus Baru vs Sembuh vs Fatalitas).
   * 🔗 **Visualisasi 5 (Scatter Plot + OLS Regression Line):** Analisis korelasi bivariat cakupan vaksinasi vs persentase reduksi keparahan kasus.
   * 📊 **Visualisasi 6 (Histogram Distribusi):** Sebaran Case Fatality Rate (CFR %) antarprovinsi dengan garis indikator mean nasional.
   * 📦 **Visualisasi Bonus (Statistical Box Plot):** Variansi dan deteksi pencilan (*outliers*) kasus harian per gugus pulau (skala logaritmik).
3. **Filter Interaktif Multi-Dimensi (Sidebar):**
   * Filter Gugus Pulau / Wilayah Kepulauan.
   * Multiselect Provinsi (disertai tombol cepat *Pilih Semua* dan *Top 5 Kasus*).
   * Date Range Picker (Pemilih Rentang Tanggal).
   * Pilihan Penghalus Tren (*Moving Average Window*: Harian, 7 Hari, 14 Hari).
4. **Data Explorer & Ekspor CSV:** Tabel interaktif dengan fasilitas pencarian teks dan tombol download CSV terfilter.
5. **Dokumentasi Terpadu (In-App Docs Viewer):** Akses langsung membaca 4 laporan tahapan proyek dari dalam web.

---

## 📁 3. Struktur Direktori Proyek
```text
tugasbunirma/
├── data/
│   ├── raw_data.csv                   # Data mentah hasil scraping (31.822 baris x 38 kolom)
│   ├── data_cleaned.csv               # Data bersih siap pakai (30.893 baris x 25 kolom)
│   └── data_sources.txt               # Dokumentasi lisensi & referensi sumber data
├── notebooks/
│   ├── 01_data_acquisition.ipynb      # Notebook Tahap 1: Pengumpulan & inspeksi data mentah
│   ├── 02_data_cleaning.ipynb         # Notebook Tahap 2: Pembersihan, imputasi, & feature engineering
│   ├── 03_eda.ipynb                   # Notebook Tahap 3: Exploratory Data Analysis (7 pertanyaan)
│   └── 04_visualization.ipynb         # Notebook Tahap 4: Prototipe 6+ visualisasi Plotly
├── docs/
│   ├── LAPORAN_TAHAP1_ACQUISITION.md  # Laporan resmi Tahap 1 (Akuisisi Data)
│   ├── LAPORAN_TAHAP2_CLEANING.md     # Laporan resmi Tahap 2 (Pembersihan Data)
│   ├── LAPORAN_TAHAP3_EDA.md          # Laporan resmi Tahap 3 (Exploratory Data Analysis)
│   └── LAPORAN_TAHAP4_VISUALISASI.md  # Laporan resmi Tahap 4 (Perancangan Visualisasi)
├── scripts/
│   └── acquire_and_clean.py           # Pipeline otomatis ETL (Extract, Transform, Load)
├── app.py                             # Kode utama aplikasi web Streamlit Dashboard
├── requirements.txt                   # Daftar dependensi modul Python
├── README.md                          # Dokumentasi utama proyek
└── .gitignore                         # Konfigurasi file yang diabaikan Git
```

---

## 💻 4. Panduan Menjalankan Proyek Secara Lokal

### Prasyarat
* Python versi 3.10 atau yang lebih baru.
* Browser web modern (Chrome, Edge, Firefox, Safari).

### Langkah Instalasi
1. **Clone atau Masuk ke Direktori Proyek:**
   ```bash
   cd c:/Users/aang/tugasbunirma
   ```

2. **Instal Seluruh Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Opsional) Jalankan Pipeline ETL:**
   Jika ingin mengunduh ulang dan memperbarui dataset mentah:
   ```bash
   python scripts/acquire_and_clean.py
   ```

4. **Jalankan Aplikasi Web Streamlit:**
   ```bash
   streamlit run app.py
   ```

5. Buka peramban di alamat: `http://localhost:8501`.

---

## ☁️ 5. Panduan Deployment ke Streamlit Cloud (Gratis & Shareable)
1. **Inisialisasi Git dan Push ke GitHub:**
   ```bash
   git init
   git add .
   git commit -m "feat: complete COVID-19 Indonesia interactive visualization dashboard"
   git branch -M main
   git remote add origin https://github.com/<username-anda>/<nama-repo>.git
   git push -u origin main
   ```
2. Buka [https://share.streamlit.io/](https://share.streamlit.io/) dan login menggunakan akun GitHub Anda.
3. Klik tombol **"New app"**.
4. Pilih repository yang baru saja di-push, branch `main`, dan set file path ke `app.py`.
5. Klik **"Deploy!"**. Dashboard akan aktif secara publik dalam hitungan menit.

---

## 📊 6. Sumber Data & Lisensi
* **Dataset Kasus Harian COVID-19:** Satgas Penanganan COVID-19 RI, KawalCOVID19, & Kemenkes RI via Kaggle/GitHub Repository Hendratno (Lisensi CC0 Public Domain).
* **Dataset Vaksinasi & Demografi:** Dashboard Vaksinasi Kementerian Kesehatan RI (`https://vaksin.kemkes.go.id/`) & *Our World in Data (OWID)* COVID-19 Data.
* **Lisensi Kode:** Proyek ini dilisensikan di bawah ketentuan MIT License untuk tujuan pendidikan dan akademik.
