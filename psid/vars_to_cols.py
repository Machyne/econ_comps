import os
import re
from collections import OrderedDict

"""
USAGE:
python vars_to_cols.py > vars_columns.txt
"""

def vars_to_cols(fname, folder='.'):
    header_do_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            folder, fname))
    with open(header_do_file) as f:
        line = ''
        while line.strip() != 'infix':
            line = f.readline()
        vars_ = OrderedDict()
        line = f.readline()
        while re.match(r'^ +[VE]', line):
            matches = re.findall(r'[VE][0-9A-Z]+ +\d+ - \d+', line)
            splits = map(lambda x: re.split(r'  +', x), matches)
            for var, range_ in splits:
                range_ = map(int, range_.split(' - '))
                vars_[var] = range_
            line = f.readline()
        return vars_

if __name__ == '__main__':
    vars_ = vars_to_cols('FAM1984.do', 'fam1984')
    for k in vars_:
        print k, ' '.join(map(str, vars_[k]))