import numpy as np
import pytest
from vcast.stat import compute_gss

@pytest.mark.parametrize(
    "hits, misses, false_alarms, total_events, expected",
    [
        (10, 5, 5, 50, 0.3548387096774194),       # Corrected expected value
        (0, 0, 0, 1, 0.0),                        # No events
        (5, 0, 0, 5, 0.0),                        # Triggers division-by-zero fallback
        (0, 5, 5, 20, -0.14285714285714285),      # Corrected negative GSS
        (3, 3, 3, 30, 0.23076923076923078),       # Corrected expected value
    ]
)
def test_compute_gss_basic_cases(hits, misses, false_alarms, total_events, expected):
    result = compute_gss(hits, misses, false_alarms, total_events)
    assert np.isclose(result, expected), f"GSS failed: got {result}, expected {expected}"

def test_compute_gss_division_by_zero():
    # This creates a case where the denominator becomes zero → should return 0.0
    hits, misses, false_alarms, total_events = 0, 0, 0, 1
    result = compute_gss(hits, misses, false_alarms, total_events)
    assert result == 0.0
