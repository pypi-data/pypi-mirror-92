from matplotlib import pyplot as plt

from ds_methods.common.df import DataFrameUtils

from ds_methods.methods.pipeline import Pipeline
from ds_methods.methods.preprocessing import *
from ds_methods.methods.groups import *
from ds_methods.methods.preprocessing import Resampling

from ds_methods.methods.custom import TimeWarpingOnRegression

from ds_methods.templates.init_data import load_raw_data


data = load_raw_data()

tw = Pipeline([
    Group({
        'keys': ['target'],
    }),
    # MovingAverage({
    #     'window': 60,
    # }),
    Diff({'periods': 1}),
    TimeWarpingOnRegression({}),
]).run(data)['data']

print(tw)

columns = ['area', 'size', 'temperature']
for name, group in tw.groupby('target'):
    numeric_part, other_part = DataFrameUtils.decompose(group)

    day_groups = Group({'time': 24}).make(group)['data']

    dates = []
    for day, day_group in day_groups:
        if not day_group.empty:
            dates.append([day_group.index[0], day.date()])

    for column in columns:
        _, ax = plt.subplots(figsize=(14, 12))
        legends = []

        group.plot(y=column, ax=ax, linewidth=0.75, alpha=0.75)
        group.plot(y=f'{column}_regression', ax=ax, linewidth=1, alpha=0.8)
        group.plot(y=f'{column}_tw_distance', ax=ax, linewidth=3, alpha=0.85)

        legends += [
            f'Mouse: {name}, Feature: {column}',
            f'Mouse: {name}, Feature: {column}_regression',
            f'Mouse: {name}, Feature: {column}_tw_distance',
        ]

        plt.title(f'Time-Warping Distance\nMouse - {name}, Feature - {column}')
        plt.xticks(
            *zip(*dates),
            rotation=30,
        )
        plt.ylabel(column)
        plt.xlabel('date')
        plt.legend(legends)

        plt.savefig(f'plots/{name}_{column}.png')

        # plt.show()
