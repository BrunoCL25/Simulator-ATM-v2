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

