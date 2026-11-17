import pytest

from priority_score import calculate_priority_score


@pytest.mark.parametrize(
    ("severity", "metric_value", "threshold", "expected_score"),
    [
        ("critical", 1.5, 1.0, 80),
        ("warning", 1.5, 1.0, 50),
        ("info", 1.5, 1.0, 30),
    ],
)
def test_calculate_priority_score_above_threshold_returns_int(
    severity, metric_value, threshold, expected_score
):
    score = calculate_priority_score(severity, metric_value, threshold)

    assert score == expected_score
    assert isinstance(score, int)


# --- Edge cases added manually ---
def test_unknown_severity_raises_value_error():
    with pytest.raises(ValueError, match="Unsupported severity"):
        calculate_priority_score("emergency", 100, 90)


def test_zero_threshold_raises_value_error():
    with pytest.raises(ValueError, match="threshold must not be zero"):
        calculate_priority_score("critical", 50, 0)


def test_metric_below_threshold_gets_no_bonus():
    assert calculate_priority_score("warning", -20, 10) == 30
