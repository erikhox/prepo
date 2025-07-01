# FeaturePreProcessor

A Python package for preprocessing pandas DataFrames, with a focus on automatic data type detection, cleaning, and scaling.

## Features

- **Automatic Data Type Detection**: Automatically identifies column types (numeric, categorical, temporal, etc.)
- **Data Cleaning**: Handles missing values, standardizes null representations
- **Outlier Removal**: Identifies and removes outliers from numeric columns
- **Feature Scaling**: Supports multiple scaling methods (standard, robust, minmax)
- **Time Series Detection**: Identifies if a DataFrame represents time series data

## Installation

```bash
pip install -e .
```

## Usage

```python
import pandas as pd
from feature_preprocessor import FeaturePreProcessor

# Create a processor instance
processor = FeaturePreProcessor()

# Load your data
df = pd.read_csv('data/raw/your_data.csv')

# Process the data
processed_df = processor.process(
    df, 
    drop_na=True,           # Drop rows with missing values
    scaler_type='standard', # Scale numeric features using standard scaling
    remove_outlier=True     # Remove outliers
)

# Save the processed data
processed_df.to_csv('data/processed/processed_data.csv', index=False)
```

## Data Type Detection

The package automatically detects the following data types:

- **temporal**: Date and time columns
- **binary**: Columns with only two unique values
- **percentage**: Columns with values between 0 and 1, or columns with names containing "perc", "rating", etc.
- **price**: Columns with names containing "price", "cost", "revenue", etc.
- **id**: Columns with names ending or starting with "id"
- **numeric**: General numeric columns
- **integer**: Numeric columns with integer values
- **categorical**: Columns with a low ratio of unique values to total values
- **string**: Short text columns
- **text**: Long text columns

## Project Structure

```
feature_preprocessor/
├── data/               # Data directory
│   ├── raw/            # Raw data files
│   ├── processed/      # Processed data files
│   └── test/           # Test data files
├── src/                # Source code
│   └── feature_preprocessor/  # Main package
│       ├── __init__.py        # Package initialization
│       ├── preprocessor.py    # Core preprocessing functionality
│       └── data_generator.py  # Utilities for generating test data
├── tests/              # Test directory
│   ├── __init__.py     # Test package initialization
│   └── test_preprocessor.py  # Tests for preprocessor
├── README.md           # Project documentation
├── LICENSE             # License information
└── setup.py            # Package installation script
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.