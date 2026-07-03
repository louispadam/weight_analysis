import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def days_plot(ax, daily):
    """
    Plot daily measurements together with monthly statistics

    Parameters
    ----------
    monthly : pandas.DataFrame
        DataFrame containing monthly weight statistics.

    Returns
    -------
    ax
    """

    # Plot daily (raw) data
    ax.scatter(
        daily["Time"],
        daily["Weight_lbs"],
        color="blue",
        alpha=0.3,
        label="Daily"
    )

    return ax

def months_plot(ax, monthly):
    """
    Plot daily measurements together with monthly statistics

    Parameters
    ----------
    monthly : pandas.DataFrame
        DataFrame containing monthly weight statistics.

    Returns
    -------
    ax
    """

    # Organize data
    #daily["Time"] = pd.to_datetime(daily["Time"])            # Convert 'Time' column to datetime

    # Set thresholds for omitting data or filling in 'blanks'
    monthly["time_gap"] = monthly["center_time"].diff().dt.days
    low_gap_threshold = 14
    high_gap_threshold = 42

    # Omit months with large gaps
    monthly.loc[monthly["time_gap"] < low_gap_threshold, "mean_weight"] = np.nan

    # Substitute-in missing months
    monthly = monthly.set_index("Month")
    all_months = pd.period_range(                           # First compute full range of months
        start=monthly.index.min(),
        end=monthly.index.max(),
        freq="M"
    )                                                       # Then fill in rows to compensate
    monthly = monthly.reindex(all_months)
    monthly = monthly.reset_index().rename(columns={"index": "Month"})

    # Set center_time for missing months to the middle of the month (otherwise ax.errobar crashes)
    mask = monthly["center_time"].isna()
    monthly.loc[mask, "center_time"] = (
        monthly.loc[mask, "Month"].dt.to_timestamp()
        + pd.to_timedelta(
            monthly.loc[mask, "Month"].dt.days_in_month // 2,
            unit="D"
        )
    )

    # Plot aggregated monthly data
    ax.errorbar(
        monthly["center_time"],
        monthly["mean_weight"],
        yerr=monthly["std_weight"],
        fmt="-o",
        color="darkorange",
        ecolor="black",
        elinewidth=1,
        capsize=3,
        linewidth=2,
        label="Monthly"
    )

    return ax