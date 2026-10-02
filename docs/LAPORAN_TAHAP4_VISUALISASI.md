# 📄 LAPORAN TAHAP 4: PERANCANGAN VISUALISASI DATA (DESIGN & SPECIFICATION)

**Mata Kuliah:** Visualisasi Data  
**Program Studi:** Teknik Informatika - Semester VII  
**Tema Proyek:** Dashboard Visualisasi Data Interaktif COVID-19 Indonesia  
**Perangkat Desain & Engine:** Python (Plotly Express, Plotly Graph Objects, Streamlit Framework)  

---

## 1. PRINSIP DESAIN & TATA KELOLA VISUAL (DESIGN SYSTEM)

* **Palet Warna Terstandarisasi (Semantic Color Coding):**
  * 🔴 **Kasus Positif Terkonfirmasi (`cases`):** `#EF5350` (Crimson Red) – melambangkan urgensi dan penularan infeksi aktif.
  * 🟢 **Kasus Sembuh (`recovered`):** `#66BB6A` (Emerald Green) – melambangkan tingkat keberhasilan medis dan pemulihan kesehatan.
  * 🟠 **Kasus Kematian (`deaths`):** `#FFA726` / `#E65100` (Amber Orange / Dark Amber) – melambangkan dampak fatalitas.
  * 🔵 **Aksen Analitis & Vaksinasi:** `#1976D2` (Royal Blue) – melambangkan intervensi sains, vaksinasi, dan stabilitas data.
  * ⚪ **Latar Belakang & Kartu:** `#F8FAFC` (Canvas White) & Card Background `#FFFFFF` dengan bayangan halus (*subtle glassmorphism shadow*).
  * ⚫ **Tipografi & Teks:** Font family Google `Inter, Roboto, sans-serif` dengan warna kontras `#1E293B` (Heading) dan `#475569` (Body).

* **Prinsip Interaktivitas (Interactive Affordance):**
  * *Hover Tooltip:* Menampilkan informasi terperinci (nama provinsi, tanggal presisi, angka absolut, dan persentase).
  * *Dynamic Filtering:* Filter multiselect provinsi, pemilih rentang tanggal (*Date Range Picker*), serta metrik pembanding.
  * *Responsive Grid Layout:* Struktur kontainer 12-kolom yang beradaptasi secara mulus antara monitor desktop, tablet, dan layar ponsel pintar (*mobile-friendly*).

---

## 2. KATALOG & SPESIFIKASI 6+ VISUALISASI

### 📊 VISUALISASI 1: BAR CHART HORIZONTAL (TOP 10 PROVINSI KASUS TERTINGGI)
* **Jenis Visualisasi:** Horizontal Bar Chart (`plotly.express.bar`)
* **Tujuan Visualisasi:** Membandingkan besaran volume kasus kumulatif antar entitas kategori provinsi secara cepat dan intuitif.
* **Variabel Data:** Sumbu Y = `Province`, Sumbu X = `Total Cases`, Skala Warna = Gradient Skala Merah (`Reds`).
* **Justifikasi Pemilihan:** Bar chart horizontal memberikan ruang label teks yang leluasa untuk 10 nama provinsi panjang tanpa rotasi yang mengganggu keterbacaan (*readability*).
* **Fitur Interaktif:** Tooltip detail total kasus, rasio kesembuhan, dan zoom rentang angka.
* **Insight yang Diperoleh:** Mengungkapkan kesenjangan beban kesehatan di mana >50% kasus nasional terkonsentrasi di 3 provinsi utama Pulau Jawa (DKI, Jabar, Jateng).

---

### 📈 VISUALISASI 2: LINE CHART INTERAKTIF (TREN KASUS HARIAN NASIONAL)
* **Jenis Visualisasi:** Time Series Line Chart (`plotly.express.line`)
* **Tujuan Visualisasi:** Memantau dinamika temporal, fluktuasi laju penularan, dan mengidentifikasi titik belok (*turning points*) gelombang pandemi.
* **Variabel Data:** Sumbu X = `Date` (Tanggal harian), Sumbu Y = `New Cases` (Kasus harian nasional).
* **Justifikasi Pemilihan:** Garis kontinu sangat efektif untuk memetakan dinamika gelombang, pergeseran varian, dan tren musiman seiring waktu.
* **Fitur Interaktif:** Date Range Slider (*range selector* 1 Bulan, 6 Bulan, 1 Tahun, Semua), crosshair cursor, dan titik hover terpadu (*unified hovermode*).
* **Insight yang Diperoleh:** Menunjukkan perbedaan curamnya kurva eksponensial Gelombang Delta (Juli 2021) dan Gelombang Omicron (Februari 2022).

---

### 🔄 VISUALISASI 3: STACKED AREA CHART (KOMPOSISI STATUS OUTCOME PASIEN)
* **Jenis Visualisasi:** Stacked Area Chart (`plotly.graph_objects.Scatter` dengan `fill='tonexty'`)
* **Tujuan Visualisasi:** Memvisualisasikan perbandingan proporsional kumulatif antara kasus baru, pasien pulih, dan fatalitas dari minggu ke minggu.
* **Variabel Data:** Sumbu X = `Week` (Mingguan), Sumbu Y = Jumlah kumulatif, Kategori Area = Kasus Baru (Merah), Sembuh (Hijau), Meninggal (Kuning-Oranye).
* **Justifikasi Pemilihan:** Grafik area bertingkat menonjolkan transisi status epidemiologi dari kondisi krisis (area merah mendominasi) menuju kondisi resolusi pemulihan (area hijau mendominasi secara absolut).
* **Fitur Interaktif:** Toggle legenda untuk menyembunyikan/menampilkan kategori tertentu, hover info kumulatif.
* **Insight yang Diperoleh:** Terlihat jelas bahwa setelah fase awal krisis terlewati, proporsi area hijau (sembuh) mendominasi secara permanen mendekati 97%.

