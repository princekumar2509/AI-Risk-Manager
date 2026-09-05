import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv("../data/orders.csv")

print("=" * 60)
print("AI RETURN-RISK MANAGER")
print("MODEL TRAINING")
print("=" * 60)

# ==========================================
# 2. FEATURES AND TARGET
# ==========================================

X = df.drop("returned", axis=1)
y = df["returned"]

# ==========================================
# 3. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nDataset split:")
print(f"Training samples: {len(X_train)}")
print(f"Testing samples:  {len(X_test)}")

# ==========================================
# 4. IDENTIFY COLUMN TYPES
# ==========================================

categorical_features = [
    "product_category",
    "payment_method"
]

numerical_features = [
    "order_value",
    "customer_orders",
    "customer_returns",
    "discount_percent",
    "delivery_distance_km",
    "days_since_last_order"
]

# ==========================================
# 5. PREPROCESSING
# ==========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)

# ==========================================
# 6. RANDOM FOREST MODEL
# ==========================================

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    min_samples_split=5,
    random_state=42,
    class_weight="balanced"
)

# ==========================================
# 7. CREATE PIPELINE
# ==========================================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)

# ==========================================
# 8. TRAIN
# ==========================================

print("\nTraining model...")

pipeline.fit(X_train, y_train)

print("Training complete!")

# ==========================================
# 9. PREDICTIONS
# ==========================================

y_pred = pipeline.predict(X_test)

# Probability of return
y_probability = pipeline.predict_proba(X_test)[:, 1]

# ==========================================
# 10. EVALUATION
# ==========================================

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(f"\nAccuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ==========================================
# 11. FALSE POSITIVE / FALSE NEGATIVE COST
# ==========================================

tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

# Example business costs
false_positive_cost = 50
false_negative_cost = 500

fp_cost = fp * false_positive_cost
fn_cost = fn * false_negative_cost

print("\n" + "=" * 60)
print("BUSINESS COST ANALYSIS")
print("=" * 60)

print(f"\nFalse Positives: {fp}")
print(f"False Negatives: {fn}")

print(
    f"\nFalse-positive cost: "
    f"₹{false_positive_cost} × {fp} = ₹{fp_cost}"
)

print(
    f"False-negative cost: "
    f"₹{false_negative_cost} × {fn} = ₹{fn_cost}"
)

print(f"\nTotal estimated error cost: ₹{fp_cost + fn_cost}")

# ==========================================
# 12. SAVE MODEL
# ==========================================

model_path = "../model/return_risk_model.pkl"

joblib.dump(pipeline, model_path)

print("\nModel saved successfully!")
print(f"Location: {model_path}")

print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)