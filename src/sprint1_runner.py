"""Executable Sprint 1 reporting routines used by the notebooks."""
from __future__ import annotations

import gc
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from . import config
from .data_loading import load_profile, load_sensor, validate_dataset
from .eda import compute_cycle_summary, check_label_combinations, row_order_check, count_outliers_iqr, sensor_quality_checks
from .utils import save_figure, set_plot_style


def _target_table() -> pd.DataFrame:
    """Build a flat target-definition table."""
    return pd.DataFrame([
        {"column": target, "value": value, "meaning": meaning, "number_of_classes": len(labels)}
        for target, labels in config.TARGET_MEANINGS.items()
        for value, meaning in labels.items()
    ])


def run_data_understanding() -> dict[str, object]:
    """Produce Sprint 1 data-understanding tables and figures without altering raw data."""
    set_plot_style(); config.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    inventory = pd.DataFrame([{"file": p.name, "size_MiB": round(p.stat().st_size / 1024**2, 2)}
                              for p in sorted(config.RAW_DIR.iterdir()) if p.is_file()])
    sensor_table = pd.DataFrame.from_dict(config.SENSORS, orient="index").rename_axis("sensor").reset_index()
    sensor_table["what_it_measures"] = sensor_table["group"].map(lambda x: f"Measures {x} in each 60-second cycle.")
    sensor_table.to_csv(config.RESULTS_DIR / "sensor_description_table.csv", index=False)
    target_table = _target_table(); target_table.to_csv(config.RESULTS_DIR / "target_description_table.csv", index=False)
    validation = validate_dataset(); validation.to_csv(config.RESULTS_DIR / "validation_summary.csv", index=False)
    profile = load_profile()
    slices = []
    for name in config.SENSORS:
        values = load_sensor(name)
        slices.append({"sensor": name, "shape": str(values.shape), "dtype": str(values.dtype),
                       "first_cycle_first5": values[0, :5].tolist(), "first_cycle_last5": values[0, -5:].tolist(),
                       "last_cycle_first5": values[-1, :5].tolist(), "last_cycle_last5": values[-1, -5:].tolist()})
        del values; gc.collect()
    slice_table = pd.DataFrame(slices); slice_table.to_csv(config.RESULTS_DIR / "sensor_slice_checks.csv", index=False)
    dist_records=[]
    for target in config.TARGET_COLUMNS:
        counts=profile[target].value_counts().sort_index(); ratio=counts.max()/counts.min()
        for value,count in counts.items(): dist_records.append({"target":target,"value":value,"count":int(count),"percentage":round(count*100/len(profile),2),"largest_smallest_ratio":round(ratio,3)})
        fig,ax=plt.subplots(); counts.plot.bar(ax=ax); ax.set(title=f"{target} class distribution",xlabel=target,ylabel="cycles"); save_figure(fig,f"01_class_distribution_{target}"); plt.close(fig)
    distributions=pd.DataFrame(dist_records); distributions.to_csv(config.RESULTS_DIR / "class_distributions.csv",index=False)
    combos=check_label_combinations(profile); combos.to_csv(config.RESULTS_DIR / "label_combinations.csv",index=False)
    order=row_order_check(profile); order.to_csv(config.RESULTS_DIR / "row_order_check.csv",index=False)
    fig,axes=plt.subplots(4,1,figsize=(12,8),sharex=True)
    for ax,target in zip(axes,config.TARGET_COLUMNS[:4]): ax.step(profile.index,profile[target],where="mid"); ax.set_ylabel(target)
    axes[-1].set_xlabel("row index"); save_figure(fig,"01_row_order_labels"); plt.close(fig)
    quality=sensor_quality_checks()
    quality.to_csv(config.RESULTS_DIR / "data_quality_checks.csv",index=False)
    return {"inventory":inventory,"sensor_table":sensor_table,"target_table":target_table,"validation":validation,"profile":profile,"slices":slice_table,"distributions":distributions,"combinations":combos,"order":order,"quality":quality}


def _rows_for_target(profile: pd.DataFrame, target: str) -> dict[int, int]:
    """Choose deterministic examples, preferring healthy settings for other targets."""
    healthy={"cooler":100,"valve":100,"pump":0,"accumulator":130}; rows={}
    for value in sorted(profile[target].unique()):
        mask=profile[target].eq(value)
        for other,setting in healthy.items():
            if other != target: mask &= profile[other].eq(setting)
        candidates=profile.index[mask]
        if len(candidates)==0: candidates=profile.index[profile[target].eq(value)]
        rows[int(value)]=int(candidates[0])
    return rows


def _signal_plot(sensor: str, target: str, rows: dict[int,int], mean: bool, profile: pd.DataFrame, filename: str) -> None:
    """Create one memory-safe raw-signal comparison figure."""
    values=load_sensor(sensor); meta=config.SENSORS[sensor]; time=np.arange(values.shape[1])/meta["sampling_hz"]
    fig,ax=plt.subplots(figsize=(11,4))
    for value,row in rows.items():
        series=values[profile[target].eq(value).to_numpy()].mean(axis=0) if mean else values[row]
        ax.plot(time,series,label=f"{target}={value}" + (" mean" if mean else f", row={row}"))
    ax.set(xlabel="seconds",ylabel=meta["unit"],title=f"{sensor} by {target} condition"); ax.legend(ncol=2); save_figure(fig,filename); plt.close(fig)
    del values; gc.collect()


