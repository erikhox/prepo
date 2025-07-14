import pandas as pd
import numpy as np
from src.prepo import FeaturePreProcessor
from pathlib import Path


def main():
    """
    Demonstrate basic usage of the FeaturePreProcessor package.
    """
    # Create a sample dataframe
    data = {
        "date_column": ["2023-01-01", "2023-01-02", np.nan, "2023-01-04", "2023-01-05"],
        "price_USD": [100.50, np.nan, 200.75, 150.25, 300.00],
        "percentage_score": [0.85, 0.92, np.nan, 0.78, 0.95],
        "rating_100": [85, 92, np.nan, 78, 95],
        "is_active": [True, False, np.nan, True, False],
        "category": ["A", "B", np.nan, "A", "C"],
        "revenue": [1000.50, 2000.75, np.nan, 1500.25, 3000.00],
        "count": [10, 15, np.nan, 12, 20],
        "description": ["Product A", np.nan, "Product C", "Product D", "Product E"],
    }
    df = pd.DataFrame(data)

    print("Original DataFrame:")
    print(df)
    print("\nDataFrame shape:", df.shape)
    print("\nDataFrame info:")
    print(df.info())

    # Create a processor instance
    processor = FeaturePreProcessor()

    # Determine datatypes
    datatypes = processor.determine_datatypes(df)
    print("\nDetermined datatypes:")
    for col, dtype in datatypes.items():
        print(f"  {col}: {dtype}")

    # Clean data
    print("\nCleaning data...")
    clean_df, _ = processor.clean_data(df, drop_na=False)
    print("Cleaned DataFrame shape:", clean_df.shape)

    # Process data (clean, remove outliers, scale)
    print("\nProcessing data (cleaning, removing outliers, scaling)...")
    processed_df = processor.process(df, drop_na=True, scaler_type="standard", remove_outlier=True)
    print("Processed DataFrame:")
    print(processed_df)
    print("\nProcessed DataFrame shape:", processed_df.shape)

    # Save processed data
    file_path = Path("../data/processed/example_processed.csv")
    processed_df.to_csv(file_path, index=False)
    print("\nProcessed data saved to ../data/processed/example_processed.csv")

    # Load and process a real dataset
    try:
        print("\nLoading and processing a real dataset...")

        file_path = Path("../data/raw/winequality-white.csv")
        real_df = pd.read_csv(file_path, sep=";")
        print("Original dataset shape:", real_df.shape)

        processed_real_df = processor.process(real_df, drop_na=True, scaler_type="standard", remove_outlier=True)
        print("Processed dataset shape:", processed_real_df.shape)

        file_path = Path("../data/processed/winequality-white-processed.csv")
        processed_real_df.to_csv(file_path, index=False)
        print("Processed data saved to ../data/processed/winequality-white-processed.csv")
    except Exception as e:
        print(f"Error processing real dataset: {e}")


if __name__ == "__main__":
    main()
