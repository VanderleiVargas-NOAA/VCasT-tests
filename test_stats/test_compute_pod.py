import numpy as np
import pytest
from vcast.stat import compute_pod

@pytest.mark.parametrize(
    "hits, misses, expected",
    [
        (10, 5, 0.6666666666666666),
        (0, 10, 0.0),
        (10, 0, 1.0),
        (0, 0, np.nan)
    ]
)
def test_compute_pod(hits, misses, expected):
    result = compute_pod(hits, misses)
    if np.isnan(expected):
        assert np.isnan(result)
    else:
        assert np.isclose(result, expected)