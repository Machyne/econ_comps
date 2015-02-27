from scipy.stats import ttest_rel
import numpy as np
import pandas as pd

from full_1984 import main as main1984
from full_2011 import main as main2011

COL_ORDER = ['vacation', 'paid_vacation', 'age', 'fam_size', 'is_female',
             'income83']


if __name__ == '__main__':
    df1984 = main1984()
    df2011 = main2011()
    dif = df1984.shape[0] - df2011.shape[0]
    if dif > 0:
        df1984 = df1984.drop(df1984.index[-dif:])
    elif dif < 0:
        df2011 = df2011.drop(df2011.index[dif:])
    names = ['t-statistic', 'two-tailed p-value']
    for col in sorted(df1984.columns, key=COL_ORDER.index):
        colb = col if col != 'income83' else 'income10'
        t = ttest_rel(df1984[col], df2011[colb])
        t = [np.round(i, decimals=3) for i in t]
        print col
        print '\n'.join('{}: {}'.format(n, v) for n, v in zip(names, t))
