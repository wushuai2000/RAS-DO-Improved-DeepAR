# RAS DO Improved DeepAR

Supporting code and configuration documentation for dissolved-oxygen (DO)
forecasting and aeration control in a recirculating aquaculture system (RAS).

This initial release provides portable analysis utilities and the hardware,
software and Improved DeepAR settings documented for the study. The full model
training implementation, trained weights and experimental datasets are outside
the scope of this release. Configuration documentation is not a substitute for
those additional materials when reproducing the complete experiments.

## Contents

| Path | Purpose |
|---|---|
| `tools/evaluate_predictions.py` | Compute MAE, MSE, RMSE, MAPE and R² from aligned observed and predicted values. |
| `tools/inspect_timeseries.py` | Check timestamp order, duplicate times, intervals and chronological split boundaries without changing the data. |
| `tools/collect_environment.py` | Report the local Python version and installed package versions. |
| `configs/reported_environment.json` | Documented acquisition, model-development and simulation environments. |
| `configs/improved_deepar.json` | Documented model architecture, regularization, selection and stopping settings. |
| `docs/data_format.md` | Input formats and interpretation of the utilities. |
| `docs/environment.md` | Environment setup and the distinction between reported settings and a locally collected runtime. |
| `tests/test_analysis_tools.py` | Small arithmetic and input-validation tests; these are not experimental observations. |

## Quick start

The three utilities and their tests use the Python standard library. Python
3.11 is recommended. Supply your own CSV files using the schema in
[`docs/data_format.md`](docs/data_format.md).

```sh
python tools/evaluate_predictions.py predictions.csv --observed observed --predicted predicted
python tools/inspect_timeseries.py monitoring.csv --timestamp timestamp --expected-interval-seconds 1800
python tools/collect_environment.py
python -m unittest discover -s tests -v
```

No tool silently sorts, fills, smooths, resamples or overwrites input data. The
evaluation tool requires rows that already represent the same target times and
forecast task. Predictions at different forecast horizons should be evaluated
separately unless the aggregation rule is explicitly specified.

## Configuration and release scope

The JSON configurations transcribe settings reported in the revised manuscript
and Supplementary Tables S3i and S9. They describe the study environment; the
analysis utilities do not train Improved DeepAR, implement RUN, execute the
controllers or operate physical aeration equipment. Use the environment
collection tool to record the versions actually installed when running code.

The repository URL is <https://github.com/wushuai2000/RAS-DO-Improved-DeepAR>.
The existing [MIT License](LICENSE) applies to the released code. Keep data,
credentials, checkpoints and unpublished review documents out of commits unless
they are deliberately prepared for a later release.
