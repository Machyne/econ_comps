import os

import numpy as np
import pandas as pd

from industry_to_days import get_census_mapper

CLEAN1984 = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '1984_clean.csv'))


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
    # write output to a file
    with open(CLEAN1984, 'w+') as csv:
        df.to_csv(path_or_buf=csv)


def do_stats(df):
    print df.describe()


def main():
    df = None
    if os.path.isfile(CLEAN1984):
        df = pd.io.parsers.read_csv(CLEAN1984)
    else:
        csv_file = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                'psid', '1984.csv'))
        with open(csv_file) as csv:
            df = pd.io.parsers.read_csv(csv)
        clean(df)
    do_stats(df)

if __name__ == '__main__':
    main()
