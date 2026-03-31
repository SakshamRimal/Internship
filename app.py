import json
from datetime import datetime

FILE = "data.json"

#-------load_data ------------------------
def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {"expenses": [], "budget": 0}


def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------- features ----------
def add_expense():
    data = load_data()

    amount = float(input("Enter amount: "))
    category = input("Enter category: ")
    note = input("Enter note: ")

    expense = {
        "amount": amount,
        "category": category,
        "note": note,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    data["expenses"].append(expense)
    save_data(data)

    print("Expense added!")

#----------view expenses----------
def view_expenses():
    data = load_data()

    if not data["expenses"]:
        print("No expenses found")
        return

    print("\n--- History ---")
    for e in data["expenses"]:
        print(f"{e['date']} | {e['category']} | Rs.{e['amount']} | {e['note']}")


def set_budget():
    data = load_data()

    budget = float(input("Enter budget: "))
    data["budget"] = budget

    save_data(data)
    print("Budget saved")


def check_budget():
    data = load_data()

    total = sum(e["amount"] for e in data["expenses"])
    budget = data["budget"]

    print(f"Total: Rs.{total}")
    print(f"Budget: Rs.{budget}")

    if budget == 0:
        print("No budget set")
    elif total > budget:
        print("Budget exceeded!")
    else:
        print(f"Remaining: Rs.{budget - total}")


def filter_category():
    data = load_data()

    cat = input("Enter category: ")
    found = False

    for e in data["expenses"]:
        if e["category"] == cat:
            print(f"{e['date']} | Rs.{e['amount']} | {e['note']}")
            found = True

    if not found:
        print("No expenses in this category")


# ---------- menu ----------
while True:
    print("\n1.Add  2.View  3.Set Budget  4.Check  5.Filter  6.Exit")
    choice = input("Choice: ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        set_budget()
    elif choice == "4":
        check_budget()
    elif choice == "5":
        filter_category()
    elif choice == "6":
        break
    else:
        print("Invalid choice")
