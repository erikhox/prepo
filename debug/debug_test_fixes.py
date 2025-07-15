#!/usr/bin/env python3
"""
Quick test script to verify our fixes work.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import numpy as np
import pandas as pd
from prepo import DataType, FeaturePreProcessor, ScalerType


def test_datatype_detection():
    """Test that rating_100 is detected as INTEGER, not PERCENTAGE."""
    processor = FeaturePreProcessor()

    test_data = {
        "rating_100": [85, 92, np.nan, 78, 95],
        "percentage_score": [0.85, 0.92, np.nan, 0.78, 0.95],
    }
    df = pd.DataFrame(test_data)

    datatypes = processor.determine_datatypes(df)

    print("Datatype Detection Test:")
    print(f"rating_100: {datatypes['rating_100']} (should be INTEGER)")
    print(f"percentage_score: {datatypes['percentage_score']} (should be PERCENTAGE)")

    assert datatypes["rating_100"] == DataType.INTEGER, f"Expected INTEGER, got {datatypes['rating_100']}"
    assert datatypes["percentage_score"] == DataType.PERCENTAGE, f"Expected PERCENTAGE, got {datatypes['percentage_score']}"
    print("✅ Datatype detection test passed!")


def test_clean_data_drop_na():
    """Test that drop_na correctly drops rows with NaN."""
    processor = FeaturePreProcessor()

    test_data = {
        "date_column": ["2023-01-01", "2023-01-02", np.nan, "2023-01-04", "2023-01-05"],
        "price_USD": [100.50, np.nan, 200.75, 150.25, 300.00],
        "description": ["Product A", np.nan, "Product C", "Product D", "Product E"],
    }
    df = pd.DataFrame(test_data)

    clean_df, datatypes = processor.clean_data(df, drop_na=True)

    print(f"\nClean Data Test:")
    print(f"Original rows: {len(df)}")
    print(f"Cleaned rows: {len(clean_df)} (should be 3)")
    print(f"Rows without NaN: {len(clean_df)}")

    assert len(clean_df) == 3, f"Expected 3 rows, got {len(clean_df)}"
    assert not clean_df.isnull().any().any(), "Found NaN values in cleaned data"
    print("✅ Clean data test passed!")


def test_scaling():
    """Test that standard scaling works correctly."""
    processor = FeaturePreProcessor()

    test_data = {
        "numeric_col": [100.0, 200.0, 300.0, 400.0, 500.0],
        "id_col": [1, 2, 3, 4, 5],  # Should not be scaled
    }
    df = pd.DataFrame(test_data)

    clean_df, datatypes = processor.clean_data(df, drop_na=True)

    # Test standard scaling
    test_df = clean_df.copy()
    datatypes_str = {k: v.value for k, v in datatypes.items()}
    processor.scaler(test_df, "standard", datatypes_str)

    print(f"\nScaling Test:")
    print(f"Original numeric_col mean: {clean_df['numeric_col'].mean()}")
    print(f"Scaled numeric_col mean: {test_df['numeric_col'].mean()} (should be ~0)")
    print(f"ID column changed: {not test_df['id_col'].equals(clean_df['id_col'])}")

    # Check that numeric column is scaled (mean should be close to 0)
    assert abs(test_df["numeric_col"].mean()) < 1e-10, f"Expected mean ~0, got {test_df['numeric_col'].mean()}"
    # Check that ID column is not scaled
    assert test_df["id_col"].equals(clean_df["id_col"]), "ID column should not be scaled"
    print("✅ Scaling test passed!")


if __name__ == "__main__":
    test_datatype_detection()
    test_clean_data_drop_na()
    test_scaling()
    print("\n🎉 All tests passed!")
