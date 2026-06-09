import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide")

st.markdown("""
<style>

[data-testid="stSidebar"] {
    background-color: #6e1d3a;
    transition: all 0.3s ease;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1rem !important;
}

[data-testid="collapsedControl"] {
    color: white;
}

[data-testid="stSidebar"] .stColumns {
    gap: 0px !important; /* Menghilangkan jarak bawaan antar kolom logo */
}

.profile-container {
    display: flex;
    align-items: center;
    padding: 15px 12px;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    margin-top: -5px; /* Menaikkan posisi kotak profil agar mendekati logo */
    margin-bottom: 35px; /* MENAMBAH JARAK SPACE ANTARA KOTAK NAMA DAN NAVIGASI */
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.profile-avatar {
    width: 55px;
    height: 55px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid rgba(255, 255, 255, 0.8);
    margin-right: 12px;
}

.profile-text-box {
    display: flex;
    flex-direction: column;
}

.profile-name {
    color: white !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    line-height: 1.2 !important;
}

.profile-major {
    color: rgba(255, 255, 255, 0.7) !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    margin-top: 3px !important;
}

.stButton>button {
    width: 100%;
    padding: 16px 20px !important; /* Mempertebal ukuran tombol */
    font-size: 18px !important; /* MEMPERBESAR UKURAN FONT NAVIGASI */
    font-weight: 600 !important;
    color: rgba(255, 255, 255, 0.85) !important;
    background-color: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    margin-bottom: 10px !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    text-align: center !important;
}

/* HOVER EFFECT */
.stButton>button:hover {
    background-color: rgba(255, 255, 255, 0.12) !important;
    color: #ffffff !important;
    transform: scale(1.02) !important; /* Efek membesar sedikit secara proporsional saat di-hover */
}

.stButton>button:disabled, .stButton>button[disabled] {
    background-color: #ffffff !important;
    color: #6e1d3a !important;
    border-left: none !important; /* Menghilangkan border kiri agar simetris saat rata tengah */
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    cursor: default !important;
    transform: none !important;
    opacity: 1 !important;
}

.kpi-card {
    background-color: var(--background-color, #ffffff) !important;
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #800000;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    margin-bottom: 15px;
}

/* CONTAINER BERGARIS ADAPTIF 100% */
.outline-box {
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 20px;
    background-color: var(--background-color, #ffffff) !important;
}

/* SINKRONISASI MUTLAK WARNA TEKS ANAK TERMASUK DAFTAR POIN (LI) */
.kpi-card, .kpi-card *,
.outline-box, .outline-box * {
    color: var(--text-color, #31333F) !important;
}

/* EFISIENSI TRANSISI PERUBAHAN TEMA */
.kpi-card, .outline-box {
    transition: background-color 0.25s ease, color 0.25s ease !important;
}

.header-box {
    background: linear-gradient(135deg, #6e1d3a, #800000);
    padding: 25px 30px;
    border-radius: 16px;
    color: white;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    margin-bottom: 25px;
}

.header-title { font-size: 28px; font-weight: 700; }
.header-sub { font-size: 14px; opacity: 0.9; }
.section { font-size: 22px; font-weight: 700; margin-top: 20px; color: #800000; }

</style>
""", unsafe_allow_html=True)

# =========================================
# LOAD DATA
# =========================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    path_konten = os.path.join(current_dir, "data", "hasil_analisis_konten.csv")
    path_agregat = os.path.join(current_dir, "data", "hasil_clustering_agregat_1tahun.csv")

    df_konten = pd.read_csv(path_konten)
    df_agregat = pd.read_csv(path_agregat)
    return df_konten, df_agregat


