import pandas as pd
import numpy as np
from dateutil.parser import parse
from scipy.stats import iqr
from sklearn.impute import KNNImputer
from typing import Dict, Tuple


class FeaturePreProcessor:
    """
    A feature preprocessing class for data cleaning, scaling, and transformation.
    """

    def __init__(self):
        self.scalers = {
            'standard': self._standard_scaler,
            'robust': self._robust_scaler,
            'minmax': self._minmax_scaler
        }

    def _robust_scaler(self, series: pd.Series) -> pd.Series:
        """Apply robust scaling using IQR."""
        median = series.median()
        iqr_value = iqr(series)
        if iqr_value == 0:
            return series - median
        return (series - median) / iqr_value

    def _minmax_scaler(self, series: pd.Series) -> pd.Series:
        """Apply min-max scaling."""
        min_val, max_val = series.min(), series.max()
        if min_val == max_val:
            return series - min_val
        return (series - min_val) / (max_val - min_val)

    def _standard_scaler(self, series: pd.Series) -> pd.Series:
        """Apply standard scaling (z-score normalization)."""
        mean_val, std_val = series.mean(), series.std()
        if std_val == 0:
            return series - mean_val
        return (series - mean_val) / std_val

    def _is_date(self, value) -> bool:
        """Check if a value can be parsed as a date."""
        if pd.isna(value) or not isinstance(value, str):
            return False
        try:
            parse(value, fuzzy=False)
            return True
        except (ValueError, TypeError):
            return False

    def _is_string(self, value) -> bool:
        """Check if a value is a string."""
        return isinstance(value, str)

    def clean_outliers(self, df: pd.DataFrame, dt: Dict[str, str]) -> pd.DataFrame:
        newdf = df.copy()

        for col in df.columns:
            if any(word in col.lower() for word in ["id", "tag", "identification", "item"]):
                continue
            if dt[col] in ["price", "numeric", "percentage"]:
                iqrv = iqr(newdf[col])
                q1 = newdf[col].quantile(0.25)
                q3 = newdf[col].quantile(0.75)
                newdf = newdf[newdf[col].between(q1-1.5*iqrv, q3+1.5*iqrv)]

        return newdf

    def is_timeseries(self, df: pd.DataFrame) -> bool:
        """
        Determine if the dataframe represents a time series (has exactly one temporal column).
        """
        datatypes = self.determine_datatypes(df)
        temporal_count = sum(1 for dtype in datatypes.values() if dtype == "temporal")
        return temporal_count == 1

    def determine_datatypes(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Determine the data type of each column in the dataframe.
        Args:
            df: DataFrame to analyze
        Returns:
            Dictionary mapping column names to their inferred data types
        """
        datatypes = {}
        # Use sample of data for efficiency
        sample_df = df.head(min(100, len(df.index)))

        for col in sample_df.columns:
            col_lower = col.lower()
            series = sample_df[col]

            # Check for temporal data
            if any(word in col_lower for word in ["date", "time"]):
                datatypes[col] = "temporal"
            elif series.dropna().apply(self._is_date).all() and not series.dropna().empty:
                datatypes[col] = "temporal"

            # Check for binary data
            elif series.nunique() == 2:
                datatypes[col] = "binary"

            # Check for percentage data
            elif (pd.api.types.is_numeric_dtype(series) and
                  any(word in col_lower for word in ["perc", "rating", "percentage", "percent", "%", "score"])):
                datatypes[col] = "percentage"

            # Check for price/currency data
            elif any(word in col_lower for word in
                     ["price", "revenue", '$', '€', '£', '¥', '₹', '₽', '₩', '₪', '₦', '₡', '¢', '₨', '₱']):
                datatypes[col] = "price"

            # Check for numeric data
            elif pd.api.types.is_numeric_dtype(series):
                datatypes[col] = "numeric"

            # Check for categorical data
            elif ((series.nunique() / len(df) < 0.5 and pd.api.types.is_object_dtype(series)) or
                  any(word in col_lower for word in ["category", "categories"])):
                datatypes[col] = "categorical"

            # Check for string data
            elif pd.api.types.is_string_dtype(series) or pd.api.types.is_object_dtype(series):
                datatypes[col] = "string"

            else:
                datatypes[col] = "unknown"

        return datatypes

    def clean_data(self, df: pd.DataFrame, drop_na: bool = True) -> Tuple[pd.DataFrame, Dict[str, str]]:
        """
        Clean the dataframe by handling missing values and standardizing null representations.
        Args:
            df: DataFrame to clean
            drop_na: If True, drop rows with NA values; if False, impute them
        Returns:
            Tuple of (cleaned_dataframe, datatypes_dict)
        """
        datatypes = self.determine_datatypes(df)
        clean_df = df.copy()

        # Standardize null value representations
        null_values = ["?", "Error", "na", "NA", "ERROR", "error", "err", "ERR",
                       "NAType", "natype", "UNKNOWN", "unknown", ""]
        clean_df = clean_df.replace(null_values, np.nan)

        if drop_na:
            clean_df = clean_df.dropna(how='any')
        else:
            # Impute missing values based on data type
            for col in clean_df.columns:
                if not clean_df[col].isnull().any():
                    continue

                if datatypes[col] in ["numeric", "price", "percentage"]:
                    # Use KNN imputation for numeric data
                    if clean_df[col].notna().sum() >= 3:  # Need at least 3 values for KNN
                        imputer = KNNImputer(n_neighbors=min(3, clean_df[col].notna().sum()))
                        clean_df[col] = imputer.fit_transform(clean_df[[col]]).flatten()
                    else:
                        # Fallback to mean imputation
                        clean_df[col] = clean_df[col].fillna(clean_df[col].mean())

                elif datatypes[col] == "categorical":
                    # Use mode for categorical data
                    mode_value = clean_df[col].mode()
                    if not mode_value.empty:
                        clean_df[col] = clean_df[col].fillna(mode_value[0])

                else:
                    # Drop rows with missing values for temporal, string, binary, or unknown types
                    clean_df = clean_df.dropna(subset=[col])

        # Reset index
        clean_df = clean_df.reset_index(drop=True)
        return clean_df, datatypes

    def scale_features(self, df: pd.DataFrame, drop_na: bool = True, scaler_type: str = 'standard') -> pd.DataFrame:
        """
        Clean and scale numeric features in the dataframe.
        Args:
            df: DataFrame to process
            drop_na: Whether to drop NA values during cleaning
            scaler_type: Type of scaler to use ('standard', 'robust', 'minmax')
        Returns:
            Scaled DataFrame
        """
        if scaler_type not in self.scalers:
            raise ValueError(f"Unknown scaler type: {scaler_type}. Available: {list(self.scalers.keys())}")

        clean_df, datatypes = self.clean_data(df, drop_na=drop_na)
        scaler_func = self.scalers[scaler_type]

        # Scale numeric columns
        for col in clean_df.columns:
            if any(word in col.lower() for word in ["id", "tag", "identification", "item"]):
                continue
            if datatypes[col] in ["price", "numeric", "percentage"]:
                clean_df[col] = scaler_func(clean_df[col])

        return clean_df

    def process(self):
        '''temp'''

if __name__ == "__main__":
    data = {
        'date_column': ['2023-01-01', '2023-01-02', np.nan, '2023-01-04', '2023-01-05'],
        'price_USD': [100.50, np.nan, 200.75, 150.25, 300.00],
        'percentage_score': [0.85, 0.92, np.nan, 0.78, 0.95],
        'rating_100': [85, 92, np.nan, 78, 95],
        'is_active': [True, False, np.nan, True, False],
        'category': ['A', 'B', np.nan, 'A', 'C'],
        'revenue': [1000.50, 2000.75, np.nan, 1500.25, 3000.00],
        'count': [10, 15, np.nan, 12, 20],
        'description': ['Product A', np.nan, 'Product C', 'Product D', 'Product E']
    }

    processor = FeaturePreProcessor()
    df = pd.read_csv(r"C:\Users\erikh\PycharmProjects\FeaturePreProcessor\listings.csv")
    normalized = processor.scale_features(df, drop_na=False, scaler_type="standard")

    print(normalized)