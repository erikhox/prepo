# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-01-XX

### Added
- **Type-safe enum architecture** using Python's `enum.Enum` for data types, scaler types, and file formats
- **Automated data type detection** with enhanced precision including integer vs float distinction
- **KNN imputation** for missing values with fallback to mean imputation
- **Multiple scaling methods** (standard, robust, minmax, none) with type-safe enum interface
- **Outlier removal** using IQR (Interquartile Range) method
- **CLI tool** supporting 8+ file formats with comprehensive options:
  - CSV, JSON, Excel (.xlsx/.xls), Parquet, Feather, TSV, Pickle, ORC
  - Multiple scaler options (standard, robust, minmax, none)
  - NA handling options (drop or impute with KNN)
  - Outlier removal toggle
  - Information display mode
  - Explicit format specification
- **Optional Polars/PyArrow optimizations** for high-performance operations
- **Modular architecture** with separate modules for:
  - Core preprocessing (`preprocessor.py`)
  - Type definitions (`types.py`) 
  - File I/O operations (`io.py`)
  - Command-line interface (`cli.py`)
- **Enhanced CI/CD pipeline** with:
  - Multi-platform testing (Ubuntu, Windows, macOS)
  - Python 3.9-3.13 support
  - Automated PyPI deployment
  - Pre-commit hooks integration
  - 85%+ test coverage requirement
  - Security scanning with bandit and safety
  - Integration testing with real data
- **Comprehensive test suite** achieving 85%+ coverage:
  - Unit tests for all modules
  - Integration tests for CLI functionality
  - Edge case testing
  - Performance optimization testing
- **Modern Python packaging** with pyproject.toml configuration
- **Pre-commit hooks** for code quality enforcement
- **Type hints** throughout the codebase for better IDE support

### Changed
- **Breaking**: Replaced string-based data type system with type-safe enums
- **Breaking**: Updated constructor to accept optimization flags (`use_polars`, `use_pyarrow`)
- **Enhanced**: Data type detection now distinguishes between integer and float numeric types
- **Enhanced**: Improved categorical data detection
- **Enhanced**: Better handling of edge cases in data cleaning
- **Enhanced**: More robust percentage detection using actual value ranges
- **Improved**: Python version support updated to 3.9-3.13
- **Improved**: Dependencies updated to more recent versions
- **Improved**: Documentation and type hints throughout

### Technical Details
- Added `DataType`, `ScalerType`, and `FileFormat` enums for type safety
- Implemented `FileReader` and `FileWriter` classes for multi-format I/O
- Created comprehensive CLI with argparse for professional command-line experience
- Integrated optional high-performance libraries (Polars, PyArrow) with graceful fallbacks
- Established modern Python packaging with both setup.py and pyproject.toml
- Implemented pre-commit hooks with black, isort, flake8, and mypy
- Created multi-platform CI/CD pipeline with GitHub Actions
- Added security scanning and automated deployment workflows

### Performance Improvements
- Optional Polars integration for high-performance CSV and Parquet operations
- Optional PyArrow integration for optimized Parquet I/O
- Improved data type detection algorithm efficiency
- Better memory usage in outlier detection

### Developer Experience
- Type hints throughout the codebase
- Pre-commit hooks for code quality
- Comprehensive test suite with 85%+ coverage
- Modern packaging with pyproject.toml
- Detailed documentation and examples
- CLI tool for quick data preprocessing tasks

## [0.1.6] - Previous Version

### Features
- Basic DataFrame preprocessing
- Simple data type detection
- Basic scaling methods
- Outlier removal
- Missing value handling

---

## Migration Guide from 0.1.x to 0.2.0

### Breaking Changes

1. **Enum-based Data Types**: Replace string comparisons with enum values
   ```python
   # Old (0.1.x)
   if datatype == "numeric":
       ...
   
   # New (0.2.0)
   if datatype == DataType.NUMERIC:
       ...
   ```

2. **Constructor Changes**: Add optimization flags if needed
   ```python
   # Old (0.1.x)
   processor = FeaturePreProcessor()
   
   # New (0.2.0) - same default behavior
   processor = FeaturePreProcessor()
   
   # New (0.2.0) - with optimizations
   processor = FeaturePreProcessor(use_polars=True, use_pyarrow=True)
   ```

3. **Scaler Type Parameter**: Can now use enums or strings
   ```python
   # Old (0.1.x) - strings only
   df = processor.process(df, scaler_type="standard")
   
   # New (0.2.0) - both work
   df = processor.process(df, scaler_type="standard")  # Still works
   df = processor.process(df, scaler_type=ScalerType.STANDARD)  # Recommended
   ```

### New Features to Explore

1. **CLI Tool**: Try the new command-line interface
   ```bash
   prepo input.csv output.csv --scaler robust --info
   ```

2. **Multiple File Formats**: Use the I/O classes for different formats
   ```python
   from prepo.io import FileReader, FileWriter
   
   reader = FileReader()
   writer = FileWriter()
   
   df = reader.read_file("data.json")
   writer.write_file(df, "output.parquet")
   ```

3. **Performance Optimizations**: Enable for large datasets
   ```python
   processor = FeaturePreProcessor(use_polars=True, use_pyarrow=True)
   ```
