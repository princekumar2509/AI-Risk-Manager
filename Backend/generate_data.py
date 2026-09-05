import pandas as pd
import numpy as np

np.random.seed(42)

N = 5000

# Customer behavior
customer_orders = np.random.randint(1, 50, N)

customer_return_rate = np.random.beta(2, 8, N)
customer_returns = np.minimum(
    np.round(customer_orders * customer_return_rate).astype(int),
    customer_orders
)

# Order information
order_value = np.random.lognormal(mean=7.5, sigma=0.7, size=N)
order_value = np.clip(order_value, 300, 30000).round(2)

discount_percent = np.random.randint(0, 61, N)

delivery_distance_km = np.random.gamma(
    shape=2,
    scale=5,
    size=N
).round(1)

product_category = np.random.choice(
    ["Electronics", "Clothing", "Footwear", "Home", "Books"],
    N,
    p=[0.20, 0.30, 0.20, 0.15, 0.15]
)

payment_method = np.random.choice(
    ["UPI", "Credit Card", "Debit Card", "COD"],
    N,
    p=[0.40, 0.25, 0.20, 0.15]
)

days_since_last_order = np.random.randint(1, 91, N)

# -----------------------------
# Create return probability
# -----------------------------

return_rate = customer_returns / customer_orders

risk_score = (
    1.5 * return_rate
    + 0.8 * (discount_percent / 100)
    + 0.3 * (order_value / 30000)
    + 0.15 * (delivery_distance_km / 30)
    + 0.4 * (payment_method == "COD")
    + 0.3 * (product_category == "Clothing")
    + np.random.normal(0, 0.25, N)
)

# Convert score into probability
probability = 1 / (1 + np.exp(-3 * (risk_score - 0.9)))

# Generate target
returned = np.random.binomial(1, probability)

# -----------------------------
# Create dataframe
# -----------------------------

df = pd.DataFrame({
    "order_value": order_value,
    "customer_orders": customer_orders,
    "customer_returns": customer_returns,
    "discount_percent": discount_percent,
    "delivery_distance_km": delivery_distance_km,
    "product_category": product_category,
    "payment_method": payment_method,
    "days_since_last_order": days_since_last_order,
    "returned": returned
})

# Save dataset
output_path = "../data/orders.csv"

df.to_csv(output_path, index=False)

print("Dataset generated successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {output_path}")
print()
print("Return distribution:")
print(df["returned"].value_counts())