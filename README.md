# 🛡️ AI Risk Manager

> **AI-powered return-risk scoring for e-commerce orders**

AI Risk Manager is a full-stack machine-learning application that helps e-commerce businesses identify potentially high-risk orders **before dispatch**. Instead of treating every order equally, the system analyzes customer and order behavior, assigns a return-risk score, explains important risk factors, and recommends an appropriate operational action.

The project is designed as a **defense-oriented hackathon prototype** with measurable performance on a held-out test set and explicit business error-cost analysis.

---

## ✨ Why AI Risk Manager?

E-commerce businesses can lose money and operational time when orders are returned unexpectedly. Manual verification of every order is expensive and inefficient, while ignoring risky orders can increase potential exposure.

AI Risk Manager creates a practical decision-support workflow:

```text
Customer + Order Data
        ↓
Machine Learning Model
        ↓
Return Risk Score
        ↓
LOW / MEDIUM / HIGH
        ↓
Explanation + Recommended Action
        ↓
Business Review / Verification
```

---

# 🚀 Key Features

### 🤖 AI Return-Risk Prediction
Predicts the probability that an order may be associated with return risk.

### 📊 Interactive Risk Dashboard
Provides a visual overview of:
- Total orders
- Return rate
- High-risk orders
- Risk distribution
- High-risk order value exposure

### 🔎 Explainable Risk Factors
The prediction response provides reasons such as:
- High historical return rate
- High discount applied
- Cash-on-delivery payment
- High order value
- Long delivery distance

### ⚠️ Risk-Based Actions

| Risk | Score | Recommended Action |
|---|---:|---|
| 🟢 LOW | `< 40%` | Normal processing |
| 🟡 MEDIUM | `40%–69%` | Apply additional verification |
| 🔴 HIGH | `≥ 70%` | Review order before dispatch |

### 📈 Model Performance Monitoring
The dashboard reports:
- Accuracy
- Precision
- Recall
- F1 Score
- False Positives
- False Negatives
- Estimated Error Cost
- Confusion Matrix

### 👀 High-Risk Order Review
High-risk orders are displayed in a dedicated table with a **Review** action.

---

# 🧠 Machine Learning

The project uses a **Random Forest Classifier** with preprocessing through a Scikit-learn pipeline.

### Input Features

The model uses:

| Feature | Description |
|---|---|
| `order_value` | Monetary value of the order |
| `customer_orders` | Number of previous customer orders |
| `customer_returns` | Number of previous returns |
| `discount_percent` | Discount applied to the order |
| `delivery_distance_km` | Delivery distance |
| `product_category` | Product category |
| `payment_method` | Payment method |
| `days_since_last_order` | Days since customer's previous order |

The customer return history is also used to provide an interpretable return-rate signal.

---

# 📊 Model Evaluation

The model is evaluated on a **held-out test set of 1,000 samples**.

> These are the measured results of the current model. They are intentionally reported without artificially optimizing or inflating the numbers.

| Metric | Result |
|---|---:|
| **Accuracy** | **62.50%** |
| **Precision** | **55.71%** |
| **Recall** | **48.08%** |
| **F1 Score** | **51.61%** |

## Confusion Matrix

| Actual / Predicted | Negative | Positive |
|---|---:|---:|
| **Actual Negative** | **409** | **159** |
| **Actual Positive** | **216** | **200** |

### Interpretation

- **True Negatives:** 409
- **False Positives:** 159
- **False Negatives:** 216
- **True Positives:** 200

The confusion matrix makes the model's mistakes visible instead of reporting accuracy alone.

---

# 💰 Business Error Cost

Not every model error has the same business impact.

For this prototype:

```text
False Positive = ₹50
False Negative = ₹500
```

Therefore:

```text
Estimated Error Cost
= (False Positives × ₹50)
  + (False Negatives × ₹500)

= (159 × ₹50) + (216 × ₹500)

= ₹115,950
```

### Why use different costs?

A false positive may cause an unnecessary review of a normal order.

A false negative means a genuinely risky order was missed, which can have a considerably larger business impact.

This cost-sensitive view makes the evaluation more relevant to a real business decision than accuracy alone.

---

# 🖥️ Application Architecture

```text
┌──────────────────────────┐
│       Frontend           │
│   HTML + CSS + JS        │
└────────────┬─────────────┘
             │ HTTP / JSON
             ▼
┌──────────────────────────┐
│       FastAPI            │
│   Prediction + Metrics   │
│       + Dashboard        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│   Scikit-learn Pipeline  │
│  Preprocessing + Random  │
│      Forest Classifier   │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       orders.csv         │
│       Training Data      │
└──────────────────────────┘
```

---

# 📁 Project Structure

