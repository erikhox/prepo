#!/usr/bin/env python3
"""
Test the real DataType enum behavior.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    from prepo.types import DataType

    print("Testing real DataType enum behavior...")

    # Create enum instances like clean_data would
    percentage_enum = DataType.PERCENTAGE
    price_enum = DataType.PRICE

    print(f"DataType.PERCENTAGE: {percentage_enum}")
    print(f"Type: {type(percentage_enum)}")
    print(f"Has .value attr: {hasattr(percentage_enum, 'value')}")
    print(f"Value: {percentage_enum.value}")
    print(f"isinstance(DataType): {isinstance(percentage_enum, DataType)}")

    # Test our logic
    col_datatype = percentage_enum
    if hasattr(col_datatype, "value"):
        col_datatype_value = col_datatype.value
    else:
        col_datatype_value = col_datatype

    print(f"Extracted value: '{col_datatype_value}'")

    scalable_types = [
        DataType.PRICE.value,
        DataType.NUMERIC.value,
        DataType.PERCENTAGE.value,
        DataType.INTEGER.value,
    ]
    print(f"Scalable types: {scalable_types}")

    should_scale = col_datatype_value in scalable_types
    print(f"Should scale: {should_scale}")

except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Error: {e}")