def prepare_agregat_data(df):
    df = df.copy()

    # Rapikan nama kolom dari TikTok Studio
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Mapping kolom fleksibel
    rename_map = {
        "date": "date",
        "tanggal": "date",

        "video_views": "video_views",
        "video_view": "video_views",
        "video_vie": "video_views",
        "views": "video_views",
        "tayangan": "video_views",

        "profile_views": "profile_views",
        "profile_view": "profile_views",
        "profile_vie": "profile_views",

        "likes": "likes",
        "like": "likes",
        "suka": "likes",

        "comments": "comments",
        "comment": "comments",
        "komentar": "comments",

        "shares": "shares",
        "share": "shares",
        "dibagikan": "shares",
    }

    df = df.rename(columns={col: rename_map[col] for col in df.columns if col in rename_map})

    required_cols = ["date", "video_views"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        raise ValueError(
            f"Kolom wajib tidak ditemukan: {missing_cols}. "
            f"Kolom terbaca: {list(df.columns)}"
        )

    # Konversi format tanggal Indonesia dari TikTok Studio
    bulan_map = {
        "januari": "January",
        "februari": "February",
        "maret": "March",
        "april": "April",
        "mei": "May",
        "juni": "June",
        "juli": "July",
        "agustus": "August",
        "september": "September",
        "oktober": "October",
        "november": "November",
        "desember": "December",
    }

    def convert_indonesia_date(x):
        x = str(x).strip().lower()

        for indo, eng in bulan_map.items():
            x = x.replace(indo, eng)

        # jika format hanya "1 June", tambahkan tahun default
        if not any(char.isdigit() and len(x.split()) >= 3 for char in x):
            pass

        if len(x.split()) == 2:
            x = f"{x} 2026"

        return x

    df["date"] = df["date"].apply(convert_indonesia_date)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Bersihkan angka
    numeric_cols = ["video_views", "profile_views", "likes", "comments", "shares"]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace(".", "", regex=False)
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df = df.dropna(subset=["date"])

    if df.empty:
        raise ValueError("Data kosong setelah konversi tanggal. Periksa format kolom Date.")

    # Hitung metrik tambahan
    if "likes" in df.columns and "comments" in df.columns and "shares" in df.columns:
        df["engagement_total"] = df["likes"] + df["comments"] + df["shares"]
    else:
        df["engagement_total"] = 0

    df["engagement_rate"] = (
        df["engagement_total"] / df["video_views"].replace(0, pd.NA)
    ) * 100

    df["engagement_rate"] = df["engagement_rate"].fillna(0).round(2)

    df["day_name"] = df["date"].dt.day_name()
    df["month"] = df["date"].dt.month_name()

    return df


df_konten, df_agregat_default = load_data()
df_agregat_default = prepare_agregat_data(df_agregat_default)

if "df_agregat_active" not in st.session_state:
    st.session_state.df_agregat_active = df_agregat_default

if "nama_file_agregat" not in st.session_state:
    st.session_state.nama_file_agregat = "Dataset default"

df_agregat = st.session_state.df_agregat_active

# =========================================
# HEADER FUNCTION (TAMBAHKAN DI SINI)
# =========================================
def render_header(title, subtitle):
    st.markdown(f"""
    <div class="header-box">
        <div class="header-title">{title}</div>
        <div class="header-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)
# =========================================
# SIDEBAR PREMIUM (RESTRUKTURISASI TATA LETAK)
# =========================================
with st.sidebar:

    # 1. LOGO HORIZONTAL SEJAJAR & BERDEMPETAN BERJARAK
    col_logo1, col_logo2 = st.columns([1, 1])
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_logo_kampus = os.path.join(base_dir, "assets", "logo_kampus.png")
    path_logo_radar = os.path.join(base_dir, "assets", "logo_radar.png")
    
    with col_logo1:
        # Mengatur perataan kanan (right) untuk logo pertama agar berdempetan ke tengah
        st.markdown('<div style="text-align: right; padding-right: 10px;">', unsafe_allow_html=True)
        st.image(path_logo_kampus, width=65)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_logo2:
        # Mengatur perataan kiri (left) untuk logo kedua agar berdempetan ke tengah
        st.markdown('<div style="text-align: left; padding-left: 10px;">', unsafe_allow_html=True)
        st.image(path_logo_radar, width=75)
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. KOMPONEN PROFIL MAHASISWA (FOTO BULAT + IDENTITAS)
    path_foto_profil = os.path.join(base_dir, "assets", "foto_profil.png")
    
    # Validasi apakah file foto tersedia untuk menghindari kegagalan sistem
    if os.path.exists(path_foto_profil):
        import base64
        with open(path_foto_profil, "rb") as image_file:
            encoded_img = base64.b64encode(image_file.read()).decode()
        img_src = f"data:image/png;base64,{encoded_img}"
    else:
        # Menggunakan avatar in-memory default jika file foto fisik belum diletakkan
        img_src = "https://www.w3schools.com/howto/img_avatar.png"

    st.markdown(f"""
    <div class="profile-container">
        <img src="{img_src}" class="profile-avatar" alt="Avatar">
        <div class="profile-text-box">
            <div class="profile-name">Muhammad Fajar Satria Adam.</div>
            <div class="profile-major">Teknik Informatika</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. SISTEM MANAJEMEN HALAMAN (STATE)
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"

    # 4. FUNGSI NAVIGASI PREMIUM DENGAN NATIVE SHORTCODE EMOJI
    def render_nav_button(label, key, emoji_icon):
        is_active = (st.session_state.page == key)
        
        # Menggabungkan emoji bawaan yang aman dibaca oleh st.button
        button_label = f"{emoji_icon}  {label}"
        
        # Pemicu pembungkus divisi kelas lewat markdown sebelum tombol dicetak
        if st.button(button_label, key=f"btn_{key}", disabled=is_active):
            st.session_state.page = key
            st.rerun()

    # EKSEKUSI MENU NAVIGASI MENGGUNAKAN EMOJI FORMAL JELAS
    render_nav_button("Dashboard", "dashboard", "🏠︎")
    render_nav_button("Data Agregat", "agregat", "🗁")
    render_nav_button("Analisis Konten", "konten", "🗐")
    render_nav_button("Strategi & Rekomendasi", "strategi", "✈︎")

menu = st.session_state.page


# =========================================
# ================= DASHBOARD =================
# =========================================
if menu == "dashboard":
    render_header(
        "Dashboard Analisis TikTok Radar Sukabumi",
        "Ringkasan performa konten dan insight utama"
    )
    
    st.markdown("### 📤 Upload Data Agregat Baru")

    with st.expander("Upload CSV Data Agregat TikTok Studio", expanded=False):
        st.info(
            "Upload file CSV data agregat baru. Minimal harus memiliki kolom Date, Video views, Likes, Comments, dan Shares, sistem akan menghitung engagement secara otomatis."
        )

        uploaded_agregat = st.file_uploader(
            "Pilih file CSV data agregat",
            type=["csv"],
            key="upload_agregat"
        )

        col_upload1, col_upload2 = st.columns([1, 1])

        with col_upload1:
            if uploaded_agregat is not None:
                try:
                    uploaded_df = pd.read_csv(uploaded_agregat)
                    uploaded_df = prepare_agregat_data(uploaded_df)

                    st.session_state.df_agregat_active = uploaded_df
                    st.session_state.nama_file_agregat = uploaded_agregat.name

                    st.success(f"Data berhasil diunggah: {uploaded_agregat.name}")
                    st.rerun()

                except Exception as e:
                    st.error(f"Upload gagal. Periksa format kolom CSV. Detail error: {e}")

        with col_upload2:
            if st.button("Gunakan Dataset Default"):
                st.session_state.df_agregat_active = df_agregat_default
                st.session_state.nama_file_agregat = "Dataset default"
                st.rerun()

    df_agregat = st.session_state.df_agregat_active

    st.caption(f"Dataset agregat aktif: {st.session_state.nama_file_agregat}")
    # ================= KPI =================

    # ================= KPI ADAPTIF FINAL =================

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f"""
    <div class="kpi-card">
        <b>Total Views</b><br>
        <span style="font-size: 22px; font-weight: 700;">{df_agregat["video_views"].sum():,.0f}</span>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="kpi-card">
        <b>Avg Engagement</b><br>
        <span style="font-size: 22px; font-weight: 700;">{df_agregat["engagement_rate"].mean():.2f}%</span>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="kpi-card">
        <b>Total Hari Data</b><br>
        <span style="font-size: 22px; font-weight: 700;">{len(df_agregat)}</span>
    </div>
    """, unsafe_allow_html=True)

    col4.markdown(f"""
    <div class="kpi-card">
        <b>Total Konten</b><br>
        <span style="font-size: 22px; font-weight: 700;">{len(df_konten)}</span>
    </div>
    """, unsafe_allow_html=True)

    # ================= ROW 1 =================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Trend Video Views")
        fig = px.line(df_agregat, x="date", y="video_views")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Trend Engagement Rate")
        fig2 = px.line(df_agregat, x="date", y="engagement_rate")
        st.plotly_chart(fig2, use_container_width=True)

    # ================= ROW 2 =================
    col1, col2 = st.columns(2)

    avg_day = df_agregat.groupby('day_name')['video_views'].mean().reset_index()

    with col1:
        st.markdown("#### 📅 Rata-rata Views per Hari")
        fig3 = px.bar(avg_day, x="day_name", y="video_views")
        st.plotly_chart(fig3, use_container_width=True)

    avg_month = df_agregat.groupby('month')['video_views'].mean().reset_index()

    with col2:
        st.markdown("#### 🗓️ Rata-rata Views per Bulan")
        fig4 = px.bar(avg_month, x="month", y="video_views")
        st.plotly_chart(fig4, use_container_width=True)

    # ================= ROW 3 =================
    st.markdown("#### 🎯 Performa Konten")

    perf = df_konten.groupby("content_type")[["engagement_rate"]].mean()

    fig5 = px.bar(perf, y=perf.index, x="engagement_rate", orientation='h')
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# ================= AGREGAT =================
# =========================================
elif menu == "agregat":
    render_header(
        "Data Agregat 1 Tahun",
        "Analisis tren performa berdasarkan waktu"
    )
    df_agregat = st.session_state.df_agregat_active
    st.caption(f"Dataset agregat aktif: {st.session_state.nama_file_agregat}")
    # ================= KPI MINI =================
    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f"""
    <div class="kpi-card">
        <b>Total Profile Views</b><br>
        <span style="font-size: 22px; font-weight: 700;">{df_agregat["profile_views"].sum():,.0f}</span>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="kpi-card">
        <b>Total Likes</b><br>
        <span style="font-size: 22px; font-weight: 700;">{df_agregat["likes"].sum():,.0f}</span>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="kpi-card">
        <b>Total Comments</b><br>
        <span style="font-size: 22px; font-weight: 700;">{df_agregat["comments"].sum():,.0f}</span>
    </div>
    """, unsafe_allow_html=True)

    col4.markdown(f"""
    <div class="kpi-card">
        <b>Total Shares</b><br>
        <span style="font-size: 22px; font-weight: 700;">{df_agregat["shares"].sum():,.0f}</span>
    </div>
    """, unsafe_allow_html=True)

    # ================= ROW 1 =================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Trend Video Views")
        fig1 = px.line(df_agregat, x="date", y="video_views")
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("### 📊 Trend Engagement Rate")
        fig2 = px.line(df_agregat, x="date", y="engagement_rate")
        st.plotly_chart(fig2, use_container_width=True)

    # ================= ROW 2 =================
    col1, col2 = st.columns(2)

    avg_day = df_agregat.groupby('day_name')['video_views'].mean().reset_index()

    with col1:
        st.markdown("### 📅 Rata-rata Views per Hari")
        fig3 = px.bar(avg_day, x="day_name", y="video_views")
        st.plotly_chart(fig3, use_container_width=True)

    avg_month = df_agregat.groupby('month')['video_views'].mean().reset_index()

    with col2:
        st.markdown("### 🗓️ Rata-rata Views per Bulan")
        fig4 = px.bar(avg_month, x="month", y="video_views")
        st.plotly_chart(fig4, use_container_width=True)

    # ================= INSIGHT =================
    best_day = df_agregat.loc[df_agregat['video_views'].idxmax()]

    st.markdown("<br>", unsafe_allow_html=True)

    st.success(
        f"Hari dengan performa tertinggi adalah {best_day['date'].date()} "
        f"dengan {best_day['video_views']:,} views"
    )

