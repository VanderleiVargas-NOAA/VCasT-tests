import numpy as np
import pytest
from vcast.stat import compute_csi

@pytest.mark.parametrize(
    "hits, misses, false_alarms, expected",
    [
        (10, 5, 5, 0.5),         # hits / (hits + misses + fa)
        (10, 0, 0, 1.0),
        (0, 5, 5, 0.0),
        (0, 0, 0, np.nan)
    ]
)
def test_compute_csi(hits, misses, false_alarms, expected):
    result = compute_csi(hits, misses, false_alarms)
    if np.isnan(expected):
        assert np.isnan(result)
    else:
        assert np.isclose(result, expected)