import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard Penjualan", page_icon="📊", layout="wide")
st.title("Dashboard Interaktif Penjualan")
st.caption("Studi kasus HCI & visualisasi — data sintetis.")

@st.cache_data
def make_data():
    rng = np.random.default_rng(10)
    n = 180
    products = rng.choice(["Laptop", "Mouse", "Keyboard", "Headset"], n)
    units = rng.integers(1, 6, n)
    prices = pd.Series(products).map({
        "Laptop": 7500000, "Mouse": 150000,
        "Keyboard": 350000, "Headset": 500000
    }).to_numpy()
    dates = pd.to_datetime("2026-01-01") + pd.to_timedelta(rng.integers(0, 180, n), unit="D")
    return pd.DataFrame({"Tanggal": dates, "Produk": products, "Jumlah": units,
                         "Harga Satuan": prices, "Pendapatan": units * prices}).sort_values("Tanggal")

df = make_data()
st.sidebar.header("Filter")
products = st.sidebar.multiselect("Produk", sorted(df["Produk"].unique()),
                                   default=sorted(df["Produk"].unique()))
start = st.sidebar.date_input("Tanggal mulai", df["Tanggal"].min().date())
end = st.sidebar.date_input("Tanggal akhir", df["Tanggal"].max().date())
filtered = df[df["Produk"].isin(products)
              & (df["Tanggal"].dt.date >= start)
              & (df["Tanggal"].dt.date <= end)]
if filtered.empty:
    st.warning("Tidak ada data untuk filter ini. Silakan ubah pilihan.")
else:
    a, b, c = st.columns(3)
    a.metric("Total pendapatan", f"Rp{filtered['Pendapatan'].sum():,.0f}")
    b.metric("Total barang", f"{filtered['Jumlah'].sum():,}")
    c.metric("Jumlah transaksi", f"{len(filtered):,}")
    st.subheader("Pendapatan per produk")
    st.bar_chart(filtered.groupby("Produk")["Pendapatan"].sum().sort_values(ascending=False))
    st.subheader("Tren pendapatan harian")
    st.line_chart(filtered.groupby("Tanggal")["Pendapatan"].sum())
    st.subheader("Transaksi")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
st.caption("Data ini sintetis, bukan transaksi bisnis nyata.")
