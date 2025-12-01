# Eurovision Data Visualization with Streamlit

[REF] - https://github.com/krisajenkins/streamlit-demo

A Streamlit application for visualizing Eurovision Song Contest voting data. Available in two versions:
- **`main_pl.py`**: Uses Polars for efficient data processing
- **`main.py`**: Uses Pandas for traditional data processing

## Features

- **Favourites Tab**: Scatter chart showing which countries consistently give 12 points to each other
- **Country Tab**: Line chart showing a selected country's total points received over the years
- **Raw Data Tab**: Interactive table view of the complete dataset

## Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

## Installation

### Using uv (Recommended)

```bash
# Clone or navigate to the project directory
cd streamlit-data-visualization-eurovision

# uv will automatically install dependencies when you run the app
uv run streamlit run main_pl.py
```

### Using pip

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install polars>=1.35.2 streamlit>=1.51.0

# Run the application
streamlit run main_pl.py
```

## Usage

1. Start the application:
   ```bash
   # Polars version (recommended for performance)
   uv run streamlit run main_pl.py --server.headless true
   
   # OR Pandas version
   uv run streamlit run main.py --server.headless true
   ```

2. Open your browser to the URL shown in the terminal (typically `http://localhost:8501`)

3. Explore the visualizations:
   - **Favourites**: See which countries frequently award each other the maximum 12 points
   - **Country**: Select a country to see its performance over the years
   - **Raw**: Browse the complete dataset with filtering and sorting

## Data Source

This application uses the Eurovision Song Contest voting dataset from:
- [Eurovision Dataset (2023 release)](https://github.com/Spijkervet/eurovision-dataset)
- Data includes voting information from Eurovision finals
- Automatically fetched and cached for 1 hour

## Development

### Running Tests

The project includes comprehensive tests for both versions using pytest:

```bash
# Run all tests for both versions
uv run pytest

# Run tests for Polars version only
uv run pytest test_main_pl.py -v

# Run tests for Pandas version only
uv run pytest test_main.py -v

# Run specific test class
uv run pytest test_main_pl.py::TestLoadVotes -v

# Run with coverage report for both versions
uv run pytest --cov=main_pl --cov=main --cov-report=term-missing
```

### Test Coverage

Both test suites (`test_main.py` and `test_main_pl.py`) provide comprehensive coverage:
- **Data Loading**: CSV parsing, caching behavior
- **Data Filtering**: Round filtering, null handling
- **Data Transformation**: Type conversions (Polars), fillna logic (Pandas)
- **Aggregation Logic**: Group by operations, counting, summing
- **Data Integrity**: Null checks, country code validation, year validation
- **Visualization Prep**: Country extraction, sorting, filtering

### Project Structure

```
streamlit-data-visualization-eurovision/
├── main_pl.py          # Streamlit app (Polars version)
├── main.py             # Streamlit app (Pandas version)
├── test_main_pl.py     # Test suite for Polars version
├── test_main.py        # Test suite for Pandas version
├── pyproject.toml      # Project dependencies
└── README.md           # This file
```

### Code Overview

Both versions contain the same core functions with different implementations:

**main_pl.py** (Polars version):
- `load_votes()`: Fetches and processes Eurovision voting data using Polars
- `favourites()`: Creates visualization of 12-point vote patterns
- `country_chart()`: Generates per-country performance charts
- `main()`: Streamlit app entry point with tab navigation

**main.py** (Pandas version):
- `load_votes()`: Fetches and processes Eurovision voting data using Pandas
- `favourites()`: Creates visualization of 12-point vote patterns
- `country_chart()`: Generates per-country performance charts
- `main()`: Streamlit app entry point with tab navigation

## Technologies Used

- **Streamlit**: Web application framework for data visualization
- **Polars**: Fast DataFrame library for data processing (main_pl.py)
- **Pandas**: Traditional DataFrame library for data processing (main.py)
- **pytest**: Testing framework with fixtures and comprehensive assertions
- **Python 3.13+**: Modern Python features and performance

## Performance

- Data is cached for 1 hour to minimize API calls
- **Polars version (main_pl.py)**: Faster data processing, lower memory usage, better for large datasets
- **Pandas version (main.py)**: More familiar API, wider ecosystem support
- Both versions use efficient filtering and aggregation operations

### When to Choose Which Version

**Use Polars (main_pl.py)** if:
- You need maximum performance
- Working with large datasets
- You want lower memory consumption

**Use Pandas (main.py)** if:
- You're more familiar with Pandas syntax
- You need compatibility with existing Pandas-based tools
- You prefer the mature Pandas ecosystem

## Contributing

1. Ensure all tests pass before submitting changes
2. Follow the existing code style
3. Add tests for new features
4. Update documentation as needed

## License

This project uses publicly available Eurovision voting data. Please refer to the [Eurovision Dataset repository](https://github.com/Spijkervet/eurovision-dataset) for data licensing information.

## Troubleshooting

### Module Not Found Error
If you get a "Module not found" error, ensure dependencies are installed:
```bash
uv sync
```

### Data Loading Issues
The application requires internet connectivity to fetch the Eurovision dataset. If you experience issues:
- Check your internet connection
- Verify the dataset URL is accessible
- Clear Streamlit cache: `streamlit cache clear`

### Type Errors
If you encounter type conversion errors, ensure you're using:
- Polars >= 1.35.2 (for main_pl.py)
- Pandas is included with Streamlit
- Python >= 3.13

### Differences Between Versions
The two versions have slightly different data processing approaches:
- **Polars**: Explicit type casting (String → Float → Int)
- **Pandas**: Uses fillna() for null handling, automatic type inference

### Browser Opening Error
If you see `gio: http://localhost:8501: Operation not supported`, this happens when Streamlit tries to auto-open a browser in a headless environment. Fix it by:

**Option 1: Use headless mode** (recommended)
```bash
uv run streamlit run main_pl.py --server.headless true
```

**Option 2: Create a config file**
Create `.streamlit/config.toml`:
```toml
[server]
headless = true
```

**Option 3: Disable browser opening**
```bash
STREAMLIT_SERVER_HEADLESS=true uv run streamlit run main_pl.py
```

## Acknowledgments

- Eurovision Song Contest dataset by [Spijkervet](https://github.com/Spijkervet/eurovision-dataset)
- Built with Streamlit and Polars
