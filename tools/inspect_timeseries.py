"""Inspect timestamp order and split boundaries without modifying observations."""
import argparse
import csv
from datetime import datetime
import json
import math
import statistics


def chronological_ranges(n, ratios=(0.70, 0.15, 0.15)):
    if n < 1 or len(ratios) != 3 or any(not math.isfinite(x) or x <= 0 for x in ratios):
        raise ValueError("Provide a positive record count and three positive finite ratios")
    if not math.isclose(sum(ratios), 1.0, abs_tol=1e-9):
        raise ValueError("Split ratios must sum to one")
    a = math.floor(n * ratios[0])
    b = a + math.floor(n * ratios[1])
    if min(a, b - a, n - b) < 1:
        raise ValueError("Each split must contain at least one record")
    return {"train": [0, a], "validation": [a, b], "test": [b, n]}


def inspect(timestamps, expected_interval_seconds=None):
    if len(timestamps) < 2:
        raise ValueError("At least two timestamped records are required")
    if expected_interval_seconds is not None and (
        not math.isfinite(expected_interval_seconds) or expected_interval_seconds <= 0
    ):
        raise ValueError("Expected interval must be finite and positive")
    aware = [x.utcoffset() is not None for x in timestamps]
    if any(aware) and not all(aware):
        raise ValueError("Do not mix timezone-aware and timezone-naive timestamps")
    intervals = [(b - a).total_seconds() for a, b in zip(timestamps, timestamps[1:])]
    return {
        "n_records": len(timestamps),
        "strictly_increasing": all(x > 0 for x in intervals),
        "duplicate_timestamps": len(timestamps) - len(set(timestamps)),
        "backward_steps": sum(x < 0 for x in intervals),
        "interval_seconds": {
            "minimum": min(intervals), "median": statistics.median(intervals), "maximum": max(intervals)
        },
        "expected_interval_seconds": expected_interval_seconds,
        "interval_mismatches": None if expected_interval_seconds is None else sum(
            not math.isclose(x, expected_interval_seconds, abs_tol=1e-6) for x in intervals
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file")
    parser.add_argument("--timestamp", default="timestamp")
    parser.add_argument("--expected-interval-seconds", type=float)
    parser.add_argument("--split", type=float, nargs=3, default=(0.7, 0.15, 0.15))
    args = parser.parse_args()
    try:
        timestamps = []
        with open(args.csv_file, newline="", encoding="utf-8-sig") as source:
            reader = csv.DictReader(source)
            if not reader.fieldnames or args.timestamp not in reader.fieldnames:
                raise ValueError("Timestamp column is absent")
            for row_number, row in enumerate(reader, 2):
                try:
                    timestamps.append(datetime.fromisoformat(row[args.timestamp].replace("Z", "+00:00")))
                except (ValueError, TypeError, AttributeError) as error:
                    raise ValueError(f"Invalid ISO-8601 timestamp in CSV row {row_number}") from error
        report = inspect(timestamps, args.expected_interval_seconds)
        report["split_index_ranges_start_inclusive_end_exclusive"] = chronological_ranges(len(timestamps), args.split)
        report["split_ranges_are_chronological"] = report["strictly_increasing"]
        print(json.dumps(report, indent=2, allow_nan=False))
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
