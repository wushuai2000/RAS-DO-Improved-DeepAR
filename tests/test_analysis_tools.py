"""Arithmetic and validation examples, not experimental measurements."""
from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


metrics = load("evaluate_predictions")
series = load("inspect_timeseries")


class AnalysisToolsTests(unittest.TestCase):
    def test_arithmetic(self):
        result = metrics.calculate_metrics([1, 2, 3], [2, 2, 2])
        self.assertAlmostEqual(result["MAE"], 2 / 3)
        self.assertAlmostEqual(result["MSE"], 2 / 3)
        self.assertEqual(result["R2"], 0)
        self.assertAlmostEqual(result["MAPE_percent"], 400 / 9)

    def test_constant_target(self):
        self.assertIsNone(metrics.calculate_metrics([2, 2], [2, 3])["R2"])

    def test_invalid_pairs(self):
        for observed, predicted in [([], []), ([1], [1, 2]), ([float("nan")], [1])]:
            with self.assertRaises(ValueError):
                metrics.calculate_metrics(observed, predicted)

    def test_zero_target_denominator(self):
        self.assertEqual(metrics.calculate_metrics([0], [1], epsilon=0.5)["MAPE_percent"], 200)

    def test_split_covers_all_rows(self):
        self.assertEqual(series.chronological_ranges(20), {"train": [0, 14], "validation": [14, 17], "test": [17, 20]})
        with self.assertRaises(ValueError):
            series.chronological_ranges(2)

    def test_interval_and_order(self):
        start = datetime(2026, 1, 1)
        values = [start, start + timedelta(minutes=30), start + timedelta(minutes=90)]
        report = series.inspect(values, 1800)
        self.assertTrue(report["strictly_increasing"])
        self.assertEqual(report["interval_mismatches"], 1)
        self.assertFalse(series.inspect(list(reversed(values)))["strictly_increasing"])

    def test_duplicate_times(self):
        start = datetime(2026, 1, 1)
        self.assertEqual(series.inspect([start, start])["duplicate_timestamps"], 1)

    def test_mixed_timezones(self):
        with self.assertRaises(ValueError):
            series.inspect([datetime(2026, 1, 1), datetime(2026, 1, 1, tzinfo=timezone.utc)])


if __name__ == "__main__":
    unittest.main()
