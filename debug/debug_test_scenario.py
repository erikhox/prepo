#!/usr/bin/env python3
"""
Debug the exact test scenario.
"""


def debug_test_scenario():
    """Debug the exact test scenario step by step."""
    print("Debugging exact test scenario...")

    # Simulate the exact test data
    test_data = {
        "date_column": ["2023-01-01", "2023-01-02", None, "2023-01-04", "2023-01-05"],
        "price_USD": [100.50, None, 200.75, 150.25, 300.00],
        "percentage_score": [0.85, 0.92, None, 0.78, 0.95],
        "rating_100": [85, 92, None, 78, 95],
        "is_active": [True, False, None, True, False],
        "category": ["A", "B", None, "A", "C"],
        "revenue": [1000.50, 2000.75, None, 1500.25, 3000.00],
        "count": [10, 15, None, 12, 20],
        "description": ["Product A", None, "Product C", "Product D", "Product E"],
        "id_column": [1001, 1002, 1003, 1004, 1005],
    }

    print("Original data rows:")
    for i, (date, price, perc, rating, active, cat, rev, cnt, desc, id_val) in enumerate(
        zip(
            test_data["date_column"],
            test_data["price_USD"],
            test_data["percentage_score"],
            test_data["rating_100"],
            test_data["is_active"],
            test_data["category"],
            test_data["revenue"],
            test_data["count"],
            test_data["description"],
            test_data["id_column"],
        )
    ):
        has_nan = any(x is None for x in [date, price, perc, rating, active, cat, rev, cnt, desc])
        print(f"Row {i}: date={date}, price={price}, perc={perc}, has_nan={has_nan}")

    print("\nAfter drop_na=True, remaining rows should be:")
    remaining_rows = []
    for i, (date, price, perc, rating, active, cat, rev, cnt, desc, id_val) in enumerate(
        zip(
            test_data["date_column"],
            test_data["price_USD"],
            test_data["percentage_score"],
            test_data["rating_100"],
            test_data["is_active"],
            test_data["category"],
            test_data["revenue"],
            test_data["count"],
            test_data["description"],
            test_data["id_column"],
        )
    ):
        has_nan = any(x is None for x in [date, price, perc, rating, active, cat, rev, cnt, desc])
        if not has_nan:
            remaining_rows.append(i)
            print(f"Row {i}: percentage_score = {perc}")

    # Calculate what the mean should be
    remaining_percentage_values = [test_data["percentage_score"][i] for i in remaining_rows]
    print(f"\nRemaining percentage_score values: {remaining_percentage_values}")
    mean_before_scaling = sum(remaining_percentage_values) / len(remaining_percentage_values)
    print(f"Mean before scaling: {mean_before_scaling}")
    print(f"This matches the error: np.float64({mean_before_scaling:.2f}) != 0")

    print("\nConclusion: percentage_score is NOT being scaled by our scaler method!")


if __name__ == "__main__":
    debug_test_scenario()
