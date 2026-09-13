"""Print the current Python and installed package versions; does not import models."""
import importlib.metadata
import json
import platform


def collect():
    packages = {}
    for name in ["numpy", "pandas", "scipy", "scikit-learn", "matplotlib", "torch", "shap", "optuna", "pigpio"]:
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    return {"python": platform.python_version(), "system": platform.system(),
            "system_release": platform.release(), "architecture": platform.machine(),
            "installed_packages": packages}


if __name__ == "__main__":
    print(json.dumps(collect(), indent=2))
