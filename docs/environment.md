# Environment documentation

`configs/reported_environment.json` records the environments described for
data acquisition, model development and numerical control simulation. These
are separate tasks, so the two Python versions and three time intervals are
reported separately.

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
