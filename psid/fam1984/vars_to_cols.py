import os
import re

from collections import OrderedDict


def vars_to_cols(fname):
    header_do_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            fname))
    with open(header_do_file) as f:
        line = ''
        while line.strip() != 'infix':
            line = f.readline()
        vars_ = OrderedDict()
        line = f.readline()
        while re.match(r'^ +V', line):
            matches = re.findall(r'V\d+ + \d+ - \d+', line)
            splits = map(lambda x: re.split(r'  +', x), matches)
            for var, range_ in splits:
                range_ = map(int, range_.split(' - '))
                vars_[var] = range_
            line = f.readline()
        return vars_

if __name__ == '__main__':
    vars_ = vars_to_cols('FAM1984.do')
    for k in vars_:
        print k, ' '.join(map(str, vars_[k]))