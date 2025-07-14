"""
Prepo - Feature Preprocessing Package

A Python package for automated data preprocessing with type-safe enum architecture,
KNN imputation, outlier removal, and multiple scaling methods.

Features:
- Automated data type detection with type-safe enums
- KNN imputation for missing values  
- Multiple scaling methods (standard, robust, minmax)
- Outlier removal using IQR method
- CLI tool supporting 8+ file formats
- Optional Polars/PyArrow optimizations
- Modular architecture for programmatic and command-line usage
"""

from .preprocessor import FeaturePreProcessor
from .types import DataType, ScalerType, FileFormat, DataTypeDict
from .io import FileReader, FileWriter
from .cli import main as cli_main

__version__ = "0.2.0"
__all__ = [
    'FeaturePreProcessor',
    'DataType', 
    'ScalerType',
    'FileFormat',
    'DataTypeDict',
    'FileReader',
    'FileWriter',
    'cli_main'
]