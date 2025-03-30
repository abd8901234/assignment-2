import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Loan EMI Calculator", page_icon="💰", layout="wide")
st.markdown(""" <style> body { background-color: #0e1117; color: white; } </style> """, unsafe_allow_html=True)

# Function to calculate EMI (Fixed & Reducing Balance)
def calculate_emi(principal, rate, tenure, method):
    monthly_rate = rate / (12 * 100)  # Convert annual rate to monthly
    months = tenure * 12
    if method == "Fixed Rate":
        emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    else:  # Reducing Balance
        emi = principal / months + (principal * monthly_rate)
    return emi

# Function to generate amortization schedule with optional prepayment
def amortization_schedule(principal, rate, tenure, emi, prepayment=0):
    balance = principal
    months = tenure * 12
    schedule = []
    for i in range(1, months + 1):
        interest = (balance * (rate / (12 * 100)))
        principal_payment = emi - interest
        balance -= principal_payment
        if prepayment and i % 12 == 0:  # Prepayment every year
            balance -= prepayment
        if balance < 0:
            balance = 0
        schedule.append([i, emi, principal_payment, interest, balance])
        if balance == 0:
            break
    return pd.DataFrame(schedule, columns=["Month", "EMI", "Principal Paid", "Interest Paid", "Remaining Balance"])

# Sidebar Inputs for Loan A and Loan B
st.sidebar.header("Loan Comparison Tool")

st.sidebar.subheader("Loan A")
loan_a_amt = st.sidebar.number_input("Loan Amount ($) - A", min_value=1000, max_value=500000, value=100000, step=500)
rate_a = st.sidebar.slider("Interest Rate (%) - A", 1.0, 20.0, 7.5, 0.1)
tenure_a = st.sidebar.slider("Tenure (Years) - A", 1, 30, 10, 1)
method_a = st.sidebar.selectbox("Interest Type - A", ["Fixed Rate", "Reducing Balance"])
prepay_a = st.sidebar.number_input("Annual Prepayment ($) - A", min_value=0, value=0, step=500)

st.sidebar.subheader("Loan B")
loan_b_amt = st.sidebar.number_input("Loan Amount ($) - B", min_value=1000, max_value=500000, value=120000, step=500)
rate_b = st.sidebar.slider("Interest Rate (%) - B", 1.0, 20.0, 8.0, 0.1)
tenure_b = st.sidebar.slider("Tenure (Years) - B", 1, 30, 15, 1)
method_b = st.sidebar.selectbox("Interest Type - B", ["Fixed Rate", "Reducing Balance"])
prepay_b = st.sidebar.number_input("Annual Prepayment ($) - B", min_value=0, value=0, step=500)

# Calculate EMIs
emi_a = calculate_emi(loan_a_amt, rate_a, tenure_a, method_a)
emi_b = calculate_emi(loan_b_amt, rate_b, tenure_b, method_b)

st.write("### Loan EMI Comparison")
col1, col2 = st.columns(2)
col1.metric(label="EMI for Loan A", value=f"${emi_a:.2f}")
col2.metric(label="EMI for Loan B", value=f"${emi_b:.2f}")

# Generate Amortization Schedules
schedule_a = amortization_schedule(loan_a_amt, rate_a, tenure_a, emi_a, prepay_a)
schedule_b = amortization_schedule(loan_b_amt, rate_b, tenure_b, emi_b, prepay_b)

st.write("### Loan Repayment Schedule")
fig = go.Figure()
fig.add_trace(go.Scatter(x=schedule_a["Month"], y=schedule_a["Remaining Balance"], mode='lines', name="Loan A Balance", line=dict(color='cyan')))
fig.add_trace(go.Scatter(x=schedule_b["Month"], y=schedule_b["Remaining Balance"], mode='lines', name="Loan B Balance", line=dict(color='magenta')))
fig.update_layout(title="Remaining Loan Balance Over Time", xaxis_title="Months", yaxis_title="Remaining Balance ($)", template="plotly_dark")
st.plotly_chart(fig)

st.write("### Detailed Amortization Schedules")
col3, col4 = st.columns(2)
col3.write("#### Loan A Schedule")
col3.dataframe(schedule_a)
col4.write("#### Loan B Schedule")
col4.dataframe(schedule_b)

st.markdown("---")
st.write("💡 Tip:** Try prepaying a small amount every year to reduce total interest paid!")