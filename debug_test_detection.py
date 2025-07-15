#!/usr/bin/env python3
"""
Test the specific column detection logic.
"""


def test_column_detection():
    """Test our specific column detection scenarios."""
    print("Testing column detection scenarios...")

    # Test cases based on our actual test data
    test_cases = [
        {
            "name": "percentage_score",
            "values": [0.85, 0.92, 0.78, 0.95],  # Values in 0-1 range
            "expected": "PERCENTAGE",
            "keywords": ["perc", "percentage", "percent", "%", "score", "ratio"],
        },
        {
            "name": "rating_100",
            "values": [85, 92, 78, 95],  # Values NOT in 0-1 range
            "expected": "INTEGER",
            "keywords": ["perc", "percentage", "percent", "%", "score", "ratio"],
        },
        {
            "name": "id_column",
            "values": [1001, 1002, 1003, 1004, 1005],  # Numeric but has "id"
            "expected": "ID",
            "keywords": ["id", "tag", "identification", "serial", "key"],
        },
    ]

    for case in test_cases:
        col_name = case["name"]
        values = case["values"]
        expected = case["expected"]

        print(f"\nTesting: {col_name}")
        print(f"Values: {values}")

        # Check if values are in percentage range (0-1)
        in_percentage_range = all(0 <= x <= 1 for x in values if x is not None)
        print(f"In percentage range (0-1): {in_percentage_range}")

        # Check for keywords
        col_lower = col_name.lower()

        # ID check (should come first)
        id_keywords = ["id", "identification", "serial", "key"]  # Removed "tag"
        has_id_keyword = any(word in col_lower for word in id_keywords)
        print(f"Has ID keyword: {has_id_keyword}")
        if has_id_keyword:
            matching_id_words = [word for word in id_keywords if word in col_lower]
            print(f"  Matching ID words: {matching_id_words}")

        # Percentage check (requires both keyword AND range)
        perc_keywords = ["perc", "percentage", "percent", "%", "score", "ratio"]
        has_percentage_keyword = any(word in col_lower for word in perc_keywords)
        print(f"Has percentage keyword: {has_percentage_keyword}")
        if has_percentage_keyword:
            matching_perc_words = [word for word in perc_keywords if word in col_lower]
            print(f"  Matching percentage words: {matching_perc_words}")

        # Apply our logic
        if has_id_keyword:
            detected = "ID"
        elif in_percentage_range and has_percentage_keyword:
            detected = "PERCENTAGE"
        elif in_percentage_range:
            detected = "PERCENTAGE"
        elif all(isinstance(x, int) or (isinstance(x, float) and x.is_integer()) for x in values if x is not None):
            detected = "INTEGER"
        else:
            detected = "NUMERIC"

        print(f"Expected: {expected}")
        print(f"Detected: {detected}")
        print(f"Match: {'YES' if detected == expected else 'NO'}")

        if detected != expected:
            print(f"ERROR: Mismatch for {col_name}!")

    print("\nDetection logic test completed.")


if __name__ == "__main__":
    test_column_detection()
