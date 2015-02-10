import os
import re

from vars_to_cols import vars_to_cols

"""
USAGE:
python vars_to_csv.py

CREATES:
age_sex.csv
"""

def vars_to_csv(vars_, in_folder, outfile):
    dict_ = vars_to_cols(in_folder.upper() + '.do', in_folder)
    vars_, names = [[x[i] for x in vars_] for i in (0, 1)]
    indicies = map(dict_.get, vars_)
    data_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            in_folder, in_folder.upper() + '.txt'))
    with open(data_file) as f:
        outfile.write(','.join(names) + '\n')
        for line in f:
            to_write = ''
            for start, end in indicies:
                to_write += line[start - 1 : end].strip() + ','
            outfile.write(to_write[:-1] + '\n')

if __name__ == '__main__':
    with open('age_sex.csv', 'w+') as f:
        vars_to_csv([('V10420', 'sex'), ('V10419', 'age')], 'fam1984', f)
