# Data formats

## Prediction evaluation

Provide a UTF-8 CSV with a header and finite numeric `observed` and `predicted`
columns. Column names can be changed through command-line arguments. Each row
must pair the observation and prediction for the same target time. The tool
does not align mismatched timestamps or reconstruct missing predictions.

DO values should use the same units, normally mg/L. MAE and RMSE then have units
of mg/L; MSE has squared units. R² is dimensionless and can be negative. For a
constant observed series, R² is reported as JSON `null` because its denominator
is zero. MAPE is returned as a percentage using
`max(abs(observed), epsilon)` as its denominator. The default `epsilon=1e-8` is
an explicit utility setting; specify another value when required by the
evaluation protocol. Near-zero observations can make MAPE sensitive to this
choice.

Use one evaluation per forecast horizon and per retained model output. A
mean of per-run metrics is different from a metric calculated after averaging
predictions; decide and document the aggregation before combining runs.

## Monitoring inspection

Provide an ISO-8601 timestamp column, such as `2026-01-01T12:30:00+08:00`.
The timestamp is a format example, not an experimental date. Do not mix
timestamps with and without timezones. The inspection utility reports
duplicates, backward steps and interval mismatches without reordering rows.

Split ranges are Python-style `[start, end)` row-index intervals. Training
and validation sizes are rounded down, and the remainder is assigned to the
test block. When times are not strictly increasing, the output explicitly
marks these ranges as not chronologically valid. Split boundaries do not, by
themselves, make interpolation, scaling or feature construction causal.

No experimental CSV files are distributed in this initial release. A future
data release should specify variable definitions, units, nitrogen reporting
basis, timestamps, forecast origins, target times, preprocessing and split
membership alongside each file.