# =========================================
# ================= KONTEN =================
# =========================================
elif menu == "konten":
    render_header(
        "Analisis Per Konten",
        "Evaluasi performa berdasarkan kategori dan jenis konten"
    )

    kategori = st.selectbox("Kategori", ["Semua"] + list(df_konten['performance_category'].dropna().unique()))
    content = st.selectbox("Jenis Konten", ["Semua"] + list(df_konten['content_type'].dropna().unique()))

    df_filtered = df_konten.copy()

    if kategori != "Semua":
        df_filtered = df_filtered[df_filtered['performance_category'] == kategori]

    if content != "Semua":
        df_filtered = df_filtered[df_filtered['content_type'] == content]

    # ================= VALIDASI DATA =================
    if df_filtered.empty:
        st.warning("Data tidak tersedia untuk filter yang dipilih")
    else:
        # ================= KPI =================
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Views", f"{df_filtered['video_views'].mean():,.0f}")
        col2.metric("Avg Engagement", f"{df_filtered['engagement_rate'].mean():.2f}%")
        col3.metric("Total Konten", len(df_filtered))

        # ================= HISTOGRAM =================
        fig = px.histogram(df_filtered, x="performance_category", title="Distribusi Performa")
        st.plotly_chart(fig, use_container_width=True)

        # ================= BAR CHART (TAMBAHAN) =================
        st.markdown("### 📊 Performa Rata-rata per Jenis Konten")

        perf = df_filtered.groupby("content_type")[["engagement_rate"]].mean()

        fig5 = px.bar(
            perf,
            y=perf.index,
            x="engagement_rate",
            orientation='h'
        )

        fig5.update_layout(
            xaxis_title="Engagement Rate (%)",
            yaxis_title="Content Type",
            plot_bgcolor="white"
        )

        st.plotly_chart(fig5, use_container_width=True)

        # ================= INSIGHT =================
        st.markdown('<p class="section">Insight & Strategi Cepat</p>', unsafe_allow_html=True)

        # HANDLE kalau tidak ada engagement_total
        if 'engagement_total' in df_konten.columns:
            best = df_konten.loc[df_konten['engagement_total'].idxmax()]
            worst = df_konten.loc[df_konten['engagement_total'].idxmin()]

            st.success(f"Konten terbaik: {best['content_type']} ({best['engagement_total']:,.0f})")
            st.error(f"Konten terburuk: {worst['content_type']} ({worst['engagement_total']:,.0f})")
        else:
            best = df_konten.loc[df_konten['engagement_rate'].idxmax()]
            worst = df_konten.loc[df_konten['engagement_rate'].idxmin()]

            st.success(f"Konten terbaik: {best['content_type']} ({best['engagement_rate']:.2f}%)")
            st.error(f"Konten terburuk: {worst['content_type']} ({worst['engagement_rate']:.2f}%)")


