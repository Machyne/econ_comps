import os

import numpy as np
import pandas as pd
from pandas.tools.plotting import scatter_matrix
import pylab
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms

from industry_to_days import get_census_mapper

"""
USAGE:
python full_2011.py

CREATES:
results/2011/clean.csv
results/2011/corr.txt
results/2011/het_breushpagan.txt
results/2011/ols1.txt
results/2011/ols2.txt
results/2011/scatter_matrix.png
results/2011/summary.txt
"""

COL_ORDER = ['vacation', 'paid_vacation', 'age', 'fam_size', 'is_female',
             'income10', 'salary', 'is_employed']

PSID_CSV = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'psid', '2011.csv'))


def get_f_path(fname):
    return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                'results', '2011', fname))


CLEAN_CSV = get_f_path('clean.csv')
CORR_TXT = get_f_path('corr.txt')
HET_BP_TXT = get_f_path('het_breushpagan.txt')
OLS1_TXT = get_f_path('ols1.txt')
OLS2_TXT = get_f_path('ols2.txt')
SCAT_MATRIX_PNG = get_f_path('scatter_matrix.png')
SUMMARY_TXT = get_f_path('summary.txt')

f_exists = (lambda file_: os.path.isfile(file_))


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
    df['is_female'] = df['sex'] - 1
    # remove unknown age values
    df.age = df.age.replace(999, np.nan)
    # figure out total vacation taken
    df['vacation'] = df.apply(_calc_vacation, axis=1)
    # fix salary to be annual amount
    df['salary'] = df.apply(_calc_salary, axis=1)
    # remove outliers
    df.ix[df.salary < 1e3] = np.nan
    df.ix[df.salary >= 400e3] = np.nan
    df.ix[df.income10 < 1e3] = np.nan
    df.ix[df.income10 >= 400e3] = np.nan
    # make employment into dummy for is_employed
    df['is_employed'] = df.employment
    # remove all those not working
    for i in range(2,10) + [99]:
        df.is_employed.replace(i, 0, inplace=True)
    # merge industry data
    df['paid_vacation'] = df.industry.map(get_census_mapper())
    # drop old values
    for col in ['took_vac', 'days_vac', 'weeks_vac', 'months_vac', 'industry',
                'salary_amt', 'salary_unit', 'sex', 'employment']:
        df.drop(col, axis=1, inplace=True)
    df = df.reindex_axis(sorted(df.columns, key=COL_ORDER.index), axis=1)
    return df


def do_stats(df):
    # Only view those that received vacation and are employed
    df.is_employed.replace(0.0, np.nan, inplace=True)
    df.paid_vacation.replace(0.0, np.nan, inplace=True)
    df.dropna(inplace=True)
    # No longer need this dummy
    df.drop('is_employed', axis=1, inplace=True)

    # Summary stats
    if not f_exists(SUMMARY_TXT):
        summary = df.describe().T
        summary = np.round(summary, decimals=3)
        with open(SUMMARY_TXT, 'w') as f:
            f.write(summary.to_string())

    # Test for autocorrelation: scatter matrix, correlation, run OLS
    if not f_exists(SCAT_MATRIX_PNG):
        scatter_matrix(df, alpha=0.2, figsize=(64, 64), diagonal='hist')
        pylab.savefig(SCAT_MATRIX_PNG, bbox_inches='tight')
    if not f_exists(CORR_TXT):
        corr = df.corr()
        corr = corr.reindex_axis(
            sorted(corr.columns, key=COL_ORDER.index), axis=0)
        corr = corr.reindex_axis(
            sorted(corr.columns, key=COL_ORDER.index), axis=1)
        for i, k in enumerate(corr):
            row = corr[k]
            for j in range(len(row)):
                if j > i:
                    row[j] = np.nan
        with open(CORR_TXT, 'w') as f:
            f.write(np.round(corr, decimals=3).to_string(na_rep=''))
    if not f_exists(OLS1_TXT):
        ols_results = smf.ols(
            formula='vacation ~ paid_vacation + np.square(paid_vacation) + '
                    'age + fam_size + is_female + income10 + salary + '
                    'np.square(salary)',
            data=df).fit()
        with open(OLS1_TXT, 'w') as f:
            f.write(str(ols_results.summary()))
            f.write('\n\nCondition Number: {}'.format(
                np.linalg.cond(ols_results.model.exog)))

    # Need to drop salary, too much autocorrelation
    df.drop('salary', axis=1, inplace=True)

    # Test for autocorrelation: scatter matrix, correlation, run OLS
    if not f_exists(HET_BP_TXT):
        ols_results = smf.ols(
            formula='vacation ~ paid_vacation + np.square(paid_vacation) + '
                    'age + fam_size + is_female + income10',
            data=df).fit()
        names = ['LM', 'LM P val.', 'F Stat.', 'F Stat. P val.']
        test = sms.het_breushpagan(ols_results.resid, ols_results.model.exog)
        f_p = test[3]
        with open(HET_BP_TXT, 'w') as f:
            str_ =  '\n'.join('{}: {}'.format(n, v)
                              for n, v in zip(names, test))
            f.write(str_ + '\n\n')
            if f_p < .01:
                f.write('No Heteroskedasticity found.\n')
            else:
                f.write('Warning: Heteroskedasticity found!\n')

    # no Heteroskedasticity found
    # final OLS results with robust standard errors
    if not f_exists(OLS2_TXT):
        ols_results = smf.ols(
            formula='vacation ~ paid_vacation + np.square(paid_vacation) + '
                    'age + fam_size + is_female + income10',
            data=df).fit().get_robustcov_results(cov_type='HAC', maxlags=1)
        with open(OLS2_TXT, 'w') as f:
            f.write(str(ols_results.summary()))
            f.write('\n\nCondition Number: {}'.format(
                np.linalg.cond(ols_results.model.exog)))
    return df


def main():
    df = None
    if f_exists(CLEAN_CSV):
        df = pd.io.parsers.read_csv(CLEAN_CSV)
        df.drop('Unnamed: 0', axis=1, inplace=True)
    else:
        with open(PSID_CSV) as csv:
            df = pd.io.parsers.read_csv(csv)
        df = clean(df)
        # write output to a file
        with open(CLEAN_CSV, 'w+') as csv:
            df.to_csv(path_or_buf=csv)
    return do_stats(df)


if __name__ == '__main__':
    main()
    print '2011 succeeds! :)'
