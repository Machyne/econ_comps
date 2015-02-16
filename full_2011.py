import os

import numpy as np
import pandas as pd
from pandas.tools.plotting import scatter_matrix
import pylab

from industry_to_days import get_census_mapper

"""
USAGE:
python full_2011.py

CREATES:
results/2011/clean.csv
results/2011/scatter_matrix.png
results/2011/summary.txt
"""

CLEAN_CSV = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'results', '2011', 'clean.csv'))

PSID_CSV = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'psid', '2011.csv'))

SCAT_MATRIX_PNG = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'results', '2011', 'scatter_matrix.png'))

SUMMARY_TXT = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'results', '2011', 'summary.txt'))


def _calc_vacation(row):
    took, days, weeks, months = (row['took_vac'], row['days_vac'],
                                 row['weeks_vac'], row['months_vac'])
    if took in [8, 9] or (days in [998, 999]) or (months in [98, 99]) or (
        weeks in [98, 99]):
        return np.nan
    elif took == 5:
        return 0
    else:
        return days + (7 * weeks) + (30 * months)


def _calc_salary(row):
    amt, unit = row['salary_amt'], row['salary_unit']
    if amt in [0.0, 9999998.0] or unit in [0, 7, 8, 9]:
        return np.nan
    if unit == 3:  # one week
        scalar = 52.0
    elif unit == 4:  # two weeks
        scalar = 26.0
    elif unit == 5:  # one month
        scalar = 12.0
    elif unit == 6:  # one year
        scalar = 1.0
    return scalar * amt


def clean(df):
    # make sex into dummy for is_female
    df['sex'] -= 1
    # remove unknown age values
    df.age = df.age.replace(999, np.nan)
    # figure out total vacation taken
    df['vacation'] = df.apply(_calc_vacation, axis=1)
    # fix salary to be annual amount
    df['salary'] = df.apply(_calc_salary, axis=1)
    # merge industry data
    df['paid_vacation'] = df.industry.map(get_census_mapper())
    # drop old values
    for col in ['took_vac', 'days_vac', 'weeks_vac', 'months_vac', 'industry',
                'salary_amt', 'salary_unit']:
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
