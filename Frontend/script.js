// ============================================
// AI RISK MANAGER - FRONTEND LOGIC
// ============================================

const API_URL = "http://127.0.0.1:8000";


// ============================================
// GET ELEMENTS
// ============================================

const predictionForm = document.getElementById("predictionForm");
const predictionResult = document.getElementById("predictionResult");


// ============================================
// PREDICTION FORM
// ============================================

predictionForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const button = predictionForm.querySelector(".predict-button");

    // Disable button while processing
    button.disabled = true;

    button.innerHTML = `
        <span>⏳</span>
        Analyzing...
    `;


    // ========================================
    // COLLECT FORM DATA
    // ========================================

    const orderData = {

        order_value: Number(
            document.getElementById("order_value").value
        ),

        customer_orders: Number(
            document.getElementById("customer_orders").value
        ),

        customer_returns: Number(
            document.getElementById("customer_returns").value
        ),

        discount_percent: Number(
            document.getElementById("discount_percent").value
        ),

        delivery_distance_km: Number(
            document.getElementById("delivery_distance_km").value
        ),

        product_category:
            document.getElementById("product_category").value,

        payment_method:
            document.getElementById("payment_method").value,

        days_since_last_order: Number(
            document.getElementById("days_since_last_order").value
        )
    };


    try {

        // ====================================
        // SEND REQUEST TO FASTAPI
        // ====================================

        const response = await fetch(
            `${API_URL}/predict`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(orderData)
            }
        );


        // Check HTTP response

        if (!response.ok) {

            throw new Error(
                `API Error: ${response.status}`
            );

        }


        // Get JSON response

        const result = await response.json();


        // ====================================
        // DISPLAY RESULT
        // ====================================

        displayPrediction(result);


    } catch (error) {

        console.error("Prediction error:", error);

        predictionResult.innerHTML = `

            <div class="error-result">

                <div class="error-icon">
                    ⚠
                </div>

                <div>

                    <strong>
                        Unable to analyze order
                    </strong>

                    <span>
                        Make sure the AI backend is running.
                    </span>

                </div>

            </div>

        `;

    } finally {

        // ====================================
        // RESTORE BUTTON
        // ====================================

        button.disabled = false;

        button.innerHTML = `
            <span>✦</span>
            Analyze Risk
        `;

    }

});


// ============================================
// DISPLAY PREDICTION
// ============================================

function displayPrediction(result) {

    const riskScore = result.risk_score;

    const riskLevel =
        result.risk_level.toLowerCase();


    // ========================================
    // CREATE REASONS
    // ========================================

    const reasonsHTML =
        result.reasons
            .map(reason => `
                <span class="reason">
                    ${reason}
                </span>
            `)
            .join("");


    // ========================================
    // DISPLAY RESULT
    // ========================================

    predictionResult.innerHTML = `

        <div class="result-content">

            <div class="
                risk-score-circle
                ${riskLevel}
            ">

                ${riskScore}%

            </div>


            <div class="result-info">

                <h3>
                    ${result.risk_level} RISK
                </h3>

                <p>
                    ${result.recommendation}
                </p>


                <div class="result-reasons">

                    ${reasonsHTML}

                </div>

            </div>

        </div>

    `;


    // ========================================
    // UPDATE KPI
    // ========================================

    const returnRisk =
        document.getElementById("returnRisk");

    if (returnRisk) {

        returnRisk.textContent =
            `${riskScore}%`;

    }

}


// ============================================
// INITIAL DASHBOARD DATA
// ============================================

async function loadDashboardData() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/dashboard"
        );

        if (!response.ok) {
            throw new Error("Dashboard API failed");
        }

        const data = await response.json();

        // Update Total Orders
const totalOrders =
    document.getElementById("totalOrders");

if (totalOrders) {
    totalOrders.textContent =
        data.total_orders.toLocaleString("en-IN");
}


// Update Risk Distribution
const lowRiskPercent =
    document.getElementById("lowRiskPercent");

const mediumRiskPercent =
    document.getElementById("mediumRiskPercent");

const highRiskPercent =
    document.getElementById("highRiskPercent");

if (lowRiskPercent) {
    lowRiskPercent.textContent =
        data.risk_distribution.low + "%";
}

if (mediumRiskPercent) {
    mediumRiskPercent.textContent =
        data.risk_distribution.medium + "%";
}

if (highRiskPercent) {
    highRiskPercent.textContent =
        data.risk_distribution.high + "%";
}

// Update donut chart
const donutChart =
    document.querySelector(".donut-chart");

if (donutChart) {

    const low = data.risk_distribution.low;
    const medium = data.risk_distribution.medium;
    const high = data.risk_distribution.high;

    donutChart.style.background =
        `conic-gradient(
            #16a979 0% ${low}%,
            #f59e0b ${low}% ${low + medium}%,
            #ef4444 ${low + medium}% 100%
        )`;
}

const donutTotalOrders =
    document.getElementById("donutTotalOrders");

