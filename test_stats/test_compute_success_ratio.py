import numpy as np
import pytest
from vcast.stat import compute_success_ratio

@pytest.mark.parametrize(
    "hits, false_alarms, expected",
    [
        (10, 5, 0.6666666666666667),  # 1 - FAR = 1 - 5/15 = 0.666...
        (10, 0, 1.0),
        (0, 10, 0.0),
        (0, 0, np.nan)
    ]
)

def test_compute_success_ratio(hits, false_alarms, expected):
    result = compute_success_ratio(hits, false_alarms)
    if np.isnan(expected):
        assert np.isnan(result)
    else:
        assert np.isclose(result, expected)