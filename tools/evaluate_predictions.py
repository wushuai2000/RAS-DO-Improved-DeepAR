"""Evaluate aligned DO predictions without altering the input series."""
import argparse
import csv
import json
import math


def calculate_metrics(observed, predicted, epsilon=1e-8):
    observed = list(observed)
    predicted = list(predicted)
    if not observed or len(observed) != len(predicted):
        raise ValueError("Observed and predicted series must have equal nonzero lengths")
    if not math.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("epsilon must be finite and positive")
    if not all(math.isfinite(x) for x in observed + predicted):
        raise ValueError("All evaluated values must be finite")
    errors = [p - y for y, p in zip(observed, predicted)]
    n = len(errors)
    squared_error = math.fsum(e * e for e in errors)
    mean_y = math.fsum(observed) / n
    total_squares = math.fsum((y - mean_y) ** 2 for y in observed)
    mse = squared_error / n
    return {
        "n_evaluated": n,
        "MAE": math.fsum(abs(e) for e in errors) / n,
        "MSE": mse,
        "RMSE": math.sqrt(mse),
        "MAPE_percent": 100 * math.fsum(
            abs(e) / max(abs(y), epsilon) for e, y in zip(errors, observed)
        ) / n,
        "R2": 1 - squared_error / total_squares if total_squares > 0 else None,
        "MAPE_denominator_epsilon": epsilon,
    }


def read_pairs(path, observed_column, predicted_column):
    observed, predicted = [], []
    with open(path, newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames or not {observed_column, predicted_column}.issubset(reader.fieldnames):
            raise ValueError("CSV does not contain the requested observed and predicted columns")
        for row_number, row in enumerate(reader, 2):
            try:
                observed.append(float(row[observed_column]))
                predicted.append(float(row[predicted_column]))
            except (TypeError, ValueError) as error:
                raise ValueError(f"Nonnumeric or missing prediction value in CSV row {row_number}") from error
    return observed, predicted


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file")
    parser.add_argument("--observed", default="observed")
    parser.add_argument("--predicted", default="predicted")
    parser.add_argument("--epsilon", type=float, default=1e-8)
    args = parser.parse_args()
    try:
        y, p = read_pairs(args.csv_file, args.observed, args.predicted)
        print(json.dumps(calculate_metrics(y, p, args.epsilon), indent=2, allow_nan=False))
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
