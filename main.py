import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/transactions.csv")

def show_data():
    print("\n📄 TRANSACTIONS 📄")
    print(df.to_string(index=False))

def show_summary():
    income = df[df["type"] == "income"]["amount"].sum()
    expenses = df[df["type"] == "expense"]["amount"].sum()
    balance = income + expenses

    print("\n💰 SUMMARY 💰")
    print(f"Income: £{income}")
    print(f"Expenses: £{expenses}")
    print(f"Balance: £{balance}")

def show_chart():
    print("\n📊 Chart loading...")

    categories = df.groupby("category")["amount"].sum()

    plt.figure(figsize=(7,5))
    categories.plot(kind="bar", color="#4ecdc4")

    plt.title("Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (£)")
    plt.xticks(rotation=30)

    plt.tight_layout()
    plt.show()

while True:
    print("\n==== FINANCE TRACKER ====")
    print("1. View data")
    print("2. Summary")
    print("3. Chart")
    print("4. Exit")

    choice = input("Choose: ")

    if choice == "1":
        show_data()
    elif choice == "2":
        show_summary()
    elif choice == "3":
        show_chart()
    elif choice == "4":
        break
