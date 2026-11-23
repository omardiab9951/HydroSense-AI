"""Project paths and dataset metadata for HydroSense AI."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_RAW_DIR = PROJECT_ROOT / "dataset" / "raw"


def _find_raw_dir() -> Path:
    """Return the folder containing profile.txt, including a one-level fallback."""
    if (_DEFAULT_RAW_DIR / "profile.txt").is_file():
        return _DEFAULT_RAW_DIR
    if _DEFAULT_RAW_DIR.is_dir():
        matches = [path.parent for path in _DEFAULT_RAW_DIR.rglob("profile.txt")]
        if len(matches) == 1:
            return matches[0]
    return _DEFAULT_RAW_DIR


RAW_DIR = _find_raw_dir()
PROCESSED_DIR = PROJECT_ROOT / "dataset" / "processed"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
RESULTS_DIR = PROJECT_ROOT / "reports" / "results"
MODELS_DIR = PROJECT_ROOT / "models"

N_CYCLES = 2205
CYCLE_SECONDS = 60
RANDOM_STATE = 42

SENSORS = {
    **{f"PS{i}": {"group": "pressure", "unit": "bar", "sampling_hz": 100,
                    "samples_per_cycle": 6000} for i in range(1, 7)},
    "EPS1": {"group": "motor power", "unit": "W", "sampling_hz": 100,
             "samples_per_cycle": 6000},
    "FS1": {"group": "flow", "unit": "l/min", "sampling_hz": 10,
            "samples_per_cycle": 600},
    "FS2": {"group": "flow", "unit": "l/min", "sampling_hz": 10,
            "samples_per_cycle": 600},
    **{f"TS{i}": {"group": "temperature", "unit": "deg C", "sampling_hz": 1,
                    "samples_per_cycle": 60} for i in range(1, 5)},
    "VS1": {"group": "vibration", "unit": "mm/s", "sampling_hz": 1,
            "samples_per_cycle": 60},
    "CE": {"group": "virtual cooling", "unit": "%", "sampling_hz": 1,
           "samples_per_cycle": 60},
    "CP": {"group": "virtual cooling", "unit": "kW", "sampling_hz": 1,
           "samples_per_cycle": 60},
    "SE": {"group": "efficiency", "unit": "%", "sampling_hz": 1,
           "samples_per_cycle": 60},
}

TARGET_COLUMNS = ["cooler", "valve", "pump", "accumulator", "stable"]
TARGET_MEANINGS = {
    "cooler": {3: "near failure", 20: "reduced efficiency", 100: "full efficiency"},
    "valve": {100: "optimal switching behavior", 90: "small lag", 80: "severe lag",
              73: "near failure"},
    "pump": {0: "no leakage", 1: "weak leakage", 2: "severe leakage"},
    "accumulator": {130: "optimal pressure", 115: "slightly reduced pressure",
                    100: "severely reduced pressure", 90: "near failure"},
    "stable": {0: "stable", 1: "static conditions might not have been reached yet"},
}
