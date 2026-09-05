from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib


# ==========================================
# CREATE API
# ==========================================

app = FastAPI(
    title="AI Return-Risk Manager API",
    description="API for predicting e-commerce return risk",
    version="1.0"
)


# ==========================================
# ENABLE FRONTEND CONNECTION
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# LOAD MODEL
# ==========================================

model = joblib.load("../model/return_risk_model.pkl")


# ==========================================
# REQUEST DATA STRUCTURE
# ==========================================

class OrderData(BaseModel):

    order_value: float
    customer_orders: int
    customer_returns: int
    discount_percent: float
    delivery_distance_km: float
    product_category: str
    payment_method: str
    days_since_last_order: int


# ==========================================
# HOME ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "AI Return-Risk Manager API is running",
        "status": "success"
    }


# ==========================================
# PREDICTION ENDPOINT
# ==========================================

@app.post("/predict")
def predict(order: OrderData):

    # Convert request into dataframe

    data = pd.DataFrame([{
        "order_value": order.order_value,
        "customer_orders": order.customer_orders,
        "customer_returns": order.customer_returns,
        "discount_percent": order.discount_percent,
        "delivery_distance_km": order.delivery_distance_km,
        "product_category": order.product_category,
        "payment_method": order.payment_method,
        "days_since_last_order": order.days_since_last_order
    }])

    # Get probability

    probability = model.predict_proba(data)[0][1]

    risk_score = round(probability * 100, 2)


    # Determine risk level

    if risk_score >= 70:

        risk_level = "HIGH"
        recommendation = "Review order before dispatch"

    elif risk_score >= 40:

        risk_level = "MEDIUM"
        recommendation = "Apply additional verification"

    else:

        risk_level = "LOW"
        recommendation = "Normal processing"


    # ==========================================
    # EXPLANATION
    # ==========================================

    reasons = []

    return_rate = 0

    if order.customer_orders > 0:

        return_rate = (
            order.customer_returns /
            order.customer_orders
        ) * 100


    if return_rate >= 40:

        reasons.append(
            f"High historical return rate ({return_rate:.1f}%)"
        )

    if order.discount_percent >= 40:

        reasons.append(
            "High discount applied"
        )

    if order.order_value >= 10000:

        reasons.append(
            "High-value order"
        )

    if order.payment_method == "COD":

        reasons.append(
            "Cash-on-delivery payment"
        )

    if order.delivery_distance_km >= 20:

        reasons.append(
            "Long delivery distance"
        )

    if not reasons:

        reasons.append(
            "No major individual risk factor detected"
        )


    # ==========================================
    # RETURN RESULT
    # ==========================================

    return {

        "risk_score": risk_score,

        "risk_level": risk_level,

        "recommendation": recommendation,

        "reasons": reasons

    }
    
    # ==========================================
# DASHBOARD STATISTICS ENDPOINT
# ==========================================

@app.get("/dashboard")
def dashboard():

    # Load the real dataset
    df = pd.read_csv("../data/orders.csv")

    # Total number of orders
    total_orders = len(df)

    # Historical return rate
    total_returns = int(df["returned"].sum())

    overall_return_rate = (
        total_returns / total_orders
    ) * 100

    # ==========================================
    # CALCULATE MODEL RISK FOR ALL ORDERS
    # ==========================================

    features = df.drop("returned", axis=1)

    probabilities = model.predict_proba(features)[:, 1]

    risk_scores = probabilities * 100

    # Risk categories
    high_risk = int((risk_scores >= 70).sum())
    medium_risk = int(
        ((risk_scores >= 40) & (risk_scores < 70)).sum()
    )
    low_risk = int((risk_scores < 40).sum())

    # ==========================================
    # POTENTIAL LOSS
    # ==========================================

    # Estimated loss if a high-risk order is returned
    high_risk_orders = df[risk_scores >= 70]

    potential_loss = float(
        high_risk_orders["order_value"].sum()
    )

    # ==========================================
    # RISK PERCENTAGES
    # ==========================================

    low_percentage = (
        low_risk / total_orders
    ) * 100

    medium_percentage = (
        medium_risk / total_orders
    ) * 100

    high_percentage = (
        high_risk / total_orders
    ) * 100
    
        # ==========================================
    # HIGH-RISK ORDER DETAILS
    # ==========================================

    high_risk_details = []

    # Get indexes of high-risk orders
    high_risk_indices = df[risk_scores >= 70].index

    # Show up to 10 highest-risk orders
    sorted_indices = sorted(
        high_risk_indices,
        key=lambda i: risk_scores[i],
        reverse=True
    )[:10]

    for i in sorted_indices:

        customer_orders = df.loc[i, "customer_orders"]
        customer_returns = df.loc[i, "customer_returns"]

        if customer_orders > 0:
            customer_return_rate = (
                customer_returns /
                customer_orders
            ) * 100
        else:
            customer_return_rate = 0

        high_risk_details.append({

            "order_id": f"ORD-{10000 + int(i)}",

            "order_value": float(
                df.loc[i, "order_value"]
            ),

            "return_rate": round(
                customer_return_rate,
                1
            ),

            "risk_score": round(
                float(risk_scores[i]),
                2
            ),

            "risk_level": "HIGH",

            "recommendation": "Review before dispatch"

        })

    # ==========================================
    # RESPONSE
    # ==========================================

    return {

        "total_orders": total_orders,

        "total_returns": total_returns,

        "return_rate": round(
            overall_return_rate,
            2
        ),

        "high_risk": high_risk,

        "medium_risk": medium_risk,

        "low_risk": low_risk,

        "risk_distribution": {

            "low": round(
                low_percentage,
                2
            ),

            "medium": round(
                medium_percentage,
                2
            ),

            "high": round(
                high_percentage,
                2
            )

        },

        "potential_loss": round(
            potential_loss,
            2
        ),
        "high_risk_orders": high_risk_details
        

    }
    
    # ==========================================
# MODEL PERFORMANCE METRICS
# ==========================================

@app.get("/metrics")
def metrics():

    from sklearn.model_selection import train_test_split
    from sklearn.metrics import (
        precision_score,
        recall_score,
        f1_score,
        accuracy_score,
        confusion_matrix
    )

    # Load dataset
    df = pd.read_csv("../data/orders.csv")

    # Separate features and target
    X = df.drop("returned", axis=1)
    y = df["returned"]

    # Recreate the same held-out test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # Predict on held-out test data
    predictions = model.predict(X_test)

    # Calculate metrics
    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    # Confusion matrix
    tn, fp, fn, tp = confusion_matrix(
        y_test,
        predictions
    ).ravel()

    # Business cost assumptions
    false_positive_cost = 50
    false_negative_cost = 500

    total_error_cost = int(
        fp * false_positive_cost
        +
        fn * false_negative_cost
    )

    return {

        "test_samples": len(y_test),

        "accuracy": round(
            accuracy * 100,
            2
        ),

        "precision": round(
            precision * 100,
            2
        ),

        "recall": round(
            recall * 100,
            2
        ),

        "f1_score": round(
            f1 * 100,
            2
        ),

        "true_negatives": int(tn),

        "false_positives": int(fp),

        "false_negatives": int(fn),

        "true_positives": int(tp),

        "false_positive_cost_per_order":
            false_positive_cost,

        "false_negative_cost_per_order":
            false_negative_cost,

        "estimated_error_cost":
            total_error_cost

    }