```text
AI-Risk-Manager/
│
├── backend/
│   ├── generate_data.py       # Generate dataset
│   ├── inspect_data.py        # Inspect dataset
│   ├── train_model.py         # Train and evaluate ML model
│   └── app.py                 # FastAPI application
│
├── frontend/
│   ├── index.html             # Dashboard UI
│   ├── style.css              # Dashboard styling
│   └── script.js              # Frontend/API integration
│
├── data/
│   └── orders.csv             # Order dataset
│
├── model/
│   └── return_risk_model.pkl  # Trained ML model
│
└── README.md
```

---

# ⚙️ Requirements

Before running the project, make sure you have:

- Python 3.x
- VS Code
- A modern web browser
- VS Code Live Server or another local HTTP server

Python packages used by the backend include:

```text
pandas
scikit-learn
fastapi
uvicorn
joblib
```

If required, install them with:

```powershell
pip install pandas scikit-learn fastapi uvicorn joblib
```

---

# ▶️ How to Run

## Step 1 — Open the Project

Open the `AI-Risk-Manager` folder in VS Code.

---

## Step 2 — Start the Backend

Open a terminal:

```powershell
cd backend
python -m uvicorn app:app --reload
```

You should see the FastAPI server running.

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

**Keep this terminal running.**

---

## Step 3 — Start the Frontend

Open the `frontend` folder in VS Code.

Right-click:

```text
index.html
```

and select:

```text
Open with Live Server
```

The frontend will normally open at something similar to:

```text
http://127.0.0.1:5500
```

> The port may be different on your computer. Use the URL shown by Live Server.

---

# 🧪 How to Test the Project

The project can be tested through both the API and the dashboard.

---

## Test 1 — Backend Health

Open:

```text
http://127.0.0.1:8000
```

Confirm that the backend responds successfully.

---

## Test 2 — API Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

You should see these endpoints:

```text
GET  /
POST /predict
GET  /dashboard
GET  /metrics
```

---

## Test 3 — Test `/predict`

In Swagger:

1. Open `POST /predict`
2. Click **Try it out**
3. Enter this sample:

```json
{
  "order_value": 8999,
  "customer_orders": 12,
  "customer_returns": 7,
  "discount_percent": 40,
  "delivery_distance_km": 18,
  "product_category": "Electronics",
  "payment_method": "COD",
  "days_since_last_order": 5
}
```

4. Click **Execute**.

### Expected Result

The current model returns approximately:

```text
Risk Score: 54.26%
Risk Level: MEDIUM
Recommendation: Apply additional verification
```

The response also includes the model-generated reasons.

---

## Test 4 — Test `/dashboard`

Open:

```text
http://127.0.0.1:8000/dashboard
```

Confirm that the API returns dashboard information including:

- Total orders
- Total returns
- Overall return rate
- High-risk count
- Medium-risk count
- Low-risk count
- Risk distribution
- High-risk orders

---

## Test 5 — Test `/metrics`

Open:

```text
http://127.0.0.1:8000/metrics
```

Verify that it returns the model evaluation information.

Expected current values:

```text
Test Samples       : 1000
Accuracy           : 62.50%
Precision          : 55.71%
Recall             : 48.08%
F1 Score           : 51.61%

True Negatives     : 409
False Positives    : 159
False Negatives    : 216
True Positives     : 200

Estimated Error Cost: ₹115,950
```

---

# 🖱️ Frontend Testing Checklist

After opening the dashboard, verify the following:

### Dashboard

- [ ] High Risk Orders KPI loads
- [ ] Return Risk KPI loads
- [ ] High-Risk Order Value loads
- [ ] Risk Overview chart loads
- [ ] Risk percentages update
- [ ] Model Performance loads
- [ ] Confusion Matrix loads

### Risk Prediction

- [ ] Enter an order
- [ ] Click the prediction button
- [ ] Risk score appears
- [ ] Risk level appears
- [ ] Recommendation appears
- [ ] Risk reasons appear

### High-Risk Orders

- [ ] High-risk order table loads
- [ ] Order values appear
- [ ] Customer return rates appear
- [ ] Risk scores appear
- [ ] HIGH status appears
- [ ] Review button works

---

# 🎬 Recommended Hackathon Demo

For a clean 3–5 minute demonstration, use this sequence:

### 1. Start with the Problem

Explain:

> E-commerce businesses don't need to manually verify every order. The goal is to identify potentially risky orders early and focus attention where it matters.

### 2. Show the Dashboard

Point out:

- Overall order volume
- Return risk
- High-risk orders
- Risk distribution

### 3. Show Model Performance

Explain:

- The model is evaluated on 1,000 held-out samples.
- Accuracy is 62.50%.
- Precision is 55.71%.
- Recall is 48.08%.
- F1 is 51.61%.

### 4. Show the Confusion Matrix

