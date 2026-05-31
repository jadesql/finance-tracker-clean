import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# ----------------------------
# DATABASE
# ----------------------------
conn = sqlite3.connect("finance.db", check_same_thread=False)

def load_data():
    return pd.read_sql("SELECT * FROM transactions", conn)

def insert_data(amount, category):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (amount, type, category) VALUES (?, ?, ?)",
        (amount, "expense", category)
    )
    conn.commit()

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Spending Dashboard", layout="wide")

st.title("💸 Monthly Spending Dashboard")

# ----------------------------
# INPUT SECTION (FIXED)
# ----------------------------
with st.form("entry_form"):
    amount = st.number_input("Amount")
    category = st.text_input("Category")
    submitted = st.form_submit_button("Add Entry")

if submitted:
    insert_data(amount, category)
    st.success("Entry added!")

# ----------------------------
# LOAD DATA (AFTER INSERT)
# ----------------------------
df = load_data()

df["category"] = df["category"].astype(str).str.strip().str.lower()

expenses = df[df["type"] == "expense"].copy()
expenses["amount"] = expenses["amount"].abs()

# ----------------------------
# TOTAL
# ----------------------------
st.metric("Total Spending", f"£{expenses['amount'].sum():,.2f}")

# ----------------------------
# TABLE
# ----------------------------
category_totals = expenses.groupby("category")["amount"].sum().reset_index()
category_totals.columns = ["Category", "Spent (£)"]

st.dataframe(category_totals, use_container_width=True)

# ----------------------------
# CHART
# ----------------------------
fig, ax = plt.subplots()

ax.bar(category_totals["Category"], category_totals["Spent (£)"])

st.pyplot(fig)