def run_eda() -> dict[str, object]:
    """Produce Sprint 1 EDA figures/tables from raw data and the EDA-only cache."""
    set_plot_style(); profile=load_profile(); summary=compute_cycle_summary(); means=summary[[f"{s}_mean" for s in config.SENSORS]].copy(); means.columns=list(config.SENSORS)
    descriptive=means.describe().T; descriptive.to_csv(config.RESULTS_DIR / "descriptive_statistics.csv")
    groups={"pressure":[f"PS{i}" for i in range(1,7)],"flow_power":["EPS1","FS1","FS2"],"low_rate":["TS1","TS2","TS3","TS4","VS1","CE","CP","SE"]}
    for group,cols in groups.items():
        fig,axes=plt.subplots((len(cols)+2)//3,3,figsize=(13,3*((len(cols)+2)//3))); axes=np.ravel(axes)
        for ax,col in zip(axes,cols): sns.histplot(means[col],kde=True,ax=ax); ax.set_title(col)
        for ax in axes[len(cols):]: ax.set_visible(False)
        save_figure(fig,f"02_sensor_mean_distributions_{group}"); plt.close(fig)
    examples={target:_rows_for_target(profile,target) for target in config.TARGET_COLUMNS[:4]}
    pd.DataFrame(examples).to_csv(config.RESULTS_DIR / "example_cycle_rows.csv",index=False)
    for sensor,target,file in [("TS1","cooler","03_cooler_TS1_signals"),("CE","cooler","03_cooler_CE_signals"),("PS2","valve","04_valve_PS2_signals"),("EPS1","pump","05_pump_EPS1_signals"),("FS1","pump","05_pump_FS1_signals"),("PS1","accumulator","06_accumulator_PS1_signals")]: _signal_plot(sensor,target,examples[target],False,profile,file)
    for sensor,target,file in [("CE","cooler","07_mean_overlay_cooler_CE"),("PS2","valve","07_mean_overlay_valve_PS2"),("EPS1","pump","07_mean_overlay_pump_EPS1"),("PS1","accumulator","07_mean_overlay_accumulator_PS1")]: _signal_plot(sensor,target,examples[target],True,profile,file)
    corr=means.corr(); fig,ax=plt.subplots(figsize=(13,10)); sns.heatmap(corr,cmap="vlag",center=0,ax=ax); save_figure(fig,"08_sensor_mean_correlation_heatmap"); plt.close(fig)
    pairs=corr.where(~np.eye(len(corr),dtype=bool)).stack().rename("pearson_r").reset_index(); pairs.columns=["sensor_1","sensor_2","pearson_r"]; strong=pairs[(pairs.sensor_1<pairs.sensor_2)&(pairs.pearson_r.abs()>0.9)].sort_values("pearson_r",key=lambda s:s.abs(),ascending=False); strong.to_csv(config.RESULTS_DIR / "strong_correlations.csv",index=False)
    relevant={"cooler":["CE","CP","TS1"],"valve":["PS1","PS2","FS1"],"pump":["EPS1","FS1","FS2"],"accumulator":["PS1","PS2","PS4"]}
    groups_out=[]
    for target,cols in relevant.items():
        data=profile[[target]].join(means[cols]); group=data.groupby(target)[cols].mean(); group.to_csv(config.RESULTS_DIR/f"group_means_{target}.csv"); groups_out.append(group.assign(target=target).reset_index())
        fig,axes=plt.subplots(1,len(cols),figsize=(5*len(cols),4))
        for ax,col in zip(np.ravel(axes),cols): sns.boxplot(data=data,x=target,y=col,ax=ax)
        save_figure(fig,f"09_relationships_{target}"); plt.close(fig)
    pd.concat(groups_out,ignore_index=True,sort=False).to_csv(config.RESULTS_DIR / "target_group_means.csv",index=False)
    sp=means.join(profile[config.TARGET_COLUMNS[:4]]).corr(method="spearman").loc[means.columns,config.TARGET_COLUMNS[:4]]; long=sp.stack().rename("spearman_r").reset_index(); long.columns=["sensor","target","spearman_r"]; long["abs_r"]=long.spearman_r.abs(); long.sort_values("abs_r",ascending=False).to_csv(config.RESULTS_DIR / "sensor_target_spearman.csv",index=False)
    stable=profile[["stable"]].join(means[["CE","PS2","EPS1","TS1"]]).groupby("stable").agg(["count","mean","std"]); stable.to_csv(config.RESULTS_DIR / "stable_flag_comparison.csv")
    fig,axes=plt.subplots(1,4,figsize=(16,4)); data=profile[["stable"]].join(means[["CE","PS2","EPS1","TS1"]])
    for ax,col in zip(axes,["CE","PS2","EPS1","TS1"]): sns.boxplot(data=data,x="stable",y=col,ax=ax)
    save_figure(fig,"10_stable_flag_comparison"); plt.close(fig)
    out=count_outliers_iqr(summary[[c for c in summary if c.endswith("_mean") or (c.endswith("_max") and c.split("_")[0] in [*{f"PS{i}" for i in range(1,7)},"EPS1"])]]); out.to_csv(config.RESULTS_DIR / "outlier_summary_iqr.csv",index=False)
    return {"summary":summary,"descriptive":descriptive,"examples":examples,"strong":strong,"spearman":long,"stable":stable,"outliers":out}
