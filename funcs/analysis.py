import numpy as np
import pandas as pd

def months_stats(daily):
    """
    Compute monthly statistics for weight data

    Parameters
    ----------
    daily : pandas.DataFrame
        DataFrame containing daily weight measurements.

    Returns
    -------
    monthly : pandas.DataFrame
        DataFrame containing monthly statistics: 
            mean weight, standard deviation, and center time.
    """

    # Compute monthly statistics
    daily["Month"] = daily["Time"].dt.to_period("M")
    monthly = daily.groupby("Month").agg(
        mean_weight=("Weight_lbs", "mean"),                  # Mean
        std_weight=("Weight_lbs", "std"),                    # Standard deviation
        center_time=("Time", lambda x: x.mean())             # Center time of the month
    ).reset_index()

    return monthly