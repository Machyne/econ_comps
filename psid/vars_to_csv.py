import os
import re

from vars_to_cols import vars_to_cols

def vars_to_csv(vars_, in_folder, outfile):
    dict_ = vars_to_cols(in_folder.upper() + '.do', in_folder)
    vars_.sort(key=dict_.keys().index)
    indicies = map(dict_.get, vars_)
    data_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            in_folder, in_folder.upper() + '.txt'))
    with open(data_file) as f:
        outfile.write(','.join(vars_) + '\n')
        for line in f:
            to_write = ''
            for start, end in indicies:
                to_write += line[start - 1 : end].strip() + ','
            outfile.write(to_write[:-1] + '\n')


if __name__ == '__main__':
    with open('age_sex.csv', 'w+') as f:
        vars_to_csv(['V10420', 'V10419'], 'fam1984', f)
