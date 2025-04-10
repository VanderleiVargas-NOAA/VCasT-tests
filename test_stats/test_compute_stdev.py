import numpy as np
import pytest
from vcast.stat import compute_stdev

def test_compute_stdev_normal():
    arr = np.array([[1, 2, 3], [4, 5, 6]])
    expected = np.std(arr)
    result = compute_stdev(arr, arr)
    assert np.isclose(result, expected)

def test_compute_stdev_shape_mismatch():
    with pytest.raises(ValueError):
        compute_stdev(np.array([1, 2]), np.array([[1, 2], [3, 4]]))

