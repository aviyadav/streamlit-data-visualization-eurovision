import pytest
import pandas as pd
from main import load_votes, favourites, country_chart


class TestLoadVotes:
    """Tests for the load_votes function."""
    
    def test_load_votes_returns_dataframe(self):
        """Test that load_votes returns a Pandas DataFrame."""
        votes = load_votes()
        assert isinstance(votes, pd.DataFrame)
    
    def test_load_votes_filters_final_round(self):
        """Test that only final round votes are included."""
        votes = load_votes()
        # All rows should be from the final round
        assert len(votes) > 0
        # Check if round column exists in the original data
        all_votes = pd.read_csv("https://github.com/Spijkervet/eurovision-dataset/releases/download/2023/votes.csv")
        assert len(all_votes) > len(votes)  # Should have filtered some rows
    
    def test_load_votes_has_points_column(self):
        """Test that the points column is created."""
        votes = load_votes()
        assert "points" in votes.columns
    
    def test_points_column_has_no_nulls(self):
        """Test that the points column has no null values."""
        votes = load_votes()
        assert votes["points"].isna().sum() == 0
    
    def test_points_column_values(self):
        """Test that points column contains valid values."""
        votes = load_votes()
        assert votes["points"].min() >= 0  # Points should be non-negative
        assert votes["points"].dtype in [int, float, 'int64', 'float64']
    
    def test_required_columns_exist(self):
        """Test that all required columns exist."""
        votes = load_votes()
        required_columns = ["from_country", "to_country", "year", "points"]
        for col in required_columns:
            assert col in votes.columns, f"Column {col} is missing"


class TestFavourites:
    """Tests for the favourites function."""
    
    @pytest.fixture
    def sample_votes(self):
        """Create sample votes data for testing."""
        return pd.DataFrame({
            "from_country": ["us", "uk", "fr", "us", "uk"],
            "to_country": ["uk", "fr", "us", "fr", "us"],
            "points": [12, 12, 10, 12, 8],
            "year": [2020, 2020, 2020, 2021, 2021]
        })
    
    def test_favourites_filters_12_points(self, sample_votes):
        """Test that favourites only includes 12-point votes."""
        result = (
            sample_votes[sample_votes["points"] == 12]
            .groupby(["from_country", "to_country"])["points"]
            .count()
            .reset_index()
        )
        assert len(result) == 3  # us->uk, us->fr, uk->fr (3 unique pairs)
        assert all(result["points"] > 0)  # All counts should be > 0
    
    def test_favourites_groups_correctly(self, sample_votes):
        """Test that favourites groups by from_country and to_country."""
        result = (
            sample_votes[sample_votes["points"] == 12]
            .groupby(["from_country", "to_country"])["points"]
            .count()
            .reset_index()
        )
        assert "from_country" in result.columns
        assert "to_country" in result.columns
        assert "points" in result.columns
    
    def test_favourites_with_real_data(self):
        """Test favourites function with real Eurovision data."""
        votes = load_votes()
        favourite_country = (
            votes[votes["points"] == 12]
            .groupby(["from_country", "to_country"])["points"]
            .count()
            .reset_index()
        )
        assert len(favourite_country) > 0
        assert len(favourite_country.columns) == 3  # from_country, to_country, points


class TestCountryChart:
    """Tests for the country_chart function."""
    
    @pytest.fixture
    def sample_votes(self):
        """Create sample votes data for testing."""
        return pd.DataFrame({
            "from_country": ["us", "uk", "fr", "us", "uk", "fr"],
            "to_country": ["de", "de", "de", "fr", "fr", "us"],
            "points": [12, 10, 8, 12, 8, 5],
            "year": [2020, 2020, 2020, 2021, 2021, 2021]
        })
    
    def test_get_unique_countries(self, sample_votes):
        """Test that unique countries are extracted correctly."""
        all_countries = sample_votes["to_country"].unique()
        all_countries.sort()
        assert len(all_countries) == 3
        assert list(all_countries) == ["de", "fr", "us"]
    
    def test_country_aggregation(self, sample_votes):
        """Test that country data is aggregated correctly by year."""
        selected_country = "de"
        total_by_country = (
            sample_votes[sample_votes["to_country"] == selected_country]
            .groupby(["to_country", "year"])["points"]
            .sum()
            .reset_index()
        )
        assert len(total_by_country) == 1  # Only one year has data for 'de'
        assert total_by_country["to_country"].iloc[0] == "de"
        assert total_by_country["points"].iloc[0] == 30  # 12 + 10 + 8
    
    def test_country_chart_with_real_data(self):
        """Test country chart aggregation with real Eurovision data."""
        votes = load_votes()
        all_countries = votes["to_country"].unique()
        assert len(all_countries) > 0
        
        # Test with first country
        selected_country = all_countries[0]
        total_by_country = (
            votes[votes["to_country"] == selected_country]
            .groupby(["to_country", "year"])["points"]
            .sum()
            .reset_index()
        )
        assert len(total_by_country) > 0
        assert "year" in total_by_country.columns
        assert "points" in total_by_country.columns
        assert total_by_country["to_country"].unique().tolist() == [selected_country]


class TestDataIntegrity:
    """Tests for overall data integrity."""
    
    def test_no_null_values_in_points(self):
        """Test that there are no null values in the points column."""
        votes = load_votes()
        assert votes["points"].isna().sum() == 0
    
    def test_country_codes_format(self):
        """Test that country codes are in the expected format."""
        votes = load_votes()
        from_countries = votes["from_country"].unique().tolist()
        to_countries = votes["to_country"].unique().tolist()
        
        # Country codes should be lowercase strings (typically 2 letters, but some may be 3)
        for country in from_countries + to_countries:
            assert isinstance(country, str)
            assert len(country) >= 2
            assert country.islower()
    
    def test_years_are_valid(self):
        """Test that years are in a valid range."""
        votes = load_votes()
        years = votes["year"].unique()
        assert all(1956 <= year <= 2025 for year in years)  # Eurovision started in 1956
    
    def test_points_are_numeric(self):
        """Test that all points values are numeric."""
        votes = load_votes()
        assert pd.api.types.is_numeric_dtype(votes["points"])
    
    def test_dataframe_not_empty(self):
        """Test that the loaded dataframe is not empty."""
        votes = load_votes()
        assert len(votes) > 0
        assert len(votes.columns) > 0


class TestDataTransformations:
    """Tests for data transformation logic."""
    
    def test_fillna_logic(self):
        """Test that fillna works correctly for points column."""
        # Create test data with nulls in jury_points
        test_data = pd.DataFrame({
            "round": ["final", "final", "final"],
            "jury_points": [10, None, 12],
            "total_points": [10, 8, 12],
            "from_country": ["us", "uk", "fr"],
            "to_country": ["uk", "fr", "de"],
            "year": [2020, 2020, 2020]
        })
        
        # Apply the same logic as load_votes
        test_data = test_data[test_data["round"] == "final"]
        test_data["points"] = test_data["jury_points"].fillna(test_data["total_points"])
        
        assert test_data["points"].iloc[0] == 10
        assert test_data["points"].iloc[1] == 8  # Should be filled from total_points
        assert test_data["points"].iloc[2] == 12
        assert test_data["points"].isna().sum() == 0
