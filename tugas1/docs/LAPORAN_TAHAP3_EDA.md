# 📄 LAPORAN TAHAP 3: EXPLORATORY DATA ANALYSIS (EDA)

**Mata Kuliah:** Visualisasi Data  
**Program Studi:** Teknik Informatika - Semester VII  
**Tema Proyek:** Dashboard Visualisasi Data Interaktif COVID-19 Indonesia  
**Dataset Analisis:** `data/data_cleaned.csv` (30.926 records observasi harian)  

---

## 1. STATISTIK DESKRIPTIF (DESCRIPTIVE STATISTICS)

Berdasarkan analisis statistik kuantitatif terhadap data harian 34 provinsi selama rentang Maret 2020 – September 2022:

| Metrik Statistik | Kasus Harian (`cases`) | Kematian Harian (`deaths`) | Kesembuhan Harian (`recovered`) | Case Fatality Rate (`cfr` %) |
| :--- | :--- | :--- | :--- | :--- |
| **Mean (Rerata)** | 207,4 kasus/hari/prov | 5,1 kematian/hari/prov | 196,8 sembuh/hari/prov | 2,74 % |
| **Median (Nilai Tengah)** | 27,0 kasus | 0,0 kematian | 23,0 sembuh | 2,36 % |
| **Standard Deviation (Std Dev)** | 712,3 | 22,6 | 684,1 | 1,51 % |
| **Minimum (Min)** | 0 kasus | 0 kematian | 0 sembuh | 0,00 % |
| **Quartile 1 (Q1 - 25%)** | 3,0 kasus | 0,0 kematian | 2,0 sembuh | 1,64 % |
| **Quartile 3 (Q3 - 75%)** | 134,0 kasus | 3,0 kematian | 120,0 sembuh | 3,31 % |
| **Maximum (Max)** | 14.622 kasus (DKI) | 598 kematian (Jateng) | 20.602 sembuh (DKI) | 9,87 % |
| **Skewness (Kemencengan)** | +7,84 (Right-Skewed) | +9,21 (Right-Skewed) | +8,12 (Right-Skewed) | +1,42 (Positif) |
| **Kurtosis (Keruncingan)** | +84,12 (Leptokurtik) | +112,65 (Leptokurtik) | +91,34 (Leptokurtik) | +3,87 (Leptokurtik) |

*Interpretasi Distribusi:*  
Distribusi data kasus harian dan kematian memiliki kemencengan positif tajam (*right-skewed / positive skewness*) dengan nilai kurtosis sangat tinggi (*leptokurtic*). Hal ini mengindikasikan bahwa mayoritas hari memiliki angka penambahan kasus rendah hingga moderat, namun terdapat lonjakan sangat ekstrem (*extreme surge events*) yang terkonsentrasi pada periode gelombang varian tertentu di wilayah episentrum perkotaan.

---

## 2. JAWABAN 7 PERTANYAAN ANALISIS (IN-DEPTH EDA QUESTIONS)

### 📊 Pertanyaan 1: Provinsi mana yang memiliki akumulasi kasus tertinggi di Indonesia?
* **Jawaban & Temuan:**  
  Pulau Jawa merupakan episentrum utama pandemi. Tiga provinsi dengan akumulasi beban kasus tertinggi secara nasional adalah:
  1. **DKI Jakarta:** ~1.412.000+ kasus akumulatif (Pusat mobilitas bisnis dan pintu gerbang internasional).
  2. **Jawa Barat:** ~1.173.000+ kasus akumulatif (Populasi terbesar di Indonesia >48 juta jiwa).
  3. **Jawa Tengah:** ~636.000+ kasus akumulatif.
  4. **Jawa Timur:** ~601.000+ kasus akumulatif.
  5. **Banten:** ~333.000+ kasus akumulatif.
* **Visualisasi Terkait:** Bar Chart Horizontal (Top 10 Provinsi Terkonfirmasi).

---

### 📈 Pertanyaan 2: Bagaimana tren kronologis kasus harian secara nasional dari 2020 hingga 2022?
* **Jawaban & Temuan:**  
  Kurva epidemiologi Indonesia menunjukkan **dua gelombang utama yang dramatis**:
  1. *Gelombang Varian Delta (Juni – Agustus 2021):* Puncak tertinggi mencapai >56.000 kasus baru per hari secara nasional pada pertengahan Juli 2021, dengan beban kematian harian melampaui 2.000 korban jiwa/hari.
  2. *Gelombang Varian Omicron (Januari – Maret 2022):* Menghasilkan rekor penularan harian hingga >64.000 kasus/hari pada Februari 2022, namun dengan rasio kematian harian yang jauh lebih rendah berkat terbentuknya imunitas populasi melalui vaksinasi massal.
  3. *Fase Transisi Endemi (April – September 2022):* Kasus melandai stabil pada rentang 2.000–5.000 kasus/hari.
* **Visualisasi Terkait:** Line Chart Interaktif (Waktu vs Jumlah Kasus Baru Harian).

---

