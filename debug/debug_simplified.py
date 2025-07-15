#!/usr/bin/env python3
"""
Test our simplified scaler logic.
"""


def test_simplified_logic():
    """Test the simplified scaler logic."""
    print("Testing simplified scaler logic...")

    # Mock data and functions
    class MockDataType:
        def __init__(self, value):
            self.value = value

    def mock_scaler_func(series):
        # Mock standard scaler
        mean_val = sum(series) / len(series)
        std_val = (sum((x - mean_val) ** 2 for x in series) / len(series)) ** 0.5
        if std_val == 0:
            return [x - mean_val for x in series]
        return [(x - mean_val) / std_val for x in series]

    # Test data after drop_na
    test_data = {
        "price_USD": [100.50, 150.25, 300.00],
        "percentage_score": [0.85, 0.78, 0.95],
        "rating_100": [85, 78, 95],
        "revenue": [1000.50, 1500.25, 3000.00],
        "count": [10, 12, 20],
        "id_column": [1001, 1004, 1005],
    }

    # Datatypes from clean_data (enum objects)
    datatypes = {
        "price_USD": MockDataType("price"),
        "percentage_score": MockDataType("percentage"),
        "rating_100": MockDataType("integer"),
        "revenue": MockDataType("price"),
        "count": MockDataType("integer"),
        "id_column": MockDataType("id"),
    }

    print("\nApplying our scaler logic:")

    for col in test_data.keys():
        print(f"\nColumn: {col}")

        # Skip ID columns
        id_excluded = any(word in col.lower() for word in ["id", "identification", "item"])
        if id_excluded:
            print(f"  -> SKIPPED (ID column)")
            continue

        # Handle both enum and string datatypes
        col_datatype = datatypes[col]
        if hasattr(col_datatype, "value"):
            col_datatype_value = col_datatype.value
        else:
            col_datatype_value = col_datatype

        print(f"  Datatype: {col_datatype_value}")

        # Check if column should be scaled
        scalable_types = ["price", "numeric", "percentage", "integer"]
        if col_datatype_value in scalable_types:
            original_values = test_data[col]
            scaled_values = mock_scaler_func(original_values)
            scaled_mean = sum(scaled_values) / len(scaled_values)

            print(f"  Original: {original_values}")
            print(f"  Scaled: {[f'{x:.6f}' for x in scaled_values]}")
            print(f"  Scaled mean: {scaled_mean:.10f}")
            print(f"  -> SCALED")
        else:
            print(f"  -> NOT SCALED")

    print("\nExpected result: percentage_score should be scaled with mean ≈ 0")


if __name__ == "__main__":
    test_simplified_logic()
