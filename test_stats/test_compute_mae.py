import numpy as np
import pytest
from vcast.stat import compute_mae

# Shared test data
forecast = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

reference = np.array([
    [1, 1, 2],
    [2, 5, 6]
])

@pytest.mark.parametrize(
    "f, r, expected",
    [
        (forecast, reference, 0.6666666666666666),  # abs diffs: [0,1,1,2,0,0] → mean = 4/6
        (forecast, forecast, 0.0),                 # identical arrays → MAE = 0
        (np.array([[0, 0], [0, 0]]), np.array([[1, 1], [1, 1]]), 1.0),  # all abs diffs = 1
    ]
)
def test_compute_mae_basic_cases(f, r, expected):
    result = compute_mae(f, r)
    assert np.isclose(result, expected), f"Expected {expected}, got {result}"

def test_compute_mae_shape_mismatch():
    f = np.array([[1, 2]])
    r = np.array([[1, 2], [3, 4]])
    with pytest.raises(ValueError):
        compute_mae(f, r)