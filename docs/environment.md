# Environment documentation

`configs/reported_environment.json` records the environments described for
data acquisition, model development and numerical control simulation. These
are separate tasks, so the two Python versions and three time intervals are
reported separately.

The eight-step DO forecast uses 30 min steps and informs outer-loop aeration
adjustment. The simulation controller executes at 1 s intervals, with a separate
0.01 s integration step. The forecast grid does not specify a 1 s model forecast
refresh interval.

The field DO comparison in Figure 5f and Supplementary Table S7 used separate
periods in the same pond on the same aeration equipment. Each of the three
strategies was evaluated for 7 d at a common 7 mg/L DO setpoint, with records
every 30 min and a common prescribed feeding regime. The plotted horizontal
axis is the sample index within each strategy-specific record. Figure 5a-d
instead reports laboratory ammonia-nitrogen and COD tests using field-collected
water, measured every 10 min. The JSON configuration records these distinct
experimental settings and time scales.

The utilities in `tools/` require only the Python standard library. Run them
with Python 3.11; there is no need to install PyTorch or MATLAB to compute the
CSV metrics or inspect timestamps.

The model-development configuration records PyTorch 2.6.0 with its CUDA 12.4
build. A CUDA build identifier does not specify the installed GPU driver or a
separately installed CUDA Toolkit. Driver, cuDNN and pigpio versions are not
assigned invented values in the JSON configuration. MATLAB/Simulink R2025a
and the named toolboxes are proprietary software and are not included here.

To record the environment actually used for a run:

```sh
python tools/collect_environment.py > local_environment.json
```

Inspect that file before sharing it. Package versions in the collected output
describe the current machine, while the reported JSON describes the study's
documented configuration. Installing matching versions alone does not reproduce
the full training or control experiment; data, training implementation,
checkpoints and complete execution settings are also required.
