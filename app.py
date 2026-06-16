import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.title("ATM Financial Simulator – Full Business Model")

# ========================
# INPUTS
# ========================
st.sidebar.header("Customers")

base_customers = st.sidebar.number_input("Customers 2026", value=16)

new_2027 = st.sidebar.number_input("New customers 2027", value=20)
new_2028 = st.sidebar.number_input("New customers 2028", value=30)
new_2029 = st.sidebar.number_input("New customers 2029", value=30)
new_2030 = st.sidebar.number_input("New customers 2030", value=30)

years = [2026, 2027, 2028, 2029, 2030]

# ========================
# PRICING & ASSUMPTIONS
# ========================
st.sidebar.header("Pricing")

price = st.sidebar.number_input("Price per hour", value=180)
upsell = st.sidebar.slider("Upsell rate", 0.0, 0.5, 0.25)

hours_per_customer = 30
auditor_cost = 70

# ========================
# REVENUE INPUTS
# ========================
st.sidebar.header("Revenue")

training_2027 = st.sidebar.number_input("Training 2027", value=0)
training_2028 = st.sidebar.number_input("Training 2028", value=0)
training_2029 = st.sidebar.number_input("Training 2029", value=0)
training_2030 = st.sidebar.number_input("Training 2030", value=0)

travel_rate = 0.15

# ========================
# COST INPUTS
# ========================
st.sidebar.header("Costs")

staff_2027 = st.sidebar.number_input("Personnel 2027", value=0)
staff_2028 = st.sidebar.number_input("Personnel 2028", value=0)
staff_2029 = st.sidebar.number_input("Personnel 2029", value=0)
staff_2030 = st.sidebar.number_input("Personnel 2030", value=0)

marketing_2027 = st.sidebar.number_input("Marketing 2027", value=0)
marketing_2028 = st.sidebar.number_input("Marketing 2028", value=0)
marketing_2029 = st.sidebar.number_input("Marketing 2029", value=0)
marketing_2030 = st.sidebar.number_input("Marketing 2030", value=0)

consult_2027 = st.sidebar.number_input("Consultants 2027", value=0)
consult_2028 = st.sidebar.number_input("Consultants 2028", value=0)
consult_2029 = st.sidebar.number_input("Consultants 2029", value=0)
consult_2030 = st.sidebar.number_input("Consultants 2030", value=0)

insurance = st.sidebar.number_input("Insurance (yearly)", value=3000)
structure = st.sidebar.number_input("Structure / Rent", value=5000)

social_rate = 0.45
travel_cost_rate = 0.10

# ========================
# SIMULATION
# ========================
customers = []
revenues = []
costs = []
profits = []
ebitda_list = []

cust = base_customers

growth = [0, new_2027, new_2028, new_2029, new_2030]
training = [0, training_2027, training_2028, training_2029, training_2030]

staff = [0, staff_2027, staff_2028, staff_2029, staff_2030]
marketing_vals = [0, marketing_2027, marketing_2028, marketing_2029, marketing_2030]
consult_vals = [0, consult_2027, consult_2028, consult_2029, consult_2030]

for i in range(len(years)):

    cust = min(cust + growth[i], 300)
    customers.append(cust)

    # REVENUE
    audit_rev = cust * hours_per_customer * price * (1 + upsell)
    travel_rev = audit_rev * travel_rate
    total_rev = audit_rev + travel_rev + training[i]

    # COSTS
    auditor_cost_total = cust * hours_per_customer * auditor_cost
    staff_total = staff[i] * (1 + social_rate)
    travel_cost = audit_rev * travel_cost_rate

    total_cost = (
        auditor_cost_total +
        staff_total +
        travel_cost +
        marketing_vals[i] +
        consult_vals[i] +
        insurance +
        structure
    )

    # RESULT
    profit_value = total_rev - total_cost
    ebitda_pct = (profit_value / total_rev) * 100 if total_rev > 0 else 0

    revenues.append(total_rev)
    costs.append(total_cost)
    profits.append(profit_value)
    ebitda_list.append(ebitda_pct)

# ========================
# TABLE
# ========================
df = pd.DataFrame({
    "Year": years,
    "Customers": customers,
    "Revenue": revenues,
    "Costs": costs,
    "Profit": profits,
    "EBITDA %": ebitda_list
})

st.subheader("P&L Table")
st.dataframe(df)

# ========================
# CHARTS
# ========================
st.subheader("Profit Evolution")

fig, ax = plt.subplots()
ax.plot(years, profits, marker='o')
ax.axhline(374000, linestyle='--', color='red')
ax.set_title("Profit Evolution")
st.pyplot(fig)

st.subheader("Revenue Breakdown")

fig2, ax2 = plt.subplots()
ax2.bar(years, revenues)
st.pyplot(fig2)

st.subheader("Cost Breakdown")

fig3, ax3 = plt.subplots()
ax3.bar(years, costs)
st.pyplot(fig3)