# =========================================
# ================= STRATEGI =================
# =========================================
elif menu == "strategi":

    render_header(
        "Strategi & Rekomendasi",
        "Insight berbasis data untuk optimasi konten"
    )

    # ===============================
    # PREPROCESS
    # ===============================
    df_agregat['date'] = pd.to_datetime(df_agregat['date'], errors='coerce')
    df_agregat['day_name'] = df_agregat['date'].dt.day_name()
    df_agregat['month'] = df_agregat['date'].dt.month_name()

    # ===============================
    # KPI UTAMA
    # ===============================
    st.markdown("### 📊 Hasil Analisis Performa")

    col1, col2, col3 = st.columns(3)

    best_day_views = df_agregat.groupby('day_name')['video_views'].mean().idxmax()
    best_day_eng = df_agregat.groupby('day_name')['engagement_rate'].mean().idxmax()
    best_month = df_agregat.groupby('month')['video_views'].mean().idxmax()

    col1.metric("Hari Views Tertinggi", best_day_views)
    col2.metric("Hari Engagement Tertinggi", best_day_eng)
    col3.metric("Bulan Terbaik", best_month)

    # ===============================
    # TABEL ANALISIS
    # ===============================
    st.markdown("### 📅 Analisis Hari Terbaik")
    day_perf = df_agregat.groupby('day_name').agg({
        'video_views': 'mean',
        'engagement_rate': 'mean'
    }).sort_values(by='video_views', ascending=False)

    st.dataframe(day_perf)

    st.markdown("### 🗓️ Analisis Bulan Terbaik")
    month_perf = df_agregat.groupby('month').agg({
        'video_views': 'mean',
        'engagement_rate': 'mean'
    }).sort_values(by='video_views', ascending=False)

    st.dataframe(month_perf)

    # ===============================
    # ANALISIS KONTEN
    # ===============================
    st.markdown("### 🎯 Analisis Berdasarkan Konten")

    content_perf = df_konten.groupby('content_type').agg({
        'video_views': 'mean',
        'engagement_rate': 'mean',
        'engagement_total': 'mean' if 'engagement_total' in df_konten.columns else 'engagement_rate'
    })

    st.dataframe(content_perf)

    # ===============================
    # WAKTU UPLOAD
    # ===============================
    if 'upload_category' in df_konten.columns:
        st.markdown("### ⏰ Analisis Waktu Upload")

        time_perf = df_konten.groupby('upload_category').agg({
            'video_views': 'mean',
            'engagement_rate': 'mean'
        })

        st.dataframe(time_perf)

    # ===============================
    # BEST CONTENT
    # ===============================
    best_views = df_konten.groupby('content_type')['video_views'].mean().idxmax()
    best_eng = df_konten.groupby('content_type')['engagement_rate'].mean().idxmax()

        # ===============================
    # STRATEGI OTOMATIS
    # ===============================
    st.markdown("### 🧠 Insight Otomatis & Strategi")

    avg_views = df_agregat['video_views'].mean()
    avg_eng = df_agregat['engagement_rate'].mean()

    st.markdown(f"""
    <div class='outline-box'>

    <b>Kategori performa terbaik:</b> Tinggi <br>
    <b>Hari dominan:</b> {best_day_views} <br>
    <b>Bulan dominan:</b> {best_month} <br><br>

    <b>Rata-rata views:</b> {avg_views:,.0f} <br>
    <b>Rata-rata engagement rate:</b> {avg_eng:.2f}% <br>

    </div>
    """, unsafe_allow_html=True)


    # ===============================
    # REKOMENDASI
    # ===============================
    st.markdown("### 📌 Rekomendasi Strategi")

    if 'upload_category' in df_konten.columns:
        best_time_views = df_konten.groupby('upload_category')['video_views'].mean().idxmax()
        best_time_eng = df_konten.groupby('upload_category')['engagement_rate'].mean().idxmax()
    else:
        best_time_views = "-"
        best_time_eng = "-"

    st.markdown(f"""
    <div class='outline-box'>

    <b>1. Jenis konten terbaik:</b><br>
    - Views: {best_views}<br>
    - Engagement: {best_eng}<br><br>

    <b>2. Waktu upload terbaik:</b><br>
    - Views: {best_time_views}<br>
    - Engagement: {best_time_eng}<br><br>

    <b>3. Hari terbaik:</b><br>
    - Views: {best_day_views}<br>
    - Engagement: {best_day_eng}<br><br>

    <b>4. Rekomendasi:</b><br>
    - Fokus pada konten {best_views}<br>
    - Upload pada waktu {best_time_views}<br>
    - Konsisten di hari {best_day_views}<br>
    - Replikasi pola konten performa tinggi<br>
    - Gunakan hari rendah untuk eksperimen konten<br>

    </div>
    """, unsafe_allow_html=True)
    
