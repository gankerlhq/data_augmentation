import math
from datetime import datetime, timedelta


import numpy as np
import pandas as pd

import tsaug
from tsaug import TimeWarp, Crop, Quantize, Drift, Reverse
from tsaug.visualization import plot

from utils import 


def add_noise(Y, X, scale=0.1):
    Y_aug_noise, X_aug_noise = tsaug.AddNoise(scale=scale).augment(Y, X)
    return Y_aug_noise, X_aug_noise


def augment_metrics(df_metrics, instanceId, historical_date, metricType='cpuUtilization'):
    df_metrics_i = df_metrics[df_metrics['instanceId'] == instanceId].copy()

    # days_range: number of days of real data
    start_date = df_metrics_i.min(axis=0)['datetime'].date()
    end_date = df_metrics_i.max(axis=0)['datetime'].date()
    days_range = end_date - start_date + timedelta(days=1)

    X = np.arange(len(df_metrics_i))
    X_date = df_metrics_i['datetime'].map(lambda x: int(x.timestamp() * 1000)).tolist()

    Y = df_metrics_i['avgValue'].tolist()
    Y = np.array(Y)
    Y_aug_noise, X_aug_noise = add_noise(Y, X)

    NUM_OF_PERIODS = calculate_number_of_augment_need(historical_date.date(), start_date, days_range)
    X_date = df_metrics_i['datetime'].map(lambda x: int(x.timestamp() * 1000)).tolist()
    X_date_extended1 = pd.date_range(start_date - (days_range) * NUM_OF_PERIODS, start_date, freq='d').map(
        lambda x: int(x.timestamp() * 1000))

    X_date_extended = np.hstack([X_date_extended1, X_date])[1:]

    extended_Y = []
    cur_Y = Y
    for i in range(0, NUM_OF_PERIODS):
        cur_Y, X = add_noise(cur_Y, X)
        extended_Y.append(cur_Y)
    Y_extended = np.hstack([Y] + extended_Y)
    new_df = pd.DataFrame(
        {'datetime': list(map(lambda x: datetime.fromtimestamp(x / 1000.0).strftime('%Y-%m-%d'), X_date_extended))})

    new_df[metricType] = pd.Series(Y_extended)
    new_df = new_df.sort_values('datetime')
    return new_df