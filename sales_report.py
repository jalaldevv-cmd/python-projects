import pandas as pd


def read_sales(filename):
    return pd.read_csv(filename)


def calculate_report(sales):
    sales["Revenue"] = sales["Price"] * sales["Quantity"]

    total_units = sales["Quantity"].sum()
    total_revenue = sales["Revenue"].sum()

    best_selling = sales.loc[sales["Quantity"].idxmax(), "Product"]

    highest_revenue = sales.loc[sales["Revenue"].idxmax(), "Product"]

    return (total_units, total_revenue, best_selling, highest_revenue)


def display_report(total_units, total_revenue, best_selling, highest_revenue):
    print("\nSales Report")
    print("-" * 30)

    print(f"Total units sold: {total_units}")
    print(f"Total revenue: ₱{total_revenue:.2f}")
    print(f"Best-selling product: {best_selling}")
    print(f"Highest revenue product: {highest_revenue}")


def save_report(total_units, total_revenue, best_selling, highest_revenue):
    report = pd.DataFrame(
        {
            "Metric": [
                "Total Units Sold",
                "Total Revenue",
                "Best-Selling Product",
                "Highest Revenue Product",
            ],
            "Value": [total_units, total_revenue, best_selling, highest_revenue],
        }
    )

    report.to_csv("sales_report.csv", index=False)

    print("\nReport saved to sales_report.csv")


def main():
    sales = read_sales("sales.csv")

    total_units, total_revenue, best_selling, highest_revenue = calculate_report(sales)

    display_report(total_units, total_revenue, best_selling, highest_revenue)
    save_report(total_units, total_revenue, best_selling, highest_revenue)


if __name__ == "__main__":
    main()
