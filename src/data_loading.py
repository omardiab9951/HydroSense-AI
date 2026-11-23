"""Safe, small data-loading utilities for the raw hydraulic-system dataset."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from .config import N_CYCLES, RAW_DIR, SENSORS, TARGET_COLUMNS


def load_profile() -> pd.DataFrame:
    """Load cycle-aligned condition labels with descriptive column names.

    Returns:
        A DataFrame of shape (2205, 5).
    Raises:
        ValueError: If profile.txt does not match the expected shape or has NaNs.
    """
    profile_path = RAW_DIR / "profile.txt"
    profile = pd.read_csv(profile_path, sep="\t", header=None, names=TARGET_COLUMNS)
    expected_shape = (N_CYCLES, len(TARGET_COLUMNS))
    if profile.shape != expected_shape:
        raise ValueError(f"profile.txt has shape {profile.shape}; expected {expected_shape}.")
    if profile.isna().any().any():
        raise ValueError("profile.txt contains missing values.")
    return profile


def load_sensor(name: str, dtype: str = "float32") -> np.ndarray:
    """Load one sensor file and validate its expected two-dimensional shape.

    High-frequency sensors are intentionally loaded only when requested. Do not
    call this function for all sensors at once because seven files are large.

    Args:
        name: Sensor key from ``config.SENSORS``, such as ``"TS1"`` or ``"PS2"``.
        dtype: Numeric NumPy dtype used to reduce memory use; float32 by default.

    Returns:
        A numeric array with one row per operating cycle.
    Raises:
        KeyError: If ``name`` is not a configured sensor.
        FileNotFoundError: If the corresponding raw file is absent.
        ValueError: If the data shape is unexpected or contains missing values.
    """
    if name not in SENSORS:
        raise KeyError(f"Unknown sensor {name!r}. Choose from: {', '.join(SENSORS)}")
    sensor_path = RAW_DIR / f"{name}.txt"
    if not sensor_path.is_file():
        raise FileNotFoundError(f"Sensor file not found: {sensor_path}")
    frame = pd.read_csv(sensor_path, sep="\t", header=None, dtype=dtype)
    expected_shape = (N_CYCLES, SENSORS[name]["samples_per_cycle"])
    if frame.shape != expected_shape:
        raise ValueError(f"{sensor_path.name} has shape {frame.shape}; expected {expected_shape}.")
    if frame.isna().any().any():
        raise ValueError(f"{sensor_path.name} contains missing values.")
    return frame.to_numpy(dtype=dtype, copy=False)


def load_all_low_rate_sensors() -> dict[str, np.ndarray]:
    """Load only 1 Hz sensors (60 samples/cycle) into a name-to-array mapping.

    Returns:
        Arrays for TS1--TS4, VS1, CE, CP, and SE. This is small enough for EDA.
    """
    low_rate_names = [name for name, meta in SENSORS.items() if meta["samples_per_cycle"] == 60]
    return {name: load_sensor(name) for name in low_rate_names}


def _inspect_file(path: Path, expected_columns: int) -> dict[str, object]:
    """Validate one raw file in chunks to keep peak memory low."""
    try:
        rows = 0
        cols: int | None = None
        nan_count = 0
        # Chunks prevent the ~100 Hz files from creating large temporary frames.
        for chunk in pd.read_csv(path, sep="\t", header=None, dtype="float32", chunksize=256):
            rows += len(chunk)
            cols = chunk.shape[1] if cols is None else cols
            if chunk.shape[1] != cols:
                raise ValueError("inconsistent column count between rows")
            nan_count += int(chunk.isna().sum().sum())
        cols = 0 if cols is None else cols
        ok = rows == N_CYCLES and cols == expected_columns and nan_count == 0
        return {"file": path.name, "rows": rows, "cols": cols,
                "size MiB": round(path.stat().st_size / 1024**2, 2),
                "NaN count": nan_count, "status": "OK" if ok else "FAIL"}
    except Exception as error:  # Keep validation summary useful when a file is corrupt.
        return {"file": path.name, "rows": np.nan, "cols": np.nan,
                "size MiB": round(path.stat().st_size / 1024**2, 2) if path.exists() else np.nan,
                "NaN count": np.nan, "status": f"FAIL: {error}"}


def validate_dataset() -> pd.DataFrame:
    """Validate all sensor and profile files and return a compact summary.

    The function reads one file at a time. It checks expected file presence,
    rows, columns, and missing values without retaining all sensor arrays.

    Returns:
        A DataFrame with file, rows, cols, size MiB, NaN count, and status.
    """
    expected = {"profile.txt": len(TARGET_COLUMNS)}
    expected.update({f"{name}.txt": meta["samples_per_cycle"] for name, meta in SENSORS.items()})
    records = []
    for filename, expected_columns in expected.items():
        path = RAW_DIR / filename
        if path.is_file():
            records.append(_inspect_file(path, expected_columns))
        else:
            records.append({"file": filename, "rows": np.nan, "cols": np.nan,
                            "size MiB": np.nan, "NaN count": np.nan,
                            "status": "FAIL: file not found"})
    return pd.DataFrame(records)
