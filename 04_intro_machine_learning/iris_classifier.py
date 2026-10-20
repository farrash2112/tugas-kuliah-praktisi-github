from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.25, random_state=42, stratify=iris.target)
model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
model.fit(X_train, y_train)
pred = model.predict(X_test)
print("=== KLASIFIKASI IRIS ===")
print("Akurasi:", round(accuracy_score(y_test, pred), 3))
print(classification_report(y_test, pred, target_names=iris.target_names))
print("Confusion matrix (baris=aktual, kolom=prediksi):")
print(confusion_matrix(y_test, pred))
sample = [[5.1, 3.5, 1.4, 0.2]]
print("Contoh prediksi:", iris.target_names[model.predict(sample)[0]])
