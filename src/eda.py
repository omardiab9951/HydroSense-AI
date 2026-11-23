"""Memory-conscious, reusable helpers for Sprint 1 exploratory data analysis."""

from __future__ import annotations

import gc
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from .config import N_CYCLES, PROCESSED_DIR, SENSORS, TARGET_COLUMNS
from .data_loading import load_sensor


EDA_CACHE_PARQUET = PROCESSED_DIR / "eda_cycle_summary.parquet"
EDA_CACHE_CSV = PROCESSED_DIR / "eda_cycle_summary.csv"


def compute_cycle_summary(sensor_names: Iterable[str] | None = None) -> pd.DataFrame:
    """Compute per-cycle mean, std, min, and max for requested sensors.

    This is an **EDA-only cache**, not a Sprint 2 feature dataset. Each sensor is
    loaded as float32, summarized, and released before the next sensor is read.

    Args:
        sensor_names: Configured sensor names. ``None`` uses all 17 sensors.

    Returns:
        DataFrame with 2,205 rows and four summary columns per sensor.
    """
    names = list(SENSORS if sensor_names is None else sensor_names)
    unknown = set(names) - set(SENSORS)
    if unknown:
        raise KeyError(f"Unknown sensor names: {sorted(unknown)}")

    # Reuse only the complete all-sensor cache. Partial requests are computed fresh.
    if set(names) == set(SENSORS):
        for cache_path in (EDA_CACHE_PARQUET, EDA_CACHE_CSV):
            if cache_path.exists():
                cached = (pd.read_parquet(cache_path) if cache_path.suffix == ".parquet"
                          else pd.read_csv(cache_path))
                expected_columns = {f"{sensor}_{stat}" for sensor in SENSORS
                                    for stat in ("mean", "std", "min", "max")}
                if cached.shape[0] == N_CYCLES and expected_columns.issubset(cached.columns):
                    return cached

    summary: dict[str, np.ndarray] = {}
    for name in names:
        values = load_sensor(name, dtype="float32")
        summary[f"{name}_mean"] = values.mean(axis=1, dtype=np.float64)
        summary[f"{name}_std"] = values.std(axis=1, dtype=np.float64)
        summary[f"{name}_min"] = values.min(axis=1)
        summary[f"{name}_max"] = values.max(axis=1)
        del values
        gc.collect()

    result = pd.DataFrame(summary)
    if set(names) == set(SENSORS):
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        try:
            result.to_parquet(EDA_CACHE_PARQUET, index=False)
            if EDA_CACHE_CSV.exists():
                EDA_CACHE_CSV.unlink()
        except Exception:
            result.to_csv(EDA_CACHE_CSV, index=False)
    return result


def check_label_combinations(profile: pd.DataFrame) -> pd.DataFrame:
    """Count unique four-component condition combinations in profile labels.

    Args:
        profile: Loaded profile DataFrame with the configured target columns.

    Returns:
        Combination counts sorted from most to least frequent.
    """
    condition_columns = TARGET_COLUMNS[:4]
    return (profile.groupby(condition_columns, dropna=False).size().rename("count")
            .reset_index().sort_values("count", ascending=False, kind="stable")
            .reset_index(drop=True))


def row_order_check(profile: pd.DataFrame) -> pd.DataFrame:
    """Compare observed label changes to the expectation under random row order.

    For a randomly shuffled categorical variable, the expected probability that
    adjacent labels differ is ``1 - sum(p_i^2)``. Much fewer changes indicates
    condition-grouped row ordering rather than random ordering.

    Args:
        profile: Loaded profile DataFrame.

    Returns:
        One row per target with observed and random-order expected changes.
    """
    records = []
    transitions = len(profile) - 1
    for target in TARGET_COLUMNS[:4]:
        probabilities = profile[target].value_counts(normalize=True)
        expected_rate = 1 - float((probabilities ** 2).sum())
        observed_changes = int(profile[target].ne(profile[target].shift()).iloc[1:].sum())
        records.append({
            "target": target,
            "transitions": transitions,
            "observed_changes": observed_changes,
            "observed_change_rate": observed_changes / transitions,
            "expected_random_changes": transitions * expected_rate,
            "expected_random_change_rate": expected_rate,
            "ordering": "grouped" if observed_changes < transitions * expected_rate * 0.5 else "mixed",
        })
    return pd.DataFrame(records)


def count_outliers_iqr(df: pd.DataFrame) -> pd.DataFrame:
    """Count observations outside the 1.5 IQR fence for every numeric column.

    This reports potential outliers only. It neither removes nor alters values.

    Args:
        df: Numeric DataFrame to inspect.

    Returns:
        DataFrame with quartiles, fences, and outlier counts by column.
    """
    numeric = df.select_dtypes(include=np.number)
    records = []
    for column in numeric.columns:
        series = numeric[column].dropna()
        q1, q3 = series.quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        records.append({"column": column, "q1": q1, "q3": q3, "iqr": iqr,
                        "lower_fence": lower, "upper_fence": upper,
                        "outlier_count": int(((series < lower) | (series > upper)).sum())})
    return pd.DataFrame(records)


def sensor_quality_checks(sensor_names: Iterable[str] | None = None) -> pd.DataFrame:
    """Inspect raw sensor quality one sensor at a time without modifying data.

    Reports NaN/inf counts, duplicated complete cycles, constant cycles/columns,
    and observed value bounds. Duplicate cycles use row-byte hashing for a compact
    exact comparison after loading one sensor.

    Args:
        sensor_names: Configured sensors to check; ``None`` checks all sensors.

    Returns:
        One quality-summary row per sensor.
    """
    names = list(SENSORS if sensor_names is None else sensor_names)
    records = []
    for name in names:
        values = load_sensor(name, dtype="float32")
        row_hashes = pd.util.hash_pandas_object(pd.DataFrame(values), index=False).to_numpy()
        records.append({
            "sensor": name,
            "NaN_count": int(np.isnan(values).sum()),
            "inf_count": int(np.isinf(values).sum()),
            "duplicate_full_cycles": int(len(row_hashes) - len(np.unique(row_hashes))),
            "constant_cycles": int(np.count_nonzero(np.ptp(values, axis=1) == 0)),
            "constant_columns": int(np.count_nonzero(np.ptp(values, axis=0) == 0)),
            "observed_min": float(values.min()),
            "observed_max": float(values.max()),
        })
        del values, row_hashes
        gc.collect()
    return pd.DataFrame(records)
