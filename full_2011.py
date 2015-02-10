import os

import numpy as np
import pandas as pd

from industry_to_days import get_census_mapper

CLEAN2011 = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '2011_clean.csv'))


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
    # figure out total vacation
    df['vacation'] = df.apply(_calc_vacation, axis=1)
    # fix salary to be annual amount
    df['salary'] = df.apply(_calc_salary, axis=1)
    # merge industry data
    df['paid_vacation'] = df.industry.map(get_census_mapper())
    # drop old values
    for col in ['took_vac', 'days_vac', 'weeks_vac', 'months_vac', 'industry',
                'salary_amt', 'salary_unit']:
        df.drop(col, axis=1, inplace=True)
    # write output to a file
    with open(CLEAN2011, 'w+') as csv:
        df.to_csv(path_or_buf=csv)


def do_stats(df):
    print df.describe()


def main():
    df = None
    if os.path.isfile(CLEAN2011):
        df = pd.io.parsers.read_csv(CLEAN2011)
    else:
        csv_file = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                'psid', '2011er.csv'))
        with open(csv_file) as csv:
            df = pd.io.parsers.read_csv(csv)
        clean(df)
    do_stats(df)

if __name__ == '__main__':
    main()
