import numpy as np
import pytest
from vcast.stat import compute_correlation

@pytest.mark.parametrize(
    "f, r, expected",
    [
        ([1, 2, 3], [1, 2, 3], 1.0),
        ([1, 2, 3], [3, 2, 1], -1.0),
        ([1, 2, 3], [1, 1, 1], np.nan),
    ]
)
def test_compute_correlation_basic(f, r, expected):
    result = compute_correlation(np.array(f), np.array(r))
    if np.isnan(expected):
        assert np.isnan(result)
    else:
        assert np.isclose(result, expected)

def test_compute_correlation_shape_mismatch():
    with pytest.raises(ValueError):
        compute_correlation(np.array([1, 2, 3]), np.array([[1, 2, 3]]))

