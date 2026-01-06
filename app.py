import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import RobustScaler

# =====================================
# KONFIGURASI HALAMAN
# =====================================
st.set_page_config(
    page_title="Crypto Top 1000 Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Visualisasi Crypto Top 1000")
st.markdown("Dataset global diambil dari GitHub dan divisualisasikan menggunakan Streamlit.")

# =====================================
# LOAD DATASET GLOBAL (GITHUB)
# =====================================
DATA_URL = "https://raw.githubusercontent.com/AwalDinz/crypto-datasets/main/crypto_top1000_dataset.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL)

df = load_data()

# =====================================
# PREPROCESSING
# =====================================
df = df.dropna(subset=[
    "current_price",
    "market_cap",
    "total_volume",
    "price_change_percentage_24h"
])

scaler = RobustScaler()
df["market_cap_scaled"] = scaler.fit_transform(df[["market_cap"]])

# =====================================
# SIDEBAR FILTER
# =====================================
st.sidebar.header("🔍 Filter Data")

top_n = st.sidebar.slider(
    "Pilih Top N Crypto berdasarkan Market Cap",
    min_value=10,
    max_value=1000,
    value=100
)

df_top = df.sort_values("market_cap", ascending=False).head(top_n)

# =====================================
# METRIK RINGKAS
# =====================================
col1, col2, col3 = st.columns(3)

col1.metric("Total Crypto Ditampilkan", len(df_top))
col2.metric("Rata-rata Harga", f"${df_top['current_price'].mean():,.2f}")
col3.metric("Rata-rata Market Cap", f"${df_top['market_cap'].mean():,.0f}")

# =====================================
# VISUALISASI 1: BAR CHART
# =====================================
st.subheader("📈 Market Cap Top Crypto")

fig_bar = px.bar(
    df_top,
    x="name",
    y="market_cap",
    title="Market Cap Cryptocurrency",
    labels={"market_cap": "Market Cap (USD)", "name": "Cryptocurrency"}
)

st.plotly_chart(fig_bar, use_container_width=True)

# =====================================
# VISUALISASI 2: SCATTER PLOT
# =====================================
st.subheader("🔵 Hubungan Harga vs Market Cap")

fig_scatter = px.scatter(
    df_top,
    x="market_cap",
    y="current_price",
    size="total_volume",
    color="price_change_percentage_24h",
    hover_name="name",
    title="Harga vs Market Cap",
    labels={
        "market_cap": "Market Cap",
        "current_price": "Harga Saat Ini"
    }
)

st.plotly_chart(fig_scatter, use_container_width=True)

# =====================================
# VISUALISASI 3: DISTRIBUSI
# =====================================
st.subheader("📊 Distribusi Perubahan Harga 24 Jam")

fig_hist = px.histogram(
    df_top,
    x="price_change_percentage_24h",
    nbins=50,
    title="Distribusi Price Change 24H (%)"
)

st.plotly_chart(fig_hist, use_container_width=True)

# =====================================
# TABEL DATA
# =====================================
st.subheader("📄 Data Crypto")

st.dataframe(
    df_top[[
        "name",
        "symbol",
        "current_price",
        "market_cap",
        "total_volume",
        "price_change_percentage_24h"
    ]]
)

# =====================================
# FOOTER
# =====================================
st.markdown("---")
st.markdown(
    "Final Project Visualisasi Data | Dataset Global dari GitHub | Streamlit Cloud"
)
