import numpy as np
import pytest
from vcast.stat import apply_threshold_mask

def test_no_threshold_returns_original():
    f = np.array([[1, 2], [3, 4]])
    r = np.array([[1, 2], [3, 4]])
    f_out, r_out = apply_threshold_mask(f, r)
    assert np.array_equal(f_out, f)
    assert np.array_equal(r_out, r)

def test_threshold_filters_correctly():
    f = np.array([[1, 2], [3, 4]])
    r = np.array([[0, 1], [2, 3]])
    f_out, r_out = apply_threshold_mask(f, r, threshold=2)
    assert np.array_equal(f_out, np.array([2, 3, 4]))
    assert np.array_equal(r_out, np.array([1, 2, 3]))

def test_threshold_no_matches_returns_none():
    f = np.array([[1, 2], [3, 4]])
    r = np.array([[1, 2], [3, 4]])
    f_out, r_out = apply_threshold_mask(f, r, threshold=10)
    assert f_out is None and r_out is None

def test_shape_mismatch_raises():
    f = np.array([[1, 2]])
    r = np.array([[1, 2], [3, 4]])
    with pytest.raises(ValueError):
        apply_threshold_mask(f, r, threshold=2)