if (donutTotalOrders) {
    donutTotalOrders.textContent =
        data.total_orders.toLocaleString("en-IN");
}

        // Update High Risk Orders
        const highRiskCount =
            document.getElementById("highRiskCount");

        if (highRiskCount) {
            highRiskCount.textContent = data.high_risk;
        }

        // Update Return Risk
        const returnRisk =
            document.getElementById("returnRisk");

        if (returnRisk) {
            returnRisk.textContent =
                data.return_rate + "%";
        }

        // Update High-Risk Order Value
        const potentialLoss =
            document.getElementById("potentialLoss");

        if (potentialLoss) {
            potentialLoss.textContent =
                "₹" +
                data.potential_loss.toLocaleString("en-IN");
        }

        console.log("Dashboard data:", data);

    } catch (error) {

        console.error(
            "Dashboard loading error:",
            error
        );

    }
}


// ============================================
// START DASHBOARD
// ============================================

loadDashboardData();
async function loadHighRiskOrders() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/dashboard"
        );

        if (!response.ok) {
            throw new Error("Failed to load orders");
        }

        const data = await response.json();

        const table =
            document.getElementById("ordersTable");

        if (!table) return;

        table.innerHTML = "";

        data.high_risk_orders.forEach(order => {

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>
                    <strong>#${order.order_id}</strong>
                </td>

                <td>
                    ₹${order.order_value.toLocaleString("en-IN", {
                        maximumFractionDigits: 2
                    })}
                </td>

                <td>
                    ${order.return_rate}%
                </td>

                <td>
                    <div class="table-risk">

                        <div class="mini-progress">
                            <span style="width: ${order.risk_score}%"></span>
                        </div>

                        <strong>
                            ${order.risk_score}%
                        </strong>

                    </div>
                </td>

                <td>
                    <span class="risk-pill high">
                        ${order.risk_level}
                    </span>
                </td>

                <td>
                    ${order.recommendation}
                </td>
                <td>
    <button class="review-btn"
        onclick="reviewOrder('${order.order_id}')">
        Review
    </button>
</td>
            `;

            table.appendChild(row);

        });

        console.log(
            "High-risk orders loaded:",
            data.high_risk_orders
        );

    } catch (error) {

        console.error(
            "High-risk orders loading error:",
            error
        );

    }
}

loadHighRiskOrders();

// ==========================================
// SIDEBAR NAVIGATION
// ==========================================

const navItems = document.querySelectorAll(".nav-item");

navItems.forEach(item => {

    item.addEventListener("click", function(event) {

        const targetId = this.getAttribute("href");

        // Dashboard link
        if (targetId === "#") {

            event.preventDefault();

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });

        }

        // Highlight active navigation item
        navItems.forEach(nav => {
            nav.classList.remove("active");
        });

        this.classList.add("active");

    });

});

// ==========================================
// VIEW ALL ORDERS BUTTON
// ==========================================

const viewAllOrders =
    document.getElementById("viewAllOrders");

if (viewAllOrders) {

    viewAllOrders.addEventListener("click", function() {

        const ordersSection =
            document.getElementById("orders");

        if (ordersSection) {

            ordersSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }

    });

}

// ==========================================
// MODEL PERFORMANCE METRICS
// ==========================================

async function loadModelMetrics() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/metrics"
        );

        if (!response.ok) {
            throw new Error("Failed to load model metrics");
        }

        const data = await response.json();

        // Accuracy
        const accuracy =
            document.getElementById("modelAccuracy");

        if (accuracy) {
            accuracy.textContent =
                data.accuracy + "%";
        }

        // Precision
        const precision =
            document.getElementById("modelPrecision");

        if (precision) {
            precision.textContent =
                data.precision + "%";
        }

        // Recall
        const recall =
            document.getElementById("modelRecall");

        if (recall) {
            recall.textContent =
                data.recall + "%";
        }

        // F1 Score
        const f1 =
            document.getElementById("modelF1");

        if (f1) {
            f1.textContent =
                data.f1_score + "%";
        }

        // False Positives
        const falsePositives =
            document.getElementById("falsePositives");

        if (falsePositives) {
            falsePositives.textContent =
                data.false_positives;
        }

        // False Negatives
        const falseNegatives =
            document.getElementById("falseNegatives");

        if (falseNegatives) {
            falseNegatives.textContent =
                data.false_negatives;
        }

        // Estimated Error Cost
        const errorCost =
            document.getElementById("errorCost");

        if (errorCost) {
            errorCost.textContent =
                "₹" + data.estimated_error_cost
                    .toLocaleString("en-IN");
        }
        document.getElementById("trueNegatives").textContent =
    data.true_negatives;

document.getElementById("matrixFalsePositives").textContent =
    data.false_positives;

document.getElementById("matrixFalseNegatives").textContent =
    data.false_negatives;

document.getElementById("truePositives").textContent =
    data.true_positives;

        console.log(
            "Model metrics loaded:",
            data
        );

    } catch (error) {

        console.error(
            "Model metrics loading error:",
            error
        );

    }
}


// Load metrics when dashboard starts
loadModelMetrics();

function reviewOrder(orderId) {
    alert(
        "Review required for " + orderId +
        "\n\nRecommended action: Review order before dispatch."
    );
}