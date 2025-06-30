import pandas as pd
import numpy as np
from dateutil.parser import parse
from scipy.stats import iqr
from sklearn.impute import KNNImputer


class FeaturePreProcessor:
    def __init__(self):
        pass

    def robustscaler(self, df: pd.DataFrame) -> pd.DataFrame:
        return (df - df.min()) / iqr(df)

    def minmaxscaler(self, df: pd.DataFrame) -> pd.DataFrame:
        return (df - df.min()) / (df.max() - df.min())

    def standardscaler(self, df: pd.DataFrame) -> pd.DataFrame:
        return df - df.mean() / df.std()

    def is_date(self, value):
        if pd.isna(value) or not isinstance(value, str):
            return False
        try:
            parse(value, fuzzy=False)
            return True
        except:
            return False

    def is_string(self, string):
        if isinstance(string, str):
            return True
        else:
            return False

    def determinedatatype(self, df: pd.DataFrame) -> dict:
        datatypes = {}
        smdf = df.head(100)
        for col in smdf.columns:
            if any(word in col.lower() for word in ["date", "time"]):
                datatypes[col] = "temporal"
            elif smdf[col].apply(self.is_date).all():
                datatypes[col] = "temporal"
            elif smdf[col].unique().size == 2:
                datatypes[col] = "binary"
            elif pd.api.types.is_any_real_numeric_dtype(smdf[col]) and any(word in col.lower() for word in ["perc", "rating", "percentage", "percent", "%", "score"]):
                datatypes[col] = "percentage"
            elif any(word in col.lower() for word in ["price", "revenue", '$', '€', '£', '¥', '₹', '₽', '₩', '₪', '₦', '₡', '¢', '₨', '₱']):
                datatypes[col] = "price"
            elif smdf[col].dtype == "int64" or smdf[col].dtype == "float64":
                datatypes[col] = "numeric"
            elif (df[col].nunique() / len(df) < 0.5 and (smdf[col].dtype == "object" or smdf[col].dtype == "string")) or any(word in col.lower() for word in ["category", "categories"]):
                datatypes[col] = "categorical"
            elif smdf[col].dtype == "string":
                datatypes[col] = "string"
            else:
                datatypes[col] = "unknown"
        return datatypes

    def cleandata(self, df: pd.DataFrame, dropna=True) -> tuple[pd.DataFrame, dict]:
        datatypes = self.determinedatatype(df)
        tempdf = df.copy()
        tempdf.replace(["Error", "na", "NA", "ERROR", "error", "err", "ERR", "NAType", "natype", "UNKNOWN", "unknown", ""], np.nan, inplace=True)
        if dropna:
            tempdf.dropna(how='any', inplace=True)
        else:
            for col in tempdf.columns:
                if not tempdf[col].isnull().any():
                    continue
                elif datatypes[col] in ["numeric", "price", "percentage"]:
                    imputer = KNNImputer(n_neighbors=3)
                    tempdf[col] = imputer.fit_transform(tempdf[[col]]).flatten()
                elif datatypes[col] in ["string", "temporal", "unknown", "binary"]:
                    tempdf.dropna(subset=[col], inplace=True)

        tempdf.index = range(len(tempdf))
        return tempdf, datatypes

    def istimeseries(self, df: pd.DataFrame) -> bool:
        datatypes = self.determinedatatype(df)
        temporalCounts = 0
        for key in datatypes:
            if datatypes[key] == "temporal":
                temporalCounts += 1
        if temporalCounts == 1:
            return True
        else:
            return False

    def scaler(self, df: pd.DataFrame, dropna=True, func=0) -> pd.DataFrame:
        cleandatares = self.cleandata(df, dropna=dropna)
        data = cleandatares[0]
        datatypes = cleandatares[1]
        function = None

        if func == 0:
            function = self.standardscaler
        elif func == 1:
            function = self.robustscaler
        elif func == 2:
            function = self.minmaxscaler
        else:
            raise ValueError("Invalid function")

        for col in data.columns:
            if datatypes[col] in ["price", "numeric"]:
                data[col] = function(data[col])
            else:
                continue

        return data


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
    df = pd.read_csv(r"C:\Users\erikh\PycharmProjects\FeaturePreProcessor\retail_store_sales.csv")
    normalized = processor.scaler(df, dropna=True, func=0)

    print(normalized)