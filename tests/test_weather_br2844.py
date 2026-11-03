import weather_br2844
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

def test_version_is_defined():
    assert isinstance(weather_br2844.__version__, str)

from weather_br2844 import (
    celsius_to_fahrenheit,
    summarize_temperatures,
    clean_readings
)

# =============================================================================
# PART 1: UNIT TESTS
# =============================================================================


@pytest.mark.parametrize(
    "celsius, expected",
    [
        (0, 32),
        (100, 212),
        (-40, -40),
        (-273.15, -459.67),
        (37, 98.6),
    ],
)
def test_celsius_to_fahrenheit(celsius, expected):
    """ Test valid Celsius to Fahrenheit conversions using pytest.approx for floating point comparison."""
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected)


@pytest.mark.parametrize(
    "bad_input, expected_error",
    [
        ("37", TypeError),
        (None, TypeError),
        (True, TypeError),
        (-274.0, ValueError),
    ],
)
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    """Test that invalid types and temperatures below absolute zero raise errors."""
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)


def test_summarize_temperatures():
    """Test summarize_temperatures correctly handles a list with one NaN."""
    # Arrange
    temps = [10.0, float("nan"), 20.0]

    # Act
    summary = summarize_temperatures(temps)

    # Assert
    assert summary["mean"] == 15.0
    assert summary["min"] == 10.0
    assert summary["max"] == 20.0
    assert summary["n_missing"] == 1


# =============================================================================
# PART 2: FIXTURES
# =============================================================================


@pytest.fixture
def raw_readings():
    """Return the raw station readings DataFrame given in Part 2 of hw06.md."""
    return pd.DataFrame(
        {
            "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
            "date": [
                "2026-07-02",
                "2026-07-01",
                "2026-07-01",
                "2026-07-02",
                "2026-07-01",
            ],
            "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
        }
    )


def test_raw_readings_fixture(raw_readings):
    """Check that the raw_readings fixture returns the expected structure and missing values."""
    # Check column names
    assert list(raw_readings.columns) == ["station", "date", "temp_c"]

    # Check total number of rows
    assert len(raw_readings) == 5

    # Check count of missing values in the temp_c column
    assert raw_readings["temp_c"].isna().sum() == 1


# =============================================================================
# PART 3: TESTING DATAFRAMES
# =============================================================================


def test_clean_readings(raw_readings):
    """Build expected DataFrame by hand and compare with clean_readings output."""
    # Act: Clean the fixture DataFrame
    cleaned = clean_readings(raw_readings)

    # Arrange: Construct the expected DataFrame by hand
    expected = pd.DataFrame(
        {
            "station": ["CPK", "JFK", "LGA"],
            "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
            "temp_c": [25.0, 30.0, 28.0],
            "temp_f": [77.0, 86.0, 82.4],
        }
    )

    # Assert: Compare DataFrames for equality in values, columns, and index
    assert_frame_equal(cleaned, expected)