Explain that the system explicitly tracks:

```text
409 True Negatives
159 False Positives
216 False Negatives
200 True Positives
```

### 5. Show Business Impact

Mention:

```text
False Positive Cost = ₹50
False Negative Cost = ₹500
Estimated Error Cost = ₹115,950
```

### 6. Demonstrate a Prediction

Use:

```text
Order Value       = ₹8,999
Previous Orders   = 12
Previous Returns  = 7
Discount          = 40%
Distance          = 18 km
Category          = Electronics
Payment           = COD
Days Since Order  = 5
```

Show:

```text
54.26% → MEDIUM
```

Then explain the reasons behind the score.

### 7. Demonstrate the Review Workflow

Open the High-Risk Orders table and click **Review**.

This demonstrates that the model is not just producing a number—it supports an operational decision.

---

# 🔌 API Reference

## `GET /`

Backend health check.

---

## `POST /predict`

Predict return risk for an individual order.

### Request

```json
{
  "order_value": 8999,
  "customer_orders": 12,
  "customer_returns": 7,
  "discount_percent": 40,
  "delivery_distance_km": 18,
  "product_category": "Electronics",
  "payment_method": "COD",
  "days_since_last_order": 5
}
```

### Response

```json
{
  "risk_score": 54.26,
  "risk_level": "MEDIUM",
  "recommendation": "Apply additional verification",
  "reasons": [
    "High historical return rate (58.3%)",
    "High discount applied",
    "Cash-on-delivery payment"
  ]
}
```

---

## `GET /dashboard`

Returns dashboard-level risk statistics and high-risk order information.

---

## `GET /metrics`

Returns model performance and business evaluation information.

---

# 🔄 Retrain the Model

If the dataset is changed or a new model needs to be trained:

```powershell
cd backend
python train_model.py
```

The trained model is saved as:

```text
model/return_risk_model.pkl
```

After retraining, restart the FastAPI backend before testing the updated model.

---

# 🔍 Inspect the Dataset

Run:

```powershell
cd backend
python inspect_data.py
```

This provides information such as:

- Dataset shape
- Columns
- Data types
- Missing values
- Duplicate records
- Target distribution
- Descriptive statistics

---

# 🧩 Design Principles

### 1. Risk-Based Decision Making

The system prioritizes potentially risky orders instead of treating all orders identically.

### 2. Explainability

The prediction includes understandable risk factors instead of showing only a probability.

### 3. Measurable Performance

The model is evaluated using a held-out test set.

### 4. Business-Aware Evaluation

False positives and false negatives are assigned different costs.

### 5. Defense-Oriented

The system is designed to reduce business losses and improve order verification. It does not provide methods for conducting fraud or abusing e-commerce systems.

---

# ⚠️ Limitations

This project is a hackathon/academic prototype.

- Model performance depends on the quality of the available data.
- Synthetic or limited datasets may not represent real-world customer behavior.
- A production deployment would require validation on representative real-world data.
- Thresholds should be calibrated according to business requirements.
- Estimated error cost depends on the selected business cost assumptions.
- High-Risk Order Value represents **risk exposure**, not confirmed financial loss.
- A model prediction should support, not blindly replace, appropriate business review.

---

# 🛣️ Future Improvements

Possible next steps include:

- Real-time order-stream integration
- Larger and more representative datasets
- Model comparison with XGBoost/Gradient Boosting
- Threshold optimization based on business cost
- SHAP-based explanations
- Customer-level risk history
- Automated verification workflows
- Authentication and role-based access
- Database integration
- Production monitoring and model drift detection
- A/B testing of risk thresholds
- Historical risk-performance tracking

---

# 📌 Project Status

| Component | Status |
|---|---|
| Dataset | ✅ Ready |
| Data inspection | ✅ Ready |
| ML training | ✅ Ready |
| Random Forest model | ✅ Ready |
| FastAPI backend | ✅ Ready |
| Prediction API | ✅ Ready |
| Dashboard API | ✅ Ready |
| Metrics API | ✅ Ready |
| Frontend dashboard | ✅ Ready |
| Risk visualization | ✅ Ready |
| Model performance panel | ✅ Ready |
| Confusion matrix | ✅ Ready |
| High-risk review action | ✅ Ready |
| End-to-end testing | ✅ Ready |

---

# 🏆 Hackathon Value Proposition

**AI Risk Manager turns raw order data into an actionable risk-management workflow.**

Instead of asking:

> *“Which orders have already caused losses?”*

the system helps answer:

> **“Which orders deserve attention before we dispatch them?”**

That shift enables businesses to prioritize verification, reduce unnecessary manual effort, and make risk-aware operational decisions.

---

## 📄 License

This project is developed as a **hackathon/academic prototype**.
