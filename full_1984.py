import os

import numpy as np
import pandas as pd
from pandas.tools.plotting import scatter_matrix
import pylab
import statsmodels.formula.api as smf
import statsmodels.stats.api as sms

"""
USAGE:
python full_1984.py

CREATES:
results/1984/clean.csv
results/1984/scatter_matrix.png
results/1984/summary.txt
"""

PSID_CSV = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'psid', '1984.csv'))


def get_f_path(fname):
    return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                'results', '1984', fname))


CLEAN_CSV = get_f_path('clean.csv')
CORR_TXT = get_f_path('corr.txt')
HET_WHITE_TXT = get_f_path('het_white.txt')
OLS1_TXT = get_f_path('ols1.txt')
OLS2_TXT = get_f_path('ols2.txt')
SCAT_MATRIX1_PNG = get_f_path('scatter_matrix1.png')
SCAT_MATRIX2_PNG = get_f_path('scatter_matrix2.png')
SUMMARY_TXT = get_f_path('summary.txt')

f_exists = (lambda file_: os.path.isfile(file_))


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
    df['is_female'] = df['sex'] - 1
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
    for col in ['sex', 'took_vac', 'weeks_vac', 'given_vac', 'hrs_paid_vac']:
        df.drop(col, axis=1, inplace=True)


def do_stats(df):
    # Summary stats
    if not f_exists(SUMMARY_TXT):
        with open(SUMMARY_TXT, 'w') as f:
            f.write(df.describe().to_string())

    # Test for autocorrelation: scatter matrix, correlation, run OLS
    if not f_exists(SCAT_MATRIX1_PNG):
        scatter_matrix(df, alpha=0.2, figsize=(64, 64), diagonal='hist')
        pylab.savefig(SCAT_MATRIX1_PNG, bbox_inches='tight')
    if not f_exists(CORR_TXT):
        corr = df.corr()
        for i, k in enumerate(corr):
            row = corr[k]
            for j in range(len(row)):
                if j > i:
                    row[j] = np.nan
        with open(CORR_TXT, 'w') as f:
            f.write(corr.to_string(na_rep=''))
    if not f_exists(OLS1_TXT):
        ols_results = smf.ols(
            formula='vacation ~ paid_vacation + np.square(paid_vacation) + '
                    'age + fam_size + income83 + is_female + salary + '
                    'np.square(salary)',
            data=df).fit()
        with open(OLS1_TXT, 'w') as f:
            f.write(str(ols_results.summary()))
            f.write('\n\nCondition Number: {}'.format(
                np.linalg.cond(ols_results.model.exog)))

    # Need to drop salary, too much autocorrelation
    df.drop('salary', axis=1, inplace=True)

    if not f_exists(HET_WHITE_TXT):
        ols_results = smf.ols(
            formula='vacation ~ paid_vacation + np.square(paid_vacation) + '
                    'age + fam_size + income83 + is_female',
            data=df).fit()
        names = ['LM', 'LM P val.', 'F Stat.', 'F Stat. P val.']
        test = sms.het_white(ols_results.resid, ols_results.model.exog)
        f_p = test[3]
        with open(HET_WHITE_TXT, 'w') as f:
            str_ =  '\n'.join('{}: {}'.format(n, v)
                              for n, v in zip(names, test))
            f.write(str_ + '\n\n')
            if f_p < .01:
                f.write('No Heteroskedasticity found.\n')
            else:
                f.write('Warning: Heteroskedasticity found!\n')

    # no Heteroskedasticity found
    # make a new scatter matrix to use for the paper
    if not f_exists(SCAT_MATRIX2_PNG):
        scatter_matrix(df, alpha=0.2, figsize=(64, 64), diagonal='hist')
        pylab.savefig(SCAT_MATRIX2_PNG, bbox_inches='tight')

    # final OLS results
    if not f_exists(OLS2_TXT):
        ols_results = smf.ols(
            formula='vacation ~ paid_vacation + np.square(paid_vacation) + '
                    'age + fam_size + income83 + is_female',
            data=df).fit()
        with open(OLS2_TXT, 'w') as f:
            f.write(str(ols_results.summary()))
            f.write('\n\nCondition Number: {}'.format(
                np.linalg.cond(ols_results.model.exog)))


def main():
    df = None
    if f_exists(CLEAN_CSV):
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
    print 'Success! :)'
