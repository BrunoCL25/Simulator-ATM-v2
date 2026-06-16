import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("ATM Financial Simulator")

# Inputs
base_customers = st.slider("Base customers", 50, 300, 150)
growth = st.slider("New customers / year", 10, 80, 40)
price = st.slider("Price per hour", 120, 250, 180)
upsell = st.slider("Upsell rate", 0.0, 0.5, 0.25)

years = [2026, 2027, 2028, 2029, 2030]

customers = base_customers
profit = []

for y in years:
    customers += growth
    revenue = customers * 30 * price * (1 + upsell)
    cost = customers * 30 * 70 + 150000
    profit.append(revenue - cost)

# Plot
plt.figure()
plt.plot(years, profit)
plt.axhline(374000, linestyle="--")
plt.title("Profit evolution")
st.pyplot(plt)

# Monte Carlo
st.subheader("Risk simulation")
runs = st.slider("Number of simulations", 100, 5000, 1000)

results = []
for i in range(runs):
    g = np.random.normal(growth, 10)
    p = np.random.normal(price, 20)
    u = np.random.normal(upsell, 0.1)

    c = base_customers
    for y in years:
        c += g
        rev = c * 30 * p * (1 + u)
        cost = c * 30 * 70 + 150000
        prof = rev - cost

    results.append(prof)

st.write("Probability to reach 374k:",
         sum(np.array(results) > 374000)/len(results))
