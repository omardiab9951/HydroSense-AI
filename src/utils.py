"""Small reusable utilities for reproducible Sprint 1 analysis."""

from __future__ import annotations

import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .config import FIGURES_DIR


def set_random_seeds(seed: int = 42) -> None:
    """Set Python and NumPy random seeds for repeatable notebook results."""
    random.seed(seed)
    np.random.seed(seed)


def set_plot_style() -> None:
    """Apply a clear, consistent Matplotlib style for notebook figures."""
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({"figure.figsize": (9, 5), "axes.titlesize": 13,
                         "axes.labelsize": 11, "figure.dpi": 100})


def save_figure(fig: plt.Figure, name: str) -> Path:
    """Save a Matplotlib figure under reports/figures at 150 dpi.

    Args:
        fig: Figure object to save.
        name: Filename with or without a file extension.

    Returns:
        The path to the saved PNG file.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    filename = name if Path(name).suffix else f"{name}.png"
    output_path = FIGURES_DIR / filename
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    return output_path
