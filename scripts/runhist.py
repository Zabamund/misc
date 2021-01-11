import sys
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

from runlog import make_df_from_csv

def make_hist(df, start_plot, end_plot):
    """Make a histogram of runs"""
    try:
        _start_plot = start_plot.date()
    except AttributeError:
        _start_plot = start_plot
    try:
        _end_plot = end_plot.date()
    except AttributeError:
        _end_plot = end_plot

    dist_min, dist_max = np.floor(df.Distance.min()), np.ceil(df.Distance.max())

    _, ax = plt.subplots(figsize=(20, 10))
    bins = np.arange(dist_min-1, dist_max+1, 1)
    sns.histplot(data=df,
                ax=ax,     
                kde=True,          
                )
    plt.title(f"Rob's run distribution from {_start_plot} to {_end_plot}", fontsize=14)
    plt.xlabel('Distance [km]')
    sns.rugplot(data=df,
                ax=ax,
                )
    mean, median, perc25, perc75 = df.Distance.mean(), df.Distance.median(), df.Distance.describe().loc['25%'], df.Distance.describe().loc['75%']
    ax.axvline(mean, color='b', linestyle='-.', lw=1.5, label='mean')
    ax.axvline(median, color='g', linestyle='--', lw=1.5, label='median')
    ax.axvline(perc25, color='r', linestyle='-', lw=1.5, label='25 percentile')
    ax.axvline(perc75, color='k', linestyle=':', lw=1.5, label='75 percentile')
    ax.text(mean, 45, f' {mean:.1f}km')
    ax.text(median, 45, f' {median:.1f}km')
    ax.text(perc25, 45, f' {perc25:.1f}km')
    ax.text(perc75, 45, f' {perc75:.1f}km')
    plt.xticks(ticks=bins)
    plt.grid(c='k', alpha=0.2)
    ax.legend()
    plt.show() 
    return None


if __name__ == "__main__":
    df = make_df_from_csv(sys.argv[1])    
    start_plot, end_plot = df.index[0], df.index[-1]
    try:
        if sys.argv[2]:
            start_plot = sys.argv[2]
    except IndexError:
        pass
    try:
        if sys.argv[3]:
            end_plot = sys.argv[3]
    except IndexError:
        pass
    df = df[start_plot:end_plot]
    make_hist(df, start_plot, end_plot)