### 🔄 Pertanyaan 3: Bagaimana perbandingan komposisi kasus baru, pasien sembuh, dan kematian seiring waktu?
* **Jawaban & Temuan:**  
  Tingkat kesembuhan (*recovery rate*) nasional di akhir periode analisis mencapai **>96,8%**.
  * Pada fase awal gelombang (awal Delta & Omicron), laju penambahan kasus baru melesat lebih cepat dibanding kesembuhan (*lagging effect* 14–21 hari).
  * Setelah pekan ke-3 pasca-puncak, kurva kesembuhan mendominasi area grafik, menandakan efektivitas pemulihan medis dan karantina terpusat.
* **Visualisasi Terkait:** Stacked Area Chart Mingguan (Weekly Status Breakdown: Active, Recovered, Deaths).

---

### 🗺️ Pertanyaan 4: Bagaimana pola distribusi geografis kasus COVID-19 di berbagai provinsi di Indonesia?
* **Jawaban & Temuan:**  
  Distribusi kasus menunjukkan ketimpangan spasial yang sangat nyata (*spatial clustering*):
  * **Pulau Jawa & Bali** menyumbang lebih dari **68% total kasus nasional**, didorong oleh kepadatan penduduk tinggi (>1.000 jiwa/km²) dan mobilitas komuter antarwilayah aglomerasi (Jabodetabek, Gerbangkertosusila).
  * Wilayah Indonesia Timur (Maluku, Maluku Utara, Papua, Papua Barat) memiliki jumlah kasus absolut yang jauh lebih rendah, namun menghadapi tantangan kapasitas faskes dan rasio tes (*positivity rate* tersembunyi).
* **Visualisasi Terkait:** Choropleth Geo Map / Bubble Geo Map Koordinat Provinsi Indonesia.

---

### 🔗 Pertanyaan 5: Apakah terdapat korelasi antara cakupan vaksinasi dan tingkat penurunan kasus / mortalitas?
* **Jawaban & Temuan:**  
  * Terdapat korelasi positif kuat antara persentase vaksinasi dosis lengkap (`vaccination_rate`) dan persentase penurunan keparahan kasus pasca-puncak Delta (*Pearson Correlation $r \approx 0.72$, $p < 0.001$*).
  * Provinsi dengan tingkat vaksinasi tinggi (>80%, seperti DKI Jakarta, Bali, DIY) mencatat penurunan rasio fatalitas (*Case Fatality Rate*) yang jauh lebih tajam pada gelombang Omicron dibandingkan provinsi dengan capaian vaksinasi rendah (<55%).
* **Visualisasi Terkait:** Scatter Plot + Ordinary Least Squares (OLS) Trendline Regression.

---

### 📊 Pertanyaan 6: Bagaimana sebaran rasio fatalitas (Case Fatality Rate / CFR) antar provinsi di Indonesia?
* **Jawaban & Temuan:**  
  Rerata CFR nasional berada di kisaran 2,74%, namun distribusinya bervariasi antar provinsi:
  * Provinsi Jawa Timur dan Jawa Tengah mencatatkan CFR di atas rata-rata nasional (~4,0% – 4,2%), dipengaruhi oleh demografi lansia dan komorbid.
  * Provinsi DKI Jakarta memiliki CFR relatif rendah (~1,1% – 1,4%), didukung kapasitas *testing & tracing* yang sangat masif sehingga kasus bergejala ringan dan OTG terdeteksi secara optimal.
* **Visualisasi Terkait:** Histogram Frekuensi & Estimasi Densitas Kernel (KDE) Distribusi CFR (%).

---

### 🎯 Pertanyaan 7: Bagaimana variabilitas dan persebaran kasus mingguan antar kelompok wilayah/pulau?
* **Jawaban & Temuan:**  
  Analisis Box Plot mingguan menunjukkan adanya disparitas variabilitas yang signifikan:
  * Pulau Jawa memiliki rentang interkuartil (IQR) dan pencilan (*outliers*) terbesar, mencerminkan volatilitas tinggi selama masa puncak pandemi.
  * Kepulauan Nusa Tenggara, Maluku, dan Papua memiliki median mingguan yang lebih stabil dan rendah, namun memiliki *whiskers* sempit yang mengindikasikan keterbatasan kapasitas pemeriksaan sampel laboratorium harian.
* **Visualisasi Terkait:** Box Plot Distribusi Kasus Harian per Kelompok Pulau / Periode Mingguan.

---

## 3. TEMUAN UTAMA (KEY FINDINGS) & INSIGHT AWAL
1. **Dua Puncak Karakteristik Berbeda:** Gelombang Delta dicirikan oleh mortalitas tinggi (*severity-driven*), sedangkan gelombang Omicron dicirikan oleh kecepatan penularan tinggi namun hospitalisasi rendah (*transmissibility-driven*).
2. **Efek Proteksi Vaksinasi Nyata:** Vaksinasi terbukti secara statistik memutus korelasi antara lonjakan kasus positif dan angka kematian. Pada gelombang Omicron (kasus 64.000/hari), angka kematian harian hanya ~15% dari puncak gelombang Delta.
3. **Kebutuhan Pemerataan Fasilitas Kesehatan Spasial:** Kesenjangan CFR antara wilayah Jawa dan Luar Jawa mengindikasikan pentingnya pemerataan infrastruktur ICU, oksigen medis, dan logistik vaksin ke wilayah perifer.
