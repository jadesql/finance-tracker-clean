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

# ----------------------------
# LOAD DATA
# ----------------------------
df = load_data()

# ----------------------------
# CLEAN CATEGORIES
# ----------------------------
df["category"] = df["category"].astype(str).str.strip().str.lower()

category_map = {
    "food": "Food",
    "fuel": "Fuel",
    "shopping": "Shopping",
    "health": "Health",
    "eating out": "Eating out",
    "eatingout": "Eating out",
    "holidays": "Holidays",
    "holiday": "Holidays"
}

df["category"] = df["category"].replace(category_map)

# ONLY EXPENSES
expenses = df[df["type"] == "expense"].copy()
expenses["amount"] = expenses["amount"].abs()

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Spending Dashboard", layout="wide")

# ----------------------------
# STYLE (DARK + PINK)
# ----------------------------
st.markdown(
    """
    <style>

    .stApp {
        background-color: #0e0e10;
        color: white;
    }

    h1, h2, h3 {
        color: #ff4da6;
    }

    div[data-testid="metric-container"] {
        background-color: #1a1a1d;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0px 0px 10px rgba(255, 77, 166, 0.2);
    }

    div[data-testid="stDataFrame"] {
        border: 2px solid #ff4da6;
        border-radius: 12px;
        padding: 6px;
    }

    div[data-testid="stDataFrame"] * {
        font-size: 18px !important;
    }

    thead tr th {
        background-color: #ff4da6 !important;
        color: white !important;
        font-size: 18px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# TITLE
# ----------------------------
st.title("💸 Monthly Spending Dashboard")

# ----------------------------
# TOTAL SPEND
# ----------------------------
total_spend = expenses["amount"].sum()

st.metric("Total Spending", f"£{total_spend:,.2f}")

# ----------------------------
# CATEGORY TABLE
# ----------------------------
st.subheader("📊 Spending by Category")

category_totals = expenses.groupby("category")["amount"].sum()

category_df = category_totals.reset_index()
category_df.columns = ["Category", "Spent (£)"]

category_df["Spent (£)"] = category_df["Spent (£)"].apply(lambda x: f"£{x:,.2f}")

st.dataframe(category_df, use_container_width=True)

# ----------------------------
# CENTRED SMALL CHART (IMPORTANT FIX)
# ----------------------------
st.subheader("📈 Breakdown")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:

    fig, ax = plt.subplots(figsize=(4.5, 3))

    ax.bar(
        category_totals.index,
        category_totals.values,
        color="#ff4da6"
    )

    ax.set_title("Spending Breakdown", fontsize=14, color="white")
    ax.set_xlabel("Category", fontsize=10, color="white")
    ax.set_ylabel("Amount (£)", fontsize=10, color="white")

    ax.tick_params(axis='x', labelsize=9, colors="white", rotation=20)
    ax.tick_params(axis='y', labelsize=9, colors="white")

    fig.patch.set_facecolor("#0e0e10")
    ax.set_facecolor("#0e0e10")

    st.pyplot(fig)