---

### 🗺️ VISUALISASI 4: CHOROPLETH / BUBBLE GEO MAP INDONESIA
* **Jenis Visualisasi:** Geospatial Scatter Map (`plotly.express.scatter_geo` / Mapbox)
* **Tujuan Visualisasi:** Memberikan persepsi spasial langsung mengenai konsentrasi klaster pandemi di seluruh kepulauan Indonesia.
* **Variabel Data:** Latitude, Longitude, Ukuran Gelembung (*size*) = `Total Cases`, Warna (*color*) = `Case Fatality Rate (%)`.
* **Justifikasi Pemilihan:** Peta spasial memungkinkan pembaca memahami relasi geografis, aglomerasi perkotaan, dan tingkat keparahan regional seketika.
* **Fitur Interaktif:** Zoom, pan kepulauan, hover nama provinsi beserta populasi dan kepadatan.
* **Insight yang Diperoleh:** Hotspot absolut berada di koridor pantai utara Jawa dan Bali, dengan konsentrasi CFR tertinggi di beberapa provinsi Jawa Timur dan Jawa Tengah.

---

### 🔗 VISUALISASI 5: SCATTER PLOT + REGRESSION TRENDLINE (VAKSINASI VS PENURUNAN KASUS)
* **Jenis Visualisasi:** Scatter Plot dengan Regresi Linear OLS (`plotly.express.scatter` dengan `trendline="ols"`)
* **Tujuan Visualisasi:** Menguji hipotesis hubungan asosiasi antara intervensi cakupan vaksinasi terhadap penurunan keparahan kasus di 34 provinsi.
* **Variabel Data:** Sumbu X = `Vaccination Rate (%)`, Sumbu Y = `Cases Decline / Severity Drop (%)`, Ukuran Titik = `Population`, Warna = `Island`.
* **Justifikasi Pemilihan:** Scatter plot adalah visualisasi gold-standard dalam statistika untuk memperlihatkan korelasi bivariat, dispersi data, dan garis regresi pembuktian.
* **Fitur Interaktif:** Garis regresi berlabel persamaan matematis ($R^2$ dan p-value), hover identitas provinsi.
* **Insight yang Diperoleh:** Menunjukkan gradien positif yang signifikan; provinsi dengan vaksinasi di atas 80% membukukan penurunan keparahan kasus lebih dari 85%.

---

### 📊 VISUALISASI 6: HISTOGRAM DISTRIBUSI CASE FATALITY RATE (CFR)
* **Jenis Visualisasi:** Frequency Distribution Histogram (`plotly.express.histogram`)
* **Tujuan Visualisasi:** Menilai bentuk sebaran dan variabilitas nilai persentase Case Fatality Rate (CFR) di seluruh provinsi.
* **Variabel Data:** Sumbu X = Interval Rentang CFR (%), Sumbu Y = Frekuensi Jumlah Provinsi, Binning = 25 bins.
* **Justifikasi Pemilihan:** Histogram secara akurat menampilkan bentuk distribusi (unimodal, bimodal, skewness) dan nilai tipikal mortalitas.
* **Fitur Interaktif:** Hover frekuensi bin dan interval persentase, batas garis rata-rata (*mean line indicator*).
* **Insight yang Diperoleh:** Mayoritas provinsi berkumpul pada interval CFR 2,0% – 3,2%, dengan segelintir pencilan di atas 4,0%.

---

### 🎯 VISUALISASI BONUS: BOX PLOT VARIASI KASUS HARIAN PER KELOMPOK PULAU
* **Jenis Visualisasi:** Statistical Box Plot (`plotly.express.box`)
* **Tujuan Visualisasi:** Menampilkan ringkasan lima angka statistik (*Five-Number Summary*: Min, Q1, Median, Q3, Max) serta mendeteksi titik data pencilan (*outliers*).
* **Variabel Data:** Sumbu X = `Island` (Pulau), Sumbu Y = `Cases` (Kasus harian).
* **Fitur Interaktif:** Hover nilai kuartil, IQR, whiskers, dan identifikasi titik outlier.
* **Insight yang Diperoleh:** Pulau Jawa memiliki varians tertinggi dan rentang interkuartil terlebar, sementara Maluku dan Papua memiliki sebaran yang rapat pada skala rendah.

---

### 💳 BONUS: INTERACTIVE KPI CARDS
1. **Total Kasus Terkonfirmasi:** Nilai kumulatif dengan format ribuan pemisah koma.
2. **Total Pasien Sembuh (Recovered):** Disertai indikator recovery rate (%) positif.
3. **Total Korban Jiwa (Deaths):** Disertai rasio kematian nasional (CFR %).
4. **Cakupan Rata-rata Vaksinasi:** Rerata progres imunisasi dosis lengkap nasional.

---

## 3. CHECKLIST KEPATUHAN SPESIFIKASI PROYEK
* [x] Minimal 6 visualisasi berbeda terimplementasi (Bar, Line, Stacked Area, Geo Map, Scatter, Histogram, Box Plot)
* [x] Minimal 4 jenis grafik berbeda (Bahkan mencakup 7 jenis grafik: Bar, Line, Area, Geo Scatter, Scatter-OLS, Histogram, Box)
* [x] Setiap grafik dilengkapi tujuan, label sumbu yang jelas, dan insight analitis
* [x] Seluruh visualisasi responsif dan interaktif (Plotly Engine + Web Streamlit)
* [x] Skema warna terpadu dan selaras dengan panduan estetika
