import pandas as pd
from tsaug import TimeWarp, Crop, Quantize, Drift, Reverse


df = pd.read_csv('./data/gcp_cost_2022.csv', sep=',', header=0)

my_augmenter = (\
TimeWarp() * 5 \  # random time warping 5 times in parallel
+ Crop(size=300) \ # random crop subsequences with length 300
+ Quantize(n_levels=[10, 20, 30]) \ # random quantize to 10-, 20-, or 30- level sets
+ Drift(max_drift=(0.1, 0.5)) @ 0.8 \ # with 80% probability, random drift the signal up to 10% - 50%
+ Reverse() @ 0.5  \# with 50% probability, reverse the sequence
)