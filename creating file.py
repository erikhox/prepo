import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta


def create_messy_numerical_csv(filename="messy_numerical_data.csv", n_rows=1000):
    """
    Create a messy numerical CSV file for testing data preprocessing.

    Args:
        filename: Name of the CSV file to create
        n_rows: Number of rows to generate

    Returns:
        DataFrame that was saved to CSV
    """

    # Set random seed for reproducibility
    np.random.seed(42)
    random.seed(42)

    # Define various null/error representations that will appear as strings
    error_values = ["?", "Error", "na", "NA", "ERROR", "error", "err", "ERR",
                    "NAType", "natype", "UNKNOWN", "unknown", "", "N/A", "null",
                    "NULL", "#DIV/0!", "#N/A", "nan", "NaN", "missing", "MISSING"]

    print(f"Generating {n_rows} rows of messy numerical data...")

    # 1. Product ID (should be skipped by your processor)
    product_ids = [f"PROD_{i:05d}" for i in range(1, n_rows + 1)]

    # 2. Price with currency symbols, missing values, and negatives
    prices = np.random.normal(25.50, 8.75, n_rows)
    prices = np.abs(prices)  # Start with positive prices

    # Convert to object array to allow mixed types
    prices = prices.astype(object)

    # Add some negative prices (errors)
    neg_idx = np.random.choice(n_rows, size=int(n_rows * 0.03), replace=False)
    prices[neg_idx] = -np.abs(prices[neg_idx].astype(float))

    # Add extreme outliers
    outlier_idx = np.random.choice(n_rows, size=int(n_rows * 0.02), replace=False)
    prices[outlier_idx] = np.random.choice([0.01, 999.99, 1500.00, 2000.00])

    # Add missing values
    missing_idx = np.random.choice(n_rows, size=int(n_rows * 0.12), replace=False)
    for idx in missing_idx:
        prices[idx] = np.random.choice(error_values)

    # 3. Revenue with extreme outliers and scientific notation issues
    revenue = np.random.lognormal(mean=8.5, sigma=1.5, size=n_rows)

    # Convert to object array to allow mixed types
    revenue = revenue.astype(object)

    # Add extreme outliers
    extreme_idx = np.random.choice(n_rows, size=int(n_rows * 0.04), replace=False)
    revenue[extreme_idx] = revenue[extreme_idx].astype(float) * 100  # Make some values extremely large

    # Add some zero/negative revenue (business errors)
    zero_idx = np.random.choice(n_rows, size=int(n_rows * 0.02), replace=False)
    revenue[zero_idx] = 0

    neg_rev_idx = np.random.choice(n_rows, size=int(n_rows * 0.01), replace=False)
    revenue[neg_rev_idx] = -np.abs(revenue[neg_rev_idx].astype(float))

    # Add missing values
    rev_missing_idx = np.random.choice(n_rows, size=int(n_rows * 0.15), replace=False)
    for idx in rev_missing_idx:
        revenue[idx] = np.random.choice(error_values)

    # 4. Rating percentage (0-1) with values outside valid range
    rating_perc = np.random.beta(3, 2, n_rows)  # Beta distribution for percentage

    # Convert to object array to allow mixed types
    rating_perc = rating_perc.astype(object)

    # Add invalid percentages
    invalid_idx = np.random.choice(n_rows, size=int(n_rows * 0.06), replace=False)
    rating_perc[invalid_idx] = np.random.choice([-0.5, 1.2, 2.0, -1.0, 1.5, 3.0], size=len(invalid_idx))

    # Add missing values
    rating_missing_idx = np.random.choice(n_rows, size=int(n_rows * 0.08), replace=False)
    for idx in rating_missing_idx:
        rating_perc[idx] = np.random.choice(error_values)

    # 5. Score out of 100 with impossible values
    scores = np.random.normal(75, 12, n_rows)
    scores = np.clip(scores, 0, 100)  # Normal range

    # Convert to object array to allow mixed types
    scores = scores.astype(object)

    # Add impossible scores
    impossible_idx = np.random.choice(n_rows, size=int(n_rows * 0.05), replace=False)
    scores[impossible_idx] = np.random.choice([-10, 150, 200, -50, 999], size=len(impossible_idx))

    # Add missing values
    score_missing_idx = np.random.choice(n_rows, size=int(n_rows * 0.10), replace=False)
    for idx in score_missing_idx:
        scores[idx] = np.random.choice(error_values)

    # 6. Count data with decimals (should be integers) and negatives
    counts = np.random.poisson(15, n_rows).astype(float)

    # Convert to object array to allow mixed types
    counts = counts.astype(object)

    # Add decimal counts (data entry errors)
    decimal_idx = np.random.choice(n_rows, size=int(n_rows * 0.07), replace=False)
    for idx in decimal_idx:
        counts[idx] = float(counts[idx]) + np.random.uniform(0.1, 0.9)

    # Add negative counts (impossible)
    neg_count_idx = np.random.choice(n_rows, size=int(n_rows * 0.03), replace=False)
    counts[neg_count_idx] = -np.random.randint(1, 10, len(neg_count_idx))

    # Add missing values
    count_missing_idx = np.random.choice(n_rows, size=int(n_rows * 0.09), replace=False)
    for idx in count_missing_idx:
        counts[idx] = np.random.choice(error_values)

    # 7. Temperature with extreme and impossible values
    temperature = np.random.normal(22, 5, n_rows)  # Room temperature

    # Convert to object array to allow mixed types
    temperature = temperature.astype(object)

    # Add extreme temperatures
    extreme_temp_idx = np.random.choice(n_rows, size=int(n_rows * 0.03), replace=False)
    temperature[extreme_temp_idx] = np.random.choice([-273, 200, 500, -300, 1000], size=len(extreme_temp_idx))

    # Add missing values
    temp_missing_idx = np.random.choice(n_rows, size=int(n_rows * 0.11), replace=False)
    for idx in temp_missing_idx:
        temperature[idx] = np.random.choice(error_values)

    # 8. Distance with mixed units (some in mm, some in km)
    distance = np.random.exponential(50, n_rows)  # Base in km

    # Convert to object array to allow mixed types
    distance = distance.astype(object)

    # Some measurements accidentally in mm (x1000 error)
    unit_error_idx = np.random.choice(n_rows, size=int(n_rows * 0.04), replace=False)
    for idx in unit_error_idx:
        distance[idx] = float(distance[idx]) * 1000

    # Add missing values
    dist_missing_idx = np.random.choice(n_rows, size=int(n_rows * 0.13), replace=False)
    for idx in dist_missing_idx:
        distance[idx] = np.random.choice(error_values)

    # 9. Financial ratio with infinity and extreme values
    financial_ratio = np.random.normal(1.5, 0.8, n_rows)

    # Convert to object array to allow mixed types
    financial_ratio = financial_ratio.astype(object)

    # Add infinity values (division by zero errors)
    inf_idx = np.random.choice(n_rows, size=int(n_rows * 0.02), replace=False)
    financial_ratio[inf_idx] = np.random.choice([np.inf, -np.inf], size=len(inf_idx))

    # Add extremely large values
    large_idx = np.random.choice(n_rows, size=int(n_rows * 0.03), replace=False)
    financial_ratio[large_idx] = np.random.choice([1e10, -1e10, 1e15], size=len(large_idx))

    # Add missing values
    ratio_missing_idx = np.random.choice(n_rows, size=int(n_rows * 0.14), replace=False)
    for idx in ratio_missing_idx:
        financial_ratio[idx] = np.random.choice(error_values)

    # 10. Age with impossible values
    age = np.random.normal(35, 10, n_rows)
    age = np.abs(age)  # No negative ages initially

    # Convert to object array to allow mixed types
    age = age.astype(object)

    # Add impossible ages
    impossible_age_idx = np.random.choice(n_rows, size=int(n_rows * 0.04), replace=False)
    age[impossible_age_idx] = np.random.choice([200, 300, -5, 999, 0.5], size=len(impossible_age_idx))

    # Add missing values
    age_missing_idx = np.random.choice(n_rows, size=int(n_rows * 0.07), replace=False)
    for idx in age_missing_idx:
        age[idx] = np.random.choice(error_values)

    # Create DataFrame
    data = {
        'product_id': product_ids,
        'price_USD': prices,
        'revenue_total': revenue,
        'rating_percentage': rating_perc,
        'score_100': scores,
        'item_count': counts,
        'temperature_celsius': temperature,
        'distance_km': distance,
        'financial_ratio': financial_ratio,
        'customer_age': age
    }

    df = pd.DataFrame(data)

    # Convert columns to object type to preserve string error values
    numeric_cols = [col for col in df.columns if col != 'product_id']
    for col in numeric_cols:
        df[col] = df[col].astype('object')

    # Save to CSV
    df.to_csv(filename, index=False)

    # Print summary
    print(f"\n✅ Created {filename} with {len(df)} rows and {len(df.columns)} columns")
    print(f"\nColumns created:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i:2d}. {col}")

    print(f"\nData types:")
    print(df.dtypes)

    print(f"\nMissing/Error values per column:")
    for col in df.columns:
        if col != 'product_id':
            error_count = sum(1 for val in df[col] if str(val) in error_values)
            print(f"{col}: {error_count} ({error_count / len(df) * 100:.1f}%)")

    print(f"\nSample problematic values:")
    for col in numeric_cols[:3]:  # Show first 3 numeric columns
        sample_errors = [val for val in df[col] if str(val) in error_values][:3]
        if sample_errors:
            print(f"{col}: {sample_errors}")

    return df


# Test different sizes
def create_test_datasets():
    """Create different sized datasets for testing."""
    sizes = [100, 500, 1000]

    for size in sizes:
        filename = f"messy_data_{size}_rows.csv"
        print(f"\n{'=' * 50}")
        print(f"Creating {filename}")
        print(f"{'=' * 50}")
        create_messy_numerical_csv(filename, size)


if __name__ == "__main__":
    # Create a single large dataset
    df = create_messy_numerical_csv("csv/messy_numerical_data.csv", 1000)

    # Show first few rows
    print(f"\nFirst 5 rows:")
    print(df.head())

    # Uncomment to create multiple test datasets
    # create_test_datasets()