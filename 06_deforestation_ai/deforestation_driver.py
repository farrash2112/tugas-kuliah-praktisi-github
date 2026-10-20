import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

rng = np.random.default_rng(21)
n = 600
ndvi_change = rng.normal(-0.25, 0.18, n)
distance_road = rng.gamma(2.0, 1.8, n)
patch_area = rng.lognormal(1.8, 0.7, n)
near_settlement = rng.binomial(1, 0.35, n)
dryness = rng.uniform(0, 1, n)

# Label buatan untuk demonstrasi; bukan label kejadian deforestasi nyata.
scores = np.column_stack([
    (ndvi_change < -0.3).astype(int) + near_settlement,
    (distance_road < 1.2).astype(int) + (patch_area > 10).astype(int),
    (distance_road < 3.0).astype(int) + (dryness < 0.4).astype(int)
])
classes = np.array(["Ekspansi pertanian", "Pembangunan jalan", "Penebangan"])
y = classes[scores.argmax(axis=1)]
X = pd.DataFrame({
    "perubahan_ndvi": ndvi_change, "jarak_jalan_km": distance_road,
    "luas_petak_ha": patch_area, "dekat_permukiman": near_settlement,
    "kekeringan_musiman": dryness
})
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=21, stratify=y)
model = RandomForestClassifier(n_estimators=200, max_depth=8,
                               class_weight="balanced", random_state=21)
model.fit(X_train, y_train)
pred = model.predict(X_test)
print("=== KLASIFIKASI ALERT DEFORESTASI (DEMO) ===")
print("Sampel sintetis:", len(X))
print("Akurasi:", round(accuracy_score(y_test, pred), 3))
print(classification_report(y_test, pred, zero_division=0))
print("Urutan kelas confusion matrix:", list(model.classes_))
print(confusion_matrix(y_test, pred))
print("\nPentingnya fitur:")
print(pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False).round(3))
example = pd.DataFrame([{"perubahan_ndvi": -0.55, "jarak_jalan_km": 0.7,
                         "luas_petak_ha": 15.0, "dekat_permukiman": 1,
                         "kekeringan_musiman": 0.3}])
print("\nPrediksi contoh:", model.predict(example)[0])
print("Peringatan: data sintetis; prediksi bukan bukti penyebab deforestasi.")
