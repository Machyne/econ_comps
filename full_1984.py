import os

import numpy as np
import pandas as pd
from pandas.tools.plotting import scatter_matrix
import pylab

"""
USAGE:
python full_1984.py

CREATES:
results/1984/clean.csv
results/1984/scatter_matrix.png
results/1984/summary.txt
"""

CLEAN_CSV = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'results', '1984', 'clean.csv'))

PSID_CSV = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'psid', '1984.csv'))

SCAT_MATRIX_PNG = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'results', '1984', 'scatter_matrix.png'))

SUMMARY_TXT = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'results', '1984', 'summary.txt'))

def _calc_vacation(key1, key2, bad, scale):
    def fn(row):
        took, amount = row[key1], row[key2]
        if took in [0, 8, 9] or amount == bad:
            return np.nan
        elif took == 5:
            return 0
        else:
            return scale * amount
    return fn

def clean(df):
    # make sex into dummy for is_female
    df['sex'] -= 1
    # figure out total vacation taken
    df['vacation'] = df.apply(
        _calc_vacation('took_vac', 'weeks_vac', 99, 7), axis=1)
    # fix salary to be annual amount
    df.salary = df.salary.replace(0.00, np.nan)
    df.salary = df.salary.replace(99.99, np.nan)
    df.salary *= 2000
    # remove unknown age values
    df.age = df.age.replace(99, np.nan)
    # compute vacation given
    df['paid_vacation'] = df.apply(
        _calc_vacation('given_vac', 'hrs_paid_vac', 9999, 1. / 40.), axis=1)
    # drop old values
    for col in ['took_vac', 'weeks_vac', 'given_vac', 'hrs_paid_vac']:
        df.drop(col, axis=1, inplace=True)


def do_stats(df):
    # Summary stats
    if not os.path.isfile(SUMMARY_TXT):
        with open(SUMMARY_TXT, 'w') as f:
            f.write(repr(df.describe()))
    # Scatter matrix
    if not os.path.isfile(SCAT_MATRIX_PNG):
        scatter_matrix(df, alpha=0.2, figsize=(64, 64), diagonal='hist')
        pylab.savefig(SCAT_MATRIX_PNG, bbox_inches='tight')



def main():
    df = None
    if os.path.isfile(CLEAN_CSV):
        df = pd.io.parsers.read_csv(CLEAN_CSV)
        df.drop('Unnamed: 0', axis=1, inplace=True)
    else:
        with open(PSID_CSV) as csv:
            df = pd.io.parsers.read_csv(csv)
        clean(df)
        # write output to a file
        with open(CLEAN_CSV, 'w+') as csv:
            df.to_csv(path_or_buf=csv)
    do_stats(df)

if __name__ == '__main__':
    main()
