import numpy as np
import pytest
from vcast.stat import compute_quantiles

def test_compute_quantiles_basic():
    f = np.array([[2, 4], [6, 8]])
    r = np.array([[1, 3], [5, 7]])
    result = compute_quantiles(f, r)
    # diffs = [1, 1, 1, 1] → All stats will be on a constant array
    q1, q2, q3, iqr, lw, uw = result
    assert q1 == q2 == q3 == 1.0
    assert iqr == 0.0
    assert lw == uw == 1.0

def test_compute_quantiles_with_outliers():
    f = np.array([[2, 4], [100, 200]])
    r = np.array([[1, 3], [5, 7]])
    result = compute_quantiles(f, r)
    q1, q2, q3, iqr, lw, uw = result
    assert q1 < q2 < q3
    assert iqr > 0
    assert lw < q1 and uw > q3

def test_compute_quantiles_shape_mismatch():
    f = np.array([[1, 2]])
    r = np.array([[1, 2], [3, 4]])
    with pytest.raises(ValueError):
        compute_quantiles(f, r)

