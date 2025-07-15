#!/usr/bin/env python3
"""
Debug the scaling issue specifically.
"""


def debug_scaling_logic():
    """Debug what happens in our scaling logic."""
    print("Debugging scaling logic...")

    # Simulate the test scenario
    import sys
    import os

    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

    # Mock the datatype enums
    class DataType:
        PRICE = "price"
        NUMERIC = "numeric"
        PERCENTAGE = "percentage"
        INTEGER = "integer"
        ID = "id"

        def __init__(self, value):
            self.value = value

    # Simulate datatypes from clean_data (enum objects)
    datatypes = {
        "price_USD": DataType("price"),
        "percentage_score": DataType("percentage"),
        "rating_100": DataType("integer"),
        "revenue": DataType("price"),
        "count": DataType("integer"),
        "id_column": DataType("id"),
    }

    # Simulate columns after drop_na
    columns = ["price_USD", "percentage_score", "rating_100", "revenue", "count", "id_column"]

    print("\nChecking which columns should be scaled:")

    for col in columns:
        print(f"\nColumn: {col}")

        # Check ID exclusion logic
        id_excluded = any(word in col.lower() for word in ["id", "identification", "item"])
        print(f"  ID excluded: {id_excluded}")

        if id_excluded:
            print(f"  -> SKIPPED (ID column)")
            continue

        # Check datatype logic
        col_datatype = datatypes[col]
        print(f"  Datatype object: {col_datatype}")
        print(f"  Has .value attr: {hasattr(col_datatype, 'value')}")

        if hasattr(col_datatype, "value"):
            col_datatype_value = col_datatype.value
        else:
            col_datatype_value = col_datatype

        print(f"  Datatype value: '{col_datatype_value}'")

        # Check if should be scaled
        scalable_types = ["price", "numeric", "percentage", "integer"]
        should_scale = col_datatype_value in scalable_types
        print(f"  Should scale: {should_scale}")

        if should_scale:
            print(f"  -> SCALED")
        else:
            print(f"  -> NOT SCALED")

    print("\nThis shows exactly which columns our logic will scale.")


if __name__ == "__main__":
    debug_scaling_logic()
