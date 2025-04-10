import numpy as np
import pytest
from vcast.stat import compute_far

@pytest.mark.parametrize(
    "hits, false_alarms, expected",
    [
        (10, 5, 0.3333333333333333),
        (0, 10, 1.0),
        (10, 0, 0.0),
        (0, 0, np.nan)
    ]
)
def test_compute_far(hits, false_alarms, expected):
    result = compute_far(hits, false_alarms)
    if np.isnan(expected):
        assert np.isnan(result)
    else:
        assert np.isclose(result, expected)