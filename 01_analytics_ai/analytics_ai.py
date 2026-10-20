from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

rng = np.random.default_rng(42)
n = 240
produk = rng.choice(["Laptop", "Mouse", "Keyboard", "Headset"], n)
jumlah = rng.integers(1, 8, n)
harga = pd.Series(produk).map({
    "Laptop": 7_500_000, "Mouse": 150_000,
    "Keyboard": 350_000, "Headset": 500_000
}).to_numpy()
diskon = rng.uniform(0, 0.25, n).round(2)
pendapatan = (jumlah * harga * (1 - diskon)).round(0)
df = pd.DataFrame({"produk": produk, "jumlah": jumlah, "harga_unit": harga,
                   "diskon": diskon, "pendapatan": pendapatan})
df["kategori"] = np.where(df.pendapatan >= df.pendapatan.median(), "Tinggi", "Rendah")

print("=== ANALITIK PENJUALAN ===")
print("Jumlah transaksi:", len(df))
print(f"Total pendapatan: Rp{df.pendapatan.sum():,.0f}")
print("\nPendapatan per produk:")
print(df.groupby("produk").pendapatan.sum().sort_values(ascending=False))

X = pd.get_dummies(df[["produk", "jumlah", "harga_unit", "diskon"]], columns=["produk"])
y = df["kategori"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)
model = DecisionTreeClassifier(max_depth=4, random_state=42).fit(X_train, y_train)
pred = model.predict(X_test)
print("\nAkurasi:", round(accuracy_score(y_test, pred), 3))
print(classification_report(y_test, pred, zero_division=0))
df.groupby("produk").pendapatan.sum().sort_values().plot(kind="barh")
plt.title("Total Pendapatan per Produk")
plt.xlabel("Pendapatan (Rp)")
plt.tight_layout()
plt.savefig(Path(__file__).with_name("ringkasan_penjualan.png"), dpi=150)
print("Grafik disimpan: ringkasan_penjualan.png")
