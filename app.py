import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# ==============================================================================
# 1. PAGE CONFIGURATION & METADATA
# ==============================================================================
st.set_page_config(
    page_title="Dashboard COVID-19 Indonesia | Teknik Informatika",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. CUSTOM CSS STYLING (MODERN & PREMIUM AESTHETICS)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1350px;
    }
    
    /* Hero Banner Header */
    .hero-banner {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 50%, #1E3A8A 100%);
        color: white;
        padding: 2.2rem 2.5rem;
        border-radius: 18px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        border-radius: 50px;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 0.8rem;
        color: #93C5FD;
        border: 1px solid rgba(147, 197, 253, 0.3);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #CBD5E1;
        max-width: 800px;
        line-height: 1.5;
        margin: 0;
    }

    /* KPI Cards Styling */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.2rem;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.4rem 1.2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
        border: 1px solid #E2E8F0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
    }
    .kpi-strip {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
    }
    .kpi-cases .kpi-strip { background: #EF5350; }
    .kpi-recovered .kpi-strip { background: #10B981; }
    .kpi-deaths .kpi-strip { background: #F59E0B; }
    .kpi-vaccine .kpi-strip { background: #3B82F6; }
    .kpi-active .kpi-strip { background: #8B5CF6; }

    .kpi-label {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #64748B;
        margin-bottom: 0.4rem;
    }
    .kpi-value {
        font-size: 1.9rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
        margin-bottom: 0.3rem;
    }
    .kpi-sub {
        font-size: 0.82rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    .sub-cases { color: #EF4444; }
    .sub-recovered { color: #10B981; }
    .sub-deaths { color: #D97706; }
    .sub-vaccine { color: #2563EB; }
    .sub-active { color: #7C3AED; }

    /* Custom Section Headers */
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-desc {
        font-size: 0.92rem;
        color: #64748B;
        margin-bottom: 1.2rem;
    }

    /* Analysis Callout Card */
    .insight-card {
        background: #F8FAFC;
        border-left: 4px solid #3B82F6;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-top: 0.8rem;
        margin-bottom: 1.5rem;
        font-size: 0.92rem;
        color: #334155;
        line-height: 1.5;
    }
    .insight-title {
        font-weight: 700;
        color: #1E40AF;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    /* Sidebar info box */
    .sidebar-info {
        background: #F1F5F9;
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        border: 1px solid #CBD5E1;
        font-size: 0.85rem;
        color: #334155;
    }

    /* Footer */
    .footer-box {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem;
        margin-top: 3rem;
        border-top: 1px solid #E2E8F0;
        color: #64748B;
        font-size: 0.88rem;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. DATA LOADING & CACHING
# ==============================================================================
@st.cache_data
def load_dataset():
    data_path = os.path.join("data", "data_cleaned.csv")
    if not os.path.exists(data_path):
        # Fallback path jika dieksekusi dari subfolder
        data_path = "data_cleaned.csv"
    
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    return df

df_full = load_dataset()

# ==============================================================================
# 4. SIDEBAR CONFIGURATION & FILTER CONTROLS
# ==============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/isometric/96/coronavirus.png", width=72)
    st.title("🎛️ Filter Analisis")
    st.caption("Eksplorasi Dinamika Pandemi COVID-19 Indonesia")
    
    st.divider()
    
    # Filter Gugus Kepulauan
    islands_list = sorted(df_full['island'].unique())
    selected_islands = st.multiselect(
        "Pilih Gugus Pulau/Wilayah:",
        options=islands_list,
        default=islands_list,
        help="Saring data berdasarkan kelompok kepulauan utama."
    )
    
    # Filter Provinsi berdasarkan Pulau yang dipilih
    available_provinces = sorted(df_full[df_full['island'].isin(selected_islands)]['province'].unique())
    
    # Opsi cepat pilih semua / top 5
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        select_all_prov = st.button("Pilih Semua", use_container_width=True)
    with col_f2:
        select_top5_prov = st.button("Top 5 Kasus", use_container_width=True)
    
    if select_all_prov:
        st.session_state['selected_provinces'] = available_provinces
    elif select_top5_prov:
        top5_list = df_full.groupby('province')['cases'].sum().nlargest(5).index.tolist()
        st.session_state['selected_provinces'] = [p for p in top5_list if p in available_provinces]
    
    if 'selected_provinces' not in st.session_state or not st.session_state['selected_provinces']:
        st.session_state['selected_provinces'] = available_provinces

    selected_provinces = st.multiselect(
        "Pilih Provinsi:",
        options=available_provinces,
        default=st.session_state['selected_provinces'],
        help="Pilih satu atau beberapa provinsi untuk analisis mendalam."
    )
    
    # Filter Rentang Tanggal
    min_date = df_full['date'].min().date()
    max_date = df_full['date'].max().date()
    
    date_range = st.date_input(
        "Rentang Waktu Observasi:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Tentukan batas awal dan akhir tanggal analisis."
    )
    
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    # Smoothing Filter (Moving Average)
    ma_window = st.selectbox(
        "Moving Average (Penghalusan Tren):",
        options=[1, 7, 14],
        format_func=lambda x: "Data Harian Murni" if x == 1 else f"Rata-rata Bergerak {x} Hari (Rolling MA)",
        index=1,
        help="Gunakan 7-Day MA untuk mereduksi volatilitas pencatatan akhir pekan."
    )
    
    st.divider()
    
    # Info Dataset di Sidebar
    st.markdown(f"""
    <div class="sidebar-info">
        <b>📋 Informasi Dataset Bersih:</b><br>
        • Total Observasi: <b>{len(df_full):,} records</b><br>
        • Rentang: <b>{min_date.strftime('%d %b %Y')} - {max_date.strftime('%d %b %Y')}</b><br>
        • Entitas: <b>{df_full['province'].nunique()} Provinsi</b><br>
        • Sumber: <b>Kemenkes RI & KawalCOVID19</b>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("Tugas Kuliah Visualisasi Data - TI Semester VII")

# ==============================================================================
# 5. DATA FILTERING PIPELINE
# ==============================================================================
if not selected_provinces:
    selected_provinces = available_provinces

df_filtered = df_full[
    (df_full['province'].isin(selected_provinces)) &
    (df_full['date'] >= pd.to_datetime(start_date)) &
    (df_full['date'] <= pd.to_datetime(end_date))
].copy()

# ==============================================================================
# 6. HERO HEADER BANNER
# ==============================================================================
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">🎓 TUGAS AKHIR VISUALISASI DATA • TEKNIK INFORMATIKA</div>
    <div class="hero-title">Dashboard Visualisasi Interaktif COVID-19 Indonesia</div>
    <p class="hero-subtitle">
        Analisis komprehensif dinamika penularan, disparitas spasial antarprovinsi, komposisi kesembuhan, 
        serta dampak capaian vaksinasi massal terhadap penurunan keparahan pandemi di Indonesia.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 7. SUMMARY KPI METRIC CARDS
# ==============================================================================
total_cases = df_filtered['cases'].sum()
total_deaths = df_filtered['deaths'].sum()
total_recovered = df_filtered['recovered'].sum()
avg_vax = df_filtered.groupby('province')['vaccination_rate'].first().mean()
cfr_val = (total_deaths / total_cases * 100) if total_cases > 0 else 0.0
recovery_val = (total_recovered / total_cases * 100) if total_cases > 0 else 0.0

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card kpi-cases">
        <div class="kpi-strip"></div>
        <div class="kpi-label">Total Terkonfirmasi</div>
        <div class="kpi-value">{total_cases:,}</div>
        <div class="kpi-sub sub-cases">🔴 Kasus Positif Baru</div>
    </div>
    <div class="kpi-card kpi-recovered">
        <div class="kpi-strip"></div>
        <div class="kpi-label">Total Pasien Sembuh</div>
        <div class="kpi-value">{total_recovered:,}</div>
        <div class="kpi-sub sub-recovered">🟢 Tingkat Sembuh: {recovery_val:.1f}%</div>
    </div>
    <div class="kpi-card kpi-deaths">
        <div class="kpi-strip"></div>
        <div class="kpi-label">Total Meninggal Dunia</div>
        <div class="kpi-value">{total_deaths:,}</div>
        <div class="kpi-sub sub-deaths">🟠 CFR: {cfr_val:.2f}%</div>
    </div>
    <div class="kpi-card kpi-vaccine">
        <div class="kpi-strip"></div>
        <div class="kpi-label">Rata-rata Vaksinasi</div>
        <div class="kpi-value">{avg_vax:.1f}%</div>
        <div class="kpi-sub sub-vaccine">🔵 Capaian Dosis Lengkap</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 8. TABBED NAVIGATION WORKFLOW
# ==============================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Ringkasan Nasional & Peta",
    "📈 Tren Temporal & Komposisi",
    "💉 Vaksinasi vs Keparahan",
    "📦 Variabilitas Spasial (Box Plot)",
    "📋 Eksplorasi Dataset",
    "📑 Dokumentasi & Laporan Tahap"
])

# ------------------------------------------------------------------------------
# TAB 1: RINGKASAN NASIONAL & PETA SPASIAL
# ------------------------------------------------------------------------------
with tab1:
    col_t1_left, col_t1_right = st.columns([1.1, 0.9])
    
    with col_t1_left:
        st.markdown('<div class="section-title">🗺️ Visualisasi 4: Distribusi Geospasial Kasus & CFR</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-desc">Peta gelembung koordinat provinsi: Ukuran = Total Kasus Terkonfirmasi, Warna = Case Fatality Rate (CFR %)</div>', unsafe_allow_html=True)
        
        prov_map_data = df_filtered.groupby('province').agg({
            'total_cases': 'max',
            'cfr': 'last',
            'latitude': 'first',
            'longitude': 'first',
            'island': 'first',
            'population': 'first'
        }).reset_index()
        
        fig_map = px.scatter_geo(
            prov_map_data,
            lat='latitude',
            lon='longitude',
            size='total_cases',
            color='cfr',
            hover_name='province',
            hover_data={
                'total_cases': ':,',
                'cfr': ':.2f%',
                'island': True,
                'population': ':,',
                'latitude': False,
                'longitude': False
            },
            color_continuous_scale='Reds',
            labels={'cfr': 'CFR (%)', 'total_cases': 'Total Kasus'},
            projection='natural earth'
        )
        fig_map.update_geos(
            center=dict(lat=-2.5, lon=118.0),
            lataxis_range=[-11.5, 6.5],
            lonaxis_range=[94.0, 142.0],
            visible=False,
            showcountries=True,
            countrycolor="#CBD5E1",
            showland=True,
            landcolor="#F1F5F9",
            showocean=True,
            oceancolor="#E0F2FE"
        )
        fig_map.update_layout(
            height=460,
            margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_colorbar=dict(title="CFR (%)", thickness=15, len=0.7)
        )
        st.plotly_chart(fig_map, use_container_width=True)
        
        st.markdown("""
        <div class="insight-card">
            <div class="insight-title">💡 Insight Geospasial:</div>
            Konsentrasi beban kasus pandemi terakumulasi sangat padat di sepanjang koridor metropolitan Pulau Jawa. 
            Meskipun wilayah luar Jawa memiliki volume kasus lebih sedikit, disparitas CFR terlihat nyata pada beberapa wilayah kepulauan karena kendala distribusi logistik medis dan fasilitas penanganan intensif (ICU).
        </div>
        """, unsafe_allow_html=True)
        
    with col_t1_right:
        st.markdown('<div class="section-title">📊 Visualisasi 1: Kasus COVID-19 Top Provinsi</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-desc">Peringkat provinsi dengan akumulasi penambahan kasus tertinggi pada filter aktif.</div>', unsafe_allow_html=True)
        
        top_n = st.slider("Jumlah Provinsi Tampil:", min_value=5, max_value=15, value=10, key="top_n_slider")
        top_prov = df_filtered.groupby('province')['cases'].sum().nlargest(top_n).reset_index()
        top_prov = top_prov.sort_values(by='cases', ascending=True)
        
        fig_bar = px.bar(
            top_prov,
            x='cases',
            y='province',
            orientation='h',
            labels={'cases': 'Jumlah Kasus', 'province': 'Provinsi'},
            color='cases',
            color_continuous_scale='Reds',
            text='cases',
            template='plotly_white'
        )
        fig_bar.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_bar.update_layout(
            height=460,
            margin=dict(l=10, r=30, t=10, b=10),
            coloraxis_showscale=False,
            xaxis=dict(showgrid=True, gridcolor='#F1F5F9')
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("""
        <div class="insight-card">
            <div class="insight-title">💡 Insight Beban Wilayah:</div>
            DKI Jakarta dan Jawa Barat secara konsisten menempati peringkat teratas penularan karena merupakan hub transportasi nasional dengan mobilitas komuter harian tertinggi di Asia Tenggara.
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 2: TREN TEMPORAL & KOMPOSISI STATUS
# ------------------------------------------------------------------------------
with tab2:
    st.markdown('<div class="section-title">📈 Visualisasi 2: Tren Kasus Harian COVID-19 (Time Series)</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Dinamika penularan harian dengan garis penghalus moving average dan pemilih rentang waktu interaktif.</div>', unsafe_allow_html=True)
    
    daily_ts = df_filtered.groupby('date').agg({'cases': 'sum', 'deaths': 'sum', 'recovered': 'sum'}).reset_index()
    if ma_window > 1:
        daily_ts['cases_ma'] = daily_ts['cases'].rolling(window=ma_window, min_periods=1).mean()
    
    fig_line = go.Figure()
    # Bar harian
    fig_line.add_trace(go.Bar(
        x=daily_ts['date'],
        y=daily_ts['cases'],
        name='Kasus Harian Riil',
        marker=dict(color='rgba(239, 83, 80, 0.35)'),
        hovertemplate='Tanggal: %{x|%d %b %Y}<br>Kasus Baru: %{y:,}<extra></extra>'
    ))
    # Garis tren
    if ma_window > 1:
        fig_line.add_trace(go.Scatter(
            x=daily_ts['date'],
            y=daily_ts['cases_ma'],
            name=f'Moving Average {ma_window} Hari',
            mode='lines',
            line=dict(color='#DC2626', width=2.5),
            hovertemplate='Tanggal: %{x|%d %b %Y}<br>MA Kasus: %{y:,.1f}<extra></extra>'
        ))
    else:
        fig_line.add_trace(go.Scatter(
            x=daily_ts['date'],
            y=daily_ts['cases'],
            name='Garis Tren Kasus',
            mode='lines',
            line=dict(color='#EF5350', width=2),
            hovertemplate='Tanggal: %{x|%d %b %Y}<br>Kasus Baru: %{y:,}<extra></extra>'
        ))
        
    fig_line.update_layout(
        template='plotly_white',
        height=450,
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(
            rangeslider=dict(visible=True, thickness=0.08),
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1 Bulan", step="month", stepmode="backward"),
                    dict(count=6, label="6 Bulan", step="month", stepmode="backward"),
                    dict(count=1, label="1 Tahun", step="year", stepmode="backward"),
                    dict(step="all", label="Semua Data")
                ])
            )
        ),
        yaxis=dict(title="Jumlah Kasus Baru")
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.divider()
    
    st.markdown('<div class="section-title">🔄 Visualisasi 3: Komposisi Status Outcome Pasien (Per Minggu)</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Grafik area bertumpuk mingguan memperlihatkan proporsi Kasus Baru vs Pasien Sembuh vs Kematian.</div>', unsafe_allow_html=True)
    
    weekly_ts = df_filtered.groupby('week').agg({
        'cases': 'sum',
        'recovered': 'sum',
        'deaths': 'sum',
        'date': 'first'
    }).reset_index().sort_values('date')
    
    fig_area = go.Figure()
    fig_area.add_trace(go.Scatter(
        x=weekly_ts['week'],
        y=weekly_ts['deaths'],
        name='Kematian',
        mode='lines',
        line=dict(width=0.5, color='#F59E0B'),
        stackgroup='one',
        fillcolor='rgba(245, 158, 11, 0.75)'
    ))
    fig_area.add_trace(go.Scatter(
        x=weekly_ts['week'],
        y=weekly_ts['recovered'],
        name='Pasien Sembuh',
        mode='lines',
        line=dict(width=0.5, color='#10B981'),
        stackgroup='one',
        fillcolor='rgba(16, 185, 129, 0.75)'
    ))
    fig_area.add_trace(go.Scatter(
        x=weekly_ts['week'],
        y=weekly_ts['cases'],
        name='Kasus Baru',
        mode='lines',
        line=dict(width=0.5, color='#EF5350'),
        stackgroup='one',
        fillcolor='rgba(239, 83, 80, 0.65)'
    ))
    
    fig_area.update_layout(
        template='plotly_white',
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode='x unified',
        xaxis_title="Minggu Kalender (Tahun-Minggu)",
        yaxis_title="Total Akumulasi Mingguan",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_area, use_container_width=True)
    
    st.markdown("""
    <div class="insight-card">
        <div class="insight-title">💡 Insight Dinamika Temporal:</div>
        Kurva memperlihatkan dua gelombang eksponensial besar di Indonesia: 
        <b>Gelombang Delta (Juli 2021)</b> dengan angka kematian masif, dan <b>Gelombang Omicron (Februari 2022)</b> dengan angka infeksi harian memecahkan rekor (>60.000 kasus/hari) namun fatalitas sangat tertekan karena tingginya imunitas hasil vaksinasi.
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 3: ANALISIS VAKSINASI & FATALITAS
# ------------------------------------------------------------------------------
with tab3:
    col_t3_left, col_t3_right = st.columns([1, 1])
    
    with col_t3_left:
        st.markdown('<div class="section-title">🔗 Visualisasi 5: Korelasi Vaksinasi vs Penurunan Kasus</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-desc">Scatter plot tingkat vaksinasi dosis lengkap (%) vs persentase penurunan keparahan kasus pasca-puncak.</div>', unsafe_allow_html=True)
        
        corr_prov = df_filtered.groupby('province').agg({
            'vaccination_rate': 'first',
            'cases_decline': 'first',
            'island': 'first',
            'population': 'first',
            'total_cases': 'max'
        }).reset_index()
        
        fig_scatter = px.scatter(
            corr_prov,
            x='vaccination_rate',
            y='cases_decline',
            color='island',
            size='population',
            hover_name='province',
            trendline='ols',
            trendline_color_override='#1E293B',
            labels={
                'vaccination_rate': 'Cakupan Vaksinasi Dosis Lengkap (%)',
                'cases_decline': 'Penurunan Keparahan Kasus (%)',
                'island': 'Wilayah Pulau',
                'population': 'Populasi'
            },
            template='plotly_white'
        )
        fig_scatter.update_layout(
            height=460,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Pearson correlation metric
        if len(corr_prov) > 2:
            r_corr = np.corrcoef(corr_prov['vaccination_rate'], corr_prov['cases_decline'])[0, 1]
            st.info(f"📊 **Koefisien Korelasi Pearson (r): {r_corr:.3f}** | Mengindikasikan hubungan searah yang kuat antara capaian vaksinasi dan reduksi keparahan kasus.")
            
    with col_t3_right:
        st.markdown('<div class="section-title">📊 Visualisasi 6: Distribusi Case Fatality Rate (CFR %)</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-desc">Histogram frekuensi sebaran rasio fatalitas antarprovinsi di Indonesia.</div>', unsafe_allow_html=True)
        
        latest_cfr_df = df_filtered.groupby('province')['cfr'].last().reset_index()
        mean_cfr = latest_cfr_df['cfr'].mean()
        
        fig_hist = px.histogram(
            latest_cfr_df,
            x='cfr',
            nbins=20,
            labels={'cfr': 'Case Fatality Rate (%)'},
            color_discrete_sequence=['#1976D2'],
            template='plotly_white'
        )
        fig_hist.add_vline(
            x=mean_cfr,
            line_dash="dash",
            line_color="#EF4444",
            annotation_text=f"Rerata: {mean_cfr:.2f}%",
            annotation_position="top right"
        )
        fig_hist.update_layout(
            height=460,
            bargap=0.1,
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis_title="Jumlah Entitas Provinsi",
            xaxis_title="Rentang CFR (%)"
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
        st.success(f"🎯 **CFR Rata-rata: {mean_cfr:.2f}%** | Rentang: **{latest_cfr_df['cfr'].min():.2f}%** ({latest_cfr_df.loc[latest_cfr_df['cfr'].idxmin()]['province']}) hingga **{latest_cfr_df['cfr'].max():.2f}%** ({latest_cfr_df.loc[latest_cfr_df['cfr'].idxmax()]['province']}).")

# ------------------------------------------------------------------------------
# TAB 4: VARIABILITAS SPASIAL (BOX PLOT)
# ------------------------------------------------------------------------------
with tab4:
    st.markdown('<div class="section-title">📦 Visualisasi Bonus: Box Plot Sebaran Kasus Harian Berdasarkan Pulau</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Menganalisis variansi data, rentang interkuartil (IQR), dan keberadaan pencilan (outliers) kasus penularan.</div>', unsafe_allow_html=True)
    
    fig_box = px.box(
        df_filtered,
        x='island',
        y='cases',
        color='island',
        points='outliers',
        labels={'island': 'Gugus Kepulauan', 'cases': 'Kasus Harian Positif'},
        template='plotly_white'
    )
    fig_box.update_layout(
        height=480,
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis=dict(type='log', title="Kasus Harian (Skala Logaritmik)")
    )
    st.plotly_chart(fig_box, use_container_width=True)
    
    st.markdown("""
    <div class="insight-card">
        <div class="insight-title">💡 Insight Distribusi Box Plot (Skala Logaritmik):</div>
        Pulau Jawa memiliki nilai median tertinggi dengan bentangan interkuartil (IQR) dan pencilan ekstrem terpanjang, mencerminkan gejolak epidemiologi yang sangat tinggi. Sebaliknya, wilayah Maluku dan Papua memiliki median yang lebih rendah dan relatif stabil, meskipun dihadapkan pada keterbatasan kapasitas tracing laboratorium harian.
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 5: EKSPLORASI DATASET & UNDUH
# ------------------------------------------------------------------------------
with tab5:
    st.markdown('<div class="section-title">📋 Eksplorasi Data Tabular & Ekspor CSV</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Tabel interaktif hasil pembersihan data yang siap diinspeksi, difilter, dan diunduh.</div>', unsafe_allow_html=True)
    
    # Pencarian teks langsung
    search_q = st.text_input("🔍 Cari berdasarkan nama provinsi:", "")
    view_df = df_filtered.copy()
    if search_q:
        view_df = view_df[view_df['province'].str.contains(search_q, case=False)]
        
    display_cols = ['date_str', 'province', 'island', 'cases', 'recovered', 'deaths', 'cfr', 'vaccination_rate', 'cases_decline']
    st.dataframe(
        view_df[display_cols].rename(columns={
            'date_str': 'Tanggal',
            'province': 'Provinsi',
            'island': 'Pulau',
            'cases': 'Kasus Baru',
            'recovered': 'Sembuh',
            'deaths': 'Meninggal',
            'cfr': 'CFR (%)',
            'vaccination_rate': 'Vaksinasi (%)',
            'cases_decline': 'Penurunan Kasus (%)'
        }),
        use_container_width=True,
        height=400
    )
    
    col_d1, col_d2 = st.columns([1, 4])
    with col_d1:
        csv_download = view_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Data Terfilter (.csv)",
            data=csv_download,
            file_name=f"covid19_indonesia_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col_d2:
        st.caption(f"Menampilkan {len(view_df):,} dari total {len(df_full):,} records data bersih.")

# ------------------------------------------------------------------------------
# TAB 6: DOKUMENTASI & LAPORAN TAHAP
# ------------------------------------------------------------------------------
with tab6:
    st.markdown('<div class="section-title">📑 Dokumentasi & Laporan Pelaksanaan Tugas</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Transparansi metodologi proyek mencakup 4 laporan tahapan lengkap sesuai rubrik penilaian.</div>', unsafe_allow_html=True)
    
    doc_choice = st.selectbox(
        "Pilih Dokumen Laporan:",
        options=[
            "Tahap 1: Laporan Data Acquisition",
            "Tahap 2: Laporan Data Cleaning",
            "Tahap 3: Laporan Exploratory Data Analysis (EDA)",
            "Tahap 4: Laporan Perancangan Visualisasi"
        ]
    )
    
    doc_mapping = {
        "Tahap 1: Laporan Data Acquisition": "LAPORAN_TAHAP1_ACQUISITION.md",
        "Tahap 2: Laporan Data Cleaning": "LAPORAN_TAHAP2_CLEANING.md",
        "Tahap 3: Laporan Exploratory Data Analysis (EDA)": "LAPORAN_TAHAP3_EDA.md",
        "Tahap 4: Laporan Perancangan Visualisasi": "LAPORAN_TAHAP4_VISUALISASI.md"
    }
    
    target_file = os.path.join("docs", doc_mapping[doc_choice])
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
        st.markdown(content)
    else:
        st.warning(f"File laporan {target_file} tidak ditemukan di folder docs/.")

# ==============================================================================
# 9. FOOTER & ACADEMIC CREDITS
# ==============================================================================
st.markdown("""
<div class="footer-box">
    <b>Tugas Kuliah Visualisasi Data</b> • Program Studi Teknik Informatika - Semester VII<br>
    Implementasi Teknologi: <b>Streamlit, Plotly Express, Pandas, NumPy, Statsmodels</b><br>
    Sumber Data: Kementerian Kesehatan Republik Indonesia, Satgas COVID-19, KawalCOVID19, & Our World in Data (OWID).<br>
    © 2026 Teknik Informatika. All rights reserved.
</div>
""", unsafe_allow_html=True)
