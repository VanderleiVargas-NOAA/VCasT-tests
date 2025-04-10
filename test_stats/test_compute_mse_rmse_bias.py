import numpy as np
import pytest
from vcast.stat import compute_mse, compute_rmse, compute_bias

@pytest.fixture
def data():
    forecast = np.array([[1, 2], [3, 4]])
    reference = np.array([[1, 1], [3, 3]])
    return forecast, reference

# Forecast: [[1, 2], [3, 4]]
# Reference: [[1, 1], [3, 3]]
# Differences: [[0, 1], [0, 1]]

@pytest.mark.parametrize("threshold, expected", [
    (None, 0.5),  # all 4 points: (0^2 + 1^2 + 0^2 + 1^2)/4 = 0.5
    (2, 2/3),     # forecast >= 2 → [2, 3, 4] vs [1, 3, 3] → diffs = [1, 0, 1] → mse = 2/3
    (4, 1.0),     # only forecast=4 → ref=3 → diff^2 = 1
    (5, np.nan),  # no forecast >= 5
])
def test_compute_mse(data, threshold, expected):
    f, r = data
    result = compute_mse(f, r, threshold=threshold)
    if np.isnan(expected):
        assert np.isnan(result)
    else:
        assert np.isclose(result, expected)

@pytest.mark.parametrize("threshold, expected", [
    (None, np.sqrt(0.5)),           # sqrt(0.5) ≈ 0.7071
    (2, np.sqrt(2/3)),              # ≈ 0.8165
    (4, 1.0),                       # sqrt(1)
    (5, np.nan),
])
def test_compute_rmse(data, threshold, expected):
    f, r = data
    result = compute_rmse(f, r, threshold=threshold)
    if np.isnan(expected):
        assert np.isnan(result)
    else:
        assert np.isclose(result, expected)

@pytest.mark.parametrize("threshold, expected", [
    (None, 0.5),    # diffs: [0,1,0,1] → mean = 0.5
    (2, 2/3),       # diffs: [1, 0, 1] → mean = 2/3
    (4, 1.0),       # diff: 1
    (5, np.nan),
])
def test_compute_bias(data, threshold, expected):
    f, r = data
    result = compute_bias(f, r, threshold=threshold)
    if np.isnan(expected):
        assert np.isnan(result)
    else:
        assert np.isclose(result, expected)

