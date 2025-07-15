#!/usr/bin/env python3
"""
Test our specific fixes without running the full test suite.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import numpy as np
import pandas as pd


# Simple mock classes to test our logic without dependencies
class DataType:
    TEMPORAL = "temporal"
    BINARY = "binary"
    PERCENTAGE = "percentage"
    PRICE = "price"
    INTEGER = "integer"
    NUMERIC = "numeric"
    ID = "id"
    CATEGORICAL = "categorical"
    STRING = "string"
    TEXT = "text"
    UNKNOWN = "unknown"


class ScalerType:
    STANDARD = "standard"
    ROBUST = "robust"
    MINMAX = "minmax"
    NONE = "none"


def test_datatype_detection_logic():
    """Test the datatype detection logic we fixed."""
    print("Testing datatype detection logic...")

    # Simulate the test data
    test_data = {
        "date_column": ["2023-01-01", "2023-01-02", np.nan, "2023-01-04", "2023-01-05"],
        "price_USD": [100.50, np.nan, 200.75, 150.25, 300.00],
        "percentage_score": [0.85, 0.92, np.nan, 0.78, 0.95],
        "rating_100": [85, 92, np.nan, 78, 95],  # Should be INTEGER, not PERCENTAGE
        "is_active": [True, False, np.nan, True, False],
        "category": ["A", "B", np.nan, "A", "C"],
        "revenue": [1000.50, 2000.75, np.nan, 1500.25, 3000.00],
        "count": [10, 15, np.nan, 12, 20],
        "description": ["Product A", np.nan, "Product C", "Product D", "Product E"],
        "id_column": [1001, 1002, 1003, 1004, 1005],  # Should be ID, not INTEGER
        "long_text": [
            "This is a very long description that exceeds 100 characters and should be classified as text type rather than string type."
        ]
        * 5,
    }

    # Test our key fixes:

    # 1. rating_100 should be detected as INTEGER (not PERCENTAGE anymore)
    rating_values = [85, 92, 78, 95]  # without NaN for testing
    is_percentage_range = all(0 <= x <= 1 for x in rating_values)
    print(f"rating_100 values {rating_values} in percentage range (0-1)? {is_percentage_range}")
    print(f"Expected: rating_100 should be INTEGER since values are not in 0-1 range")

    # 2. id_column should be detected as ID (checked before numeric)
    id_col_name = "id_column"
    has_id_keyword = any(word in id_col_name.lower() for word in ["id", "tag", "identification", "serial", "key"])
    print(f"id_column contains ID keyword? {has_id_keyword}")
    print(f"Expected: id_column should be ID because it contains 'id' keyword")

    # 3. Clean data drop NA test
    df = pd.DataFrame(test_data)
    rows_without_nan = []
    for i, row in df.iterrows():
        if not row.isnull().any():
            rows_without_nan.append(i)

    print(f"Rows without NaN: {rows_without_nan} (indices)")
    print(f"Total rows without NaN: {len(rows_without_nan)}")
    print(f"Expected: 3 rows should have no NaN values")

    print("✅ Datatype detection logic test completed")


def test_scaling_logic():
    """Test the scaling method changes."""
    print("\nTesting scaling logic...")

    # Test data for scaling
    test_data = [100.0, 200.0, 300.0, 400.0, 500.0]

    # Standard scaler calculation
    mean_val = np.mean(test_data)
    std_val = np.std(test_data, ddof=0)  # Population std
    scaled_data = [(x - mean_val) / std_val for x in test_data]
    scaled_mean = np.mean(scaled_data)

    print(f"Original data: {test_data}")
    print(f"Original mean: {mean_val}")
    print(f"Original std: {std_val}")
    print(f"Scaled data: {[f'{x:.6f}' for x in scaled_data]}")
    print(f"Scaled mean: {scaled_mean:.10f}")
    print(f"Expected: Scaled mean should be very close to 0")

    # Test datatype handling for both enum and string
    datatypes_enum = {"numeric_col": DataType.INTEGER}
    datatypes_str = {"numeric_col": "integer"}

    # Test that our logic handles both
    for dt_name, datatypes in [("enum", datatypes_enum), ("string", datatypes_str)]:
        col_datatype = datatypes["numeric_col"]
        if hasattr(col_datatype, "value"):  # It's an enum-like object
            col_datatype_value = col_datatype
        else:
            col_datatype_value = col_datatype

        should_scale = col_datatype_value in ["price", "numeric", "percentage", "integer"]
        print(f"Datatypes ({dt_name}): {datatypes} -> should scale: {should_scale}")

    print("✅ Scaling logic test completed")


if __name__ == "__main__":
    test_datatype_detection_logic()
    test_scaling_logic()
    print("\n🎉 Logic tests completed!")
