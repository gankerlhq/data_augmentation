import os
import io
from datetime import datetime

import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from matplotlib import pyplot as plt

plt.interactive(False)


def parser(x):
	return datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ')

df = pd.read_csv('./data/gcp_cost_2022.csv', sep=',', header=0, parse_dates=[0], index_col=0,
                  squeeze=True, date_parser=parser)

print('--ORIGINIAL')
print(df)
plt.plot(df)
plt.show()

print('--UPSAMPLED')
upsampled = df.resample('D')
print(upsampled)

print('--INTERPOLATED')
interpolated = upsampled.interpolate(method='spline', order=1)
print(interpolated.head(32))
plt.plot(interpolated)
plt.show()


print('--DECOMPOSED')
decompose = seasonal_decompose(interpolated, period=24)
decompose.plot().show()
