import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ========================
# CONFIG
# ========================
st.set_page_config(
    page_title="Air Quality Dashboard",
    layout="wide"
)

FIG_SIZE = (3, 2)
DPI = 120

# ========================
# LOAD DATA
# ========================
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    file_id = "18SJfGBNBEviWArMvZ7l6gH4bM5mIXtX1"
    url = f"https://drive.google.com/uc?id={file_id}"
    df = pd.read_csv(url)
    return df

df = load_data()

# ========================
# TITLE
# ========================
st.title("🌍 Air Quality Dashboard (Beijing 2013–2017)")
st.caption("Analisis kualitas udara berdasarkan waktu, lokasi, dan faktor cuaca")

# ========================
# SIDEBAR FILTER
# ========================
st.sidebar.header("🔍 Filter")

stations = st.sidebar.multiselect(
    "Pilih Stasiun",
    options=sorted(df['station'].unique()),
    default=sorted(df['station'].unique())
)

year_min, year_max = int(df['year'].min()), int(df['year'].max())
year_range = st.sidebar.slider(
    "Rentang Tahun",
    year_min, year_max, (year_min, year_max)
)

df_filtered = df[
    (df['station'].isin(stations)) &
    (df['year'].between(year_range[0], year_range[1]))
].copy()

# ========================
# KPI
# ========================
k1, k2, k3 = st.columns(3)
k1.metric("Avg PM2.5", f"{df_filtered['PM2.5'].mean():.2f}")
k2.metric("Max PM2.5", f"{df_filtered['PM2.5'].max():.2f}")
k3.metric("Min PM2.5", f"{df_filtered['PM2.5'].min():.2f}")

st.divider()

# ========================
# ROW 1
# ========================
c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 Trend PM2.5 per Tahun")
    pm25_year = df_filtered.groupby('year')['PM2.5'].mean()

    fig1, ax1 = plt.subplots(figsize=FIG_SIZE, dpi=DPI)
    ax1.plot(pm25_year.index, pm25_year.values, marker='o')
    ax1.set_xlabel("Tahun")
    ax1.set_ylabel("PM2.5")
    ax1.grid(alpha=0.3)
    st.pyplot(fig1)

with c2:
    st.subheader("🏙️ PM2.5 per Stasiun")
    pm25_station = df_filtered.groupby('station')['PM2.5'].mean().sort_values()

    fig2, ax2 = plt.subplots(figsize=FIG_SIZE, dpi=DPI)
    pm25_station.plot(kind='barh', ax=ax2)
    ax2.set_xlabel("PM2.5")
    st.pyplot(fig2)

st.divider()

# ========================
# ROW 2
# ========================
c3, c4 = st.columns(2)

with c3:
    st.subheader("🌡️ Suhu vs PM2.5")
    fig3, ax3 = plt.subplots(figsize=FIG_SIZE, dpi=DPI)
    sns.scatterplot(
        x=df_filtered['TEMP'],
        y=df_filtered['PM2.5'],
        alpha=0.3,
        ax=ax3
    )
    ax3.set_xlabel("Temperature")
    ax3.set_ylabel("PM2.5")
    st.pyplot(fig3)

with c4:
    st.subheader("📊 Kategori PM2.5 (Binning)")
    bins = [0, 50, 100, 150, 200, 500]
    labels = ['Baik', 'Sedang', 'Tidak Sehat', 'Sangat Tidak Sehat', 'Berbahaya']

    df_filtered['kategori_pm25'] = pd.cut(
        df_filtered['PM2.5'], bins=bins, labels=labels
    )

    kategori = df_filtered['kategori_pm25'].value_counts().reindex(labels)

    fig4, ax4 = plt.subplots(figsize=FIG_SIZE, dpi=DPI)
    kategori.plot(kind='bar', ax=ax4)
    ax4.set_xlabel("Kategori")
    ax4.set_ylabel("Jumlah")
    st.pyplot(fig4)

st.divider()

# ========================
# INSIGHT
# ========================
st.subheader("🧠 Insight")
st.info(
    "- PM2.5 berfluktuasi dan memuncak di 2017\n"
    "- Stasiun perkotaan cenderung lebih tinggi\n"
    "- Angin membantu menurunkan polusi\n"
    "- Mayoritas berada di kategori Baik–Sedang, namun ada kondisi ekstrem"
)