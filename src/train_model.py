import pandas as pd
import os
import joblib
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, precision_score, log_loss, f1_score
from sklearn.preprocessing import StandardScaler

# -------------------------
# 1. Configuración de MLflow
# -------------------------
# Establece el nombre del experimento para que no salga "Default"
mlflow.set_experiment("PREDICCION DE LLUVIA IDEAM")

# -------------------------
# Rutas dinámicas
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "dataset_modelo_estacion_52045020.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "rain_model.pkl")

os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)

print("📥 Cargando dataset...")
df = pd.read_csv(DATA_PATH)

# Eliminar columnas innecesarias
df = df.drop(columns=["fecha", "estacion"], errors="ignore")

# -------------------------
# CONVERTIR A CLASIFICACIÓN
# -------------------------
df["lluvia_binaria"] = (df["precip"] > 0).astype(int)

y = df["lluvia_binaria"]
X = df.drop(columns=["precip", "lluvia_binaria"])

# Escalar datos
scaler = StandardScaler()
X = scaler.fit_transform(X)

# División
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("🧠 Entrenando modelo de clasificación...")

model = SGDClassifier(
    loss="log_loss",
    max_iter=1,
    warm_start=True,
    random_state=42
)

epochs = 30
train_losses, val_losses = [], []
train_acc, val_acc = [], []
train_f1, val_f1 = [], []

# Iniciamos la corrida con un nombre profesional
with mlflow.start_run(run_name="Ejecucion_Final_Modelo"):

    mlflow.log_param("model_type", "SGDClassifier")
    mlflow.log_param("epochs", epochs)

    for epoch in range(epochs):
        model.fit(X_train, y_train)

        # Probabilidades y Predicciones
        train_probs = model.predict_proba(X_train)
        val_probs = model.predict_proba(X_test)
        train_pred = model.predict(X_train)
        val_pred = model.predict(X_test)

        # 1. Función de Costo (Log Loss)
        t_loss = log_loss(y_train, train_probs)
        v_loss = log_loss(y_test, val_probs)
        train_losses.append(t_loss)
        val_losses.append(v_loss)

        # 2. Métrica 1: Accuracy
        t_acc = accuracy_score(y_train, train_pred)
        v_acc = accuracy_score(y_test, val_pred)
        train_acc.append(t_acc)
        val_acc.append(v_acc)

        # 3. Métrica 2: F1-Score (Requisito de la guía)
        t_f1 = f1_score(y_train, train_pred)
        v_f1 = f1_score(y_test, val_pred)
        train_f1.append(t_f1)
        val_f1.append(v_f1)

        # Registro en MLflow por cada paso (step)
        mlflow.log_metric("train_loss", t_loss, step=epoch)
        mlflow.log_metric("val_loss", v_loss, step=epoch)
        mlflow.log_metric("train_accuracy", t_acc, step=epoch)
        mlflow.log_metric("val_accuracy", v_acc, step=epoch)
        mlflow.log_metric("train_f1", t_f1, step=epoch)
        mlflow.log_metric("val_f1", v_f1, step=epoch)

    # Precision final
    precision = precision_score(y_test, val_pred)
    mlflow.log_metric("precision_final", precision)

    # Guardar modelo en MLflow
    mlflow.sklearn.log_model(model, "modelo_clasificacion_lluvia")
    joblib.dump(model, MODEL_PATH)

# -------------------------
# GENERACIÓN DE GRÁFICAS (Doble Traza)
# -------------------------
def save_plot(train_data, val_data, title, filename):
    plt.figure(figsize=(10, 6))
    plt.plot(train_data, label=f"Train {title}", color="blue")
    plt.plot(val_data, label=f"Test {title}", color="red")
    plt.title(f"Evolución de {title}")
    plt.xlabel("Steps")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

save_plot(train_losses, val_losses, "Función de Costo (Loss)", "loss_plot.png")
save_plot(train_acc, val_acc, "Accuracy", "accuracy_plot.png")
save_plot(train_f1, val_f1, "F1-Score", "f1_score_plot.png")

print("✅ Modelo entrenado. Nombre del proyecto: PREDICCION DE LLUVIA IDEAM")