# -*- coding: utf-8 -*-
"""
Unit tests for Sentinel helper functions.

Run with: python -m pytest tests/test_helpers.py -v
"""

import pytest
import pandas as pd
from sentinel.utils.helpers import (
    sanitize_conviction,
    conviction_to_weight,
    floor_to_precision,
    calculate_rsi,
    compute_pct_change
)


class TestSanitizeConviction:
    """Tests for sanitize_conviction function."""

    def test_valid_integer(self):
        """Test with valid integer conviction scores."""
        assert sanitize_conviction(5) == 5
        assert sanitize_conviction(1) == 1
        assert sanitize_conviction(10) == 10

    def test_valid_float(self):
        """Test with float values (should round)."""
        assert sanitize_conviction(7.4) == 7
        assert sanitize_conviction(7.6) == 8
        assert sanitize_conviction(9.5) == 10

    def test_out_of_range(self):
        """Test values outside 1-10 range (should clamp)."""
        assert sanitize_conviction(0) == 1
        assert sanitize_conviction(-5) == 1
        assert sanitize_conviction(15) == 10
        assert sanitize_conviction(100) == 10

    def test_invalid_input(self):
        """Test with invalid input (should default to 5)."""
        assert sanitize_conviction("invalid") == 5
        assert sanitize_conviction(None) == 5
        assert sanitize_conviction([1, 2, 3]) == 5


class TestConvictionToWeight:
    """Tests for conviction_to_weight function."""

    def test_max_conviction(self):
        """Test maximum conviction (10) gives weight of 1.0."""
        assert conviction_to_weight(10) == 1.0

    def test_min_conviction(self):
        """Test minimum conviction (1) gives minimum floor weight."""
        weight = conviction_to_weight(1)
        assert weight >= 0.05  # MIN_WEIGHT_FLOOR

    def test_mid_conviction(self):
        """Test middle conviction scores."""
        weight_5 = conviction_to_weight(5)
        weight_7 = conviction_to_weight(7)
        assert 0.05 < weight_5 < weight_7 < 1.0

    def test_monotonic_increasing(self):
        """Test that higher conviction always gives higher weight."""
        weights = [conviction_to_weight(i) for i in range(1, 11)]
        assert weights == sorted(weights)  # Should be strictly increasing


class TestFloorToPrecision:
    """Tests for floor_to_precision function."""

    def test_normal_value(self):
        """Test flooring normal positive values."""
        result = floor_to_precision(1.123456789, decimals=6)
        assert result < 1.123456
        assert result >= 1.123454  # Allow for epsilon adjustment

    def test_zero_and_negative(self):
        """Test zero and negative values."""
        assert floor_to_precision(0, decimals=6) == 0.0
        assert floor_to_precision(-1.5, decimals=6) == 0.0

    def test_different_precision(self):
        """Test different decimal precisions."""
        result_2 = floor_to_precision(1.9999, decimals=2)
        result_4 = floor_to_precision(1.9999, decimals=4)
        assert result_2 < 2.0
        assert result_4 < 2.0


class TestCalculateRSI:
    """Tests for RSI calculation."""

    def test_insufficient_data(self):
        """Test with insufficient data returns None."""
        short_series = pd.Series([100, 101, 102])
        assert calculate_rsi(short_series, period=14) is None

    def test_rsi_range(self):
        """Test that RSI stays in 0-100 range."""
        # Create test data: trending up
        prices = pd.Series(range(100, 130))
        rsi = calculate_rsi(prices, period=14)
        assert rsi is not None
        assert 0 <= rsi <= 100

    def test_all_gains(self):
        """Test RSI with all gains (should be 100)."""
        prices = pd.Series([100 + i for i in range(20)])  # Steadily increasing
        rsi = calculate_rsi(prices, period=14)
        assert rsi == 100.0

    def test_rsi_calculation(self):
        """Test RSI with realistic price data."""
        # Sample price data with ups and downs
        prices = pd.Series([
            100, 102, 101, 103, 102, 104, 103, 105,
            106, 105, 107, 106, 108, 107, 109, 110,
            109, 111, 110, 112
        ])
        rsi = calculate_rsi(prices, period=14)
        assert rsi is not None
        assert 50 < rsi < 100  # Uptrend should have RSI > 50


class TestComputePctChange:
    """Tests for compute_pct_change function."""

    def test_insufficient_data(self):
        """Test with insufficient data returns None."""
        short_series = pd.Series([100, 101])
        assert compute_pct_change(short_series, periods=5) is None

    def test_positive_return(self):
        """Test positive price change."""
        prices = pd.Series([100, 100, 100, 100, 100, 110])  # 10% gain
        change = compute_pct_change(prices, periods=5)
        assert change is not None
        assert 9.9 < change < 10.1  # Should be ~10%

    def test_negative_return(self):
        """Test negative price change."""
        prices = pd.Series([100, 100, 100, 100, 100, 90])  # 10% loss
        change = compute_pct_change(prices, periods=5)
        assert change is not None
        assert -10.1 < change < -9.9  # Should be ~-10%

    def test_zero_change(self):
        """Test no price change."""
        prices = pd.Series([100] * 10)
        change = compute_pct_change(prices, periods=5)
        assert change == 0.0

    def test_zero_start_price(self):
        """Test with zero starting price (division by zero protection)."""
        prices = pd.Series([0, 0, 0, 0, 0, 100])
        change = compute_pct_change(prices, periods=5)
        assert change is None  # Should handle gracefully


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
