import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.title("ATM Financial Simulator – Full P&L Model")

# ======================
# INPUTS
# ======================

st.sidebar.header("Business Parameters")

base_customers = st.sidebar.slider("Initial customers", 1, 50, 16)
new_customers = st.sidebar.slider("New customers / year", 0, 100, 40)

price_per_hour = st.sidebar.slider("Price per hour (CHF)", 120, 250, 180)
hours_per_customer = 30

upsell = st.sidebar.slider("Upsell rate", 0.0, 0.5, 0.25)

# Revenues
training_revenue = st.sidebar.slider("Training revenue / year", 0, 100000, 50000)
travel_revenue_rate = 0.15  # 15%

# Costs
auditor_cost = 70
fixed_staff_cost = st.sidebar.slider("Fixed personnel cost", 50000, 200000, 100000)
social_rate = 0.45
marketing = st.sidebar.slider("Marketing", 10000, 100000, 30000)
external_consult = st.sidebar.slider("External consultants", 10000, 50000, 25000)
insurance = st.sidebar.slider("Insurance", 1000, 10000, 3000)
structure_cost = st.sidebar.slider("Structure / rent", 2000, 10000, 5000)
travel_cost_rate = 0.10

years = np.arange(2026, 2031)

# ======================
# MODEL
# ======================

customers = []
revenue_total = []
cost_total = []
profit = []

current_customers = base_customers

for y in years:
    
    # Customers growth (capped at 300)
    current_customers = min(current_customers + new_customers, 300)
    customers.append(current_customers)

    # ===== REVENUE =====
    audit_revenue = current_customers * hours_per_customer * price_per_hour * (1 + upsell)
    travel_revenue = audit_revenue * travel_revenue_rate

    total_revenue = audit_revenue + training_revenue + travel_revenue

    # ===== COSTS =====
    auditor_cost_total = current_customers * hours_per_customer * auditor_cost
    staff_cost_total = fixed_staff_cost * (1 + social_rate)
    travel_cost = audit_revenue * travel_cost_rate

    total_cost = (
        auditor_cost_total +
        staff_cost_total +
        travel_cost +
        marketing +
        external_consult +
        insurance +
        structure_cost
    )

    # ===== PROFIT =====
    profit_value = total_revenue - total_cost

    revenue_total.append(total_revenue)
    cost_total.append(total_cost)
    profit.append(profit_value)

# ======================
# DISPLAY
# ======================

df = pd.DataFrame({
    "Year": years,
    "Customers": customers,
    "Revenue": revenue_total,
    "Costs": cost_total,
    "Profit": profit
})

st.subheader("P&L Overview")
st.dataframe(df)

# Chart
fig, ax = plt.subplots()
ax.plot(years, profit, label="Profit")
ax.axhline(374000, linestyle='--', color='red', label="Target 374k")
ax.legend()
ax.set_title("Profit evolution")
st.pyplot(fig)

# ======================
# MONTE CARLO
# ======================

st.subheader("Monte Carlo – Risk Analysis")

runs = st.slider("Number of simulations", 100, 5000, 1000)

results = []

for i in range(runs):
    
    g = np.random.normal(new_customers, 10)
    p = np.random.normal(price_per_hour, 20)
    u = np.random.normal(upsell, 0.1)

    cust = base_customers

    for y in years:
        cust = min(cust + g, 300)

        audit_rev = cust * hours_per_customer * p * (1 + u)
        travel_rev = audit_rev * travel_revenue_rate

        revenue = audit_rev + training_revenue + travel_rev

        auditor_c = cust * hours_per_customer * auditor_cost
        travel_c = audit_rev * travel_cost_rate
        staff_c = fixed_staff_cost * (1 + social_rate)

        cost = (
            auditor_c +
            travel_c +
            staff_c +
            marketing +
            external_consult +
            insurance +
            structure_cost
        )

        prof = revenue - cost

    results.append(prof)

results = np.array(results)

st.metric("Probability to reach 374k", f"{np.mean(results > 374000)*100:.1f}%")

fig2, ax2 = plt.subplots()
ax2.hist(results, bins=40)
ax2.axvline(374000, linestyle='--', color='red')
st.pyplot(fig2)
