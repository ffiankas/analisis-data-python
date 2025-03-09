import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Dashboard Penyewaan Sepeda 2012")

st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", options=[2011, 2012], index=1)

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")
day_df = day_df[day_df["yr"] == (selected_year - 2011)]

season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}

byseason_df = hour_df.groupby(by="season").cnt.sum().reset_index()
byseason_df["season"] = byseason_df["season"].map(season_labels)
byseason_df.rename(columns={
    "cnt": "total_rent"
}, inplace=True)

st.header("Proyek Akhir Analisis Bike Dataset :bike:")

st.subheader("Jumlah Penyewa Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 5))
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="total_rent", y="season", data=byseason_df.sort_values(by="total_rent", ascending=False),
    hue="season", palette=colors_, legend=False, ax=ax
)
ax.set_title("Jumlah Penyewa Berdasarkan Musim", fontsize=15)
ax.set_xlabel(None)
ax.set_ylabel(None)
xticks = np.arange(400000, 1100000, 200000)
ax.set_xticks(xticks)
ax.set_xticklabels([f"{int(x/1000)}K" for x in xticks])
ax.set_xlim(400000, 1100000)
st.pyplot(fig)

st.subheader("Tren Penyewaan Sepeda Bulanan di 2012")
data_2012 = day_df.copy()
data_2012["dteday"] = pd.to_datetime(data_2012["dteday"])
month = data_2012.resample('ME', on='dteday').sum()
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(month.index, month['cnt'], marker='o', linestyle='-', color="#72BCD4")
ax.set_xticks(month.index)
ax.set_xticklabels(month.index.strftime('%b'))
ax.set_title("Penyewaan Sepeda Selama Tahun 2012", fontsize=15)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.grid(True, linestyle="--", alpha=0.6)
st.pyplot(fig)

st.subheader("Tren Penyewaan Harian: Casual vs Registered")
rfm_df = data_2012[['dteday', 'casual', 'registered']].copy()
rfm_df_melted = rfm_df.melt(
    id_vars="dteday", value_vars=["casual", "registered"],
    var_name="user_type", value_name="count"
)
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=rfm_df_melted, x="dteday", y="count", hue="user_type", marker="o", ax=ax)
ax.set_title("Tren Penyewaan Harian 2012: Casual vs Registered", fontsize=15)
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_xticks(month.index)
ax.set_xticklabels(month.index.strftime('%b'))
plt.xticks(rotation=45)
ax.grid(True, linestyle="--", alpha=0.6)
st.pyplot(fig)

