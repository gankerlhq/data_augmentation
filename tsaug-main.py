from datetime import datetime

import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import tsaug
from tsaug import TimeWarp, Crop, Quantize, Drift, Reverse
from tsaug.visualization import plot
import plotly.graph_objects as go


def parser(x):
	return datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ')

df = pd.read_csv('./data/gcp_cost_2022.csv', sep=',', header=0, parse_dates=[0],
                  date_parser=parser)


my_augmenter = (TimeWarp() * 5
                + Crop(size=300)
                + Quantize(n_levels=[10, 20, 30])
                + Drift(max_drift=(0.1, 0.5)) @ 0.8
                + Reverse() @ 0.5)

X = np.arange(len(df))
print(df)
print(df.__dict__)
# X = df['datetime']
# X = df['datetime'].tolist()
Y = df['costInUsd'].tolist()

plt.plot(X, Y)

plt.show()

Y = np.array(Y)
Y_aug_noise, X_aug_noise = tsaug.AddNoise(scale=0.1).augment(Y, X)
Y_aug_drift, X_aug_drift = tsaug.Drift(max_drift=0.5, n_drift_points=5).augment(Y, X)

def draw_plot_px2(title_plot, X_aug, Y_aug, label1, X_aug2, Y_aug2, label2):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X_aug, y=Y_aug,
                        mode='lines',
                        name=label1))
    fig.add_trace(go.Scatter(x=X_aug2, y=Y_aug2,
                        mode='lines',
                        name=label2))
    fig.add_trace(go.Scatter(x=X, y=Y,
                        mode='lines',
                        name='Origin data'))
    fig.update_layout(title=title_plot)
    fig.show()


draw_plot_px2('GCP_cost_March-Sept',X_aug_noise, Y_aug_noise, 'after_add_noise', X_aug_drift, Y_aug_drift, 'after_add_drift')
