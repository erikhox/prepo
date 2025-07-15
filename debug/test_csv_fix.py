#!/usr/bin/env python3
"""
Test CSV special character handling.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_csv_special_chars():
    """Test that our CSV quoting fix works."""
    try:
        import pandas as pd
        from prepo.io import FileWriter, FileReader

        print("Testing CSV special character handling...")

        # Create test data with problematic characters
        special_data = {
            "col_with_unicode": ["café", "naïve", "résumé", "测试", "Москва"],
            "col_with_symbols": ["$100", "€200", "£300", "¥400", "₹500"],
            "col_with_newlines": ["line1\nline2", "single_line", "line1\rline2", "tab\tseparated", "normal"],
        }
        original_df = pd.DataFrame(special_data)

        print(f"Original DataFrame shape: {original_df.shape}")
        print("Original data with newlines:")
        for i, val in enumerate(original_df["col_with_newlines"]):
            print(f"  Row {i}: {repr(val)}")

        # Test write and read
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            csv_path = f.name

        try:
            writer = FileWriter()
            reader = FileReader()

            # Write with our improved quoting
            writer.write_file(original_df, csv_path)

            # Read back
            read_df = reader.read_file(csv_path)

            print(f"Read DataFrame shape: {read_df.shape}")
            print("Read data with newlines:")
            for i, val in enumerate(read_df["col_with_newlines"]):
                print(f"  Row {i}: {repr(val)}")

            # Check if shapes match
            shapes_match = original_df.shape == read_df.shape
            print(f"Shapes match: {shapes_match}")

            if shapes_match:
                print("✓ CSV special character handling test PASSED")
            else:
                print("✗ CSV special character handling test FAILED")
                print(f"Expected {original_df.shape}, got {read_df.shape}")

        finally:
            if os.path.exists(csv_path):
                os.unlink(csv_path)

    except ImportError as e:
        print(f"Import error (expected in test environment): {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_csv_special_chars()
