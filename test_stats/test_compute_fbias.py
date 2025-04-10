import numpy as np
import pytest
from vcast.stat import compute_fbias

@pytest.mark.parametrize(
    "hits, false_alarms, misses, expected",
    [
        (10, 5, 5, 1.0),            # Overforecasting
        (10, 0, 10, 0.5),           # Perfect forecast
        (5, 0, 5, 0.5),             # Balanced
        (5, 5, 5, 1.0),             # Double forecasted
        (0, 0, 0, np.nan),          # No observed events → should return NaN
    ]
)
def test_compute_fbias(hits, false_alarms, misses, expected):
    result = compute_fbias(hits, false_alarms, misses)
    if np.isnan(expected):
        assert np.isnan(result)
    else:
        assert np.isclose(result, expected), f"Expected {expected}, got {result}"