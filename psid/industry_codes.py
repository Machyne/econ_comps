import os
import re
import StringIO
output = StringIO.StringIO()

from vars_to_csv import vars_to_csv

"""
USAGE:
python industry_codes.py > psid_inds.txt
"""

_industries = {999: 'DK; NA; refused'}


def load_industries():
    csv_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'industries.csv'))
    with open(csv_file) as f:
        # read away titles
        line = f.readline()
        for line in f:
            parts = re.search(r'^"?([^"]+)"?,(\d+)\s*$', line)
            if parts is not None:
                _industries[int(parts.group(2))] = parts.group(1)

load_industries()


def get_industry(code):
    return _industries.get(code, 'UNK: {}'.format(code))

if __name__ == '__main__':
    output = StringIO.StringIO()
    vars_to_csv([('ER47480', 'industry_code')], 'fam2011er', output)
    vals = output.getvalue()
    output.close()

    vals = vals.split('\n')[1:]  # ignore header
    vals = set(map(int, filter(len, vals)))  # unique ints only
    vals.remove(0)  # 0 = does not apply
    for x in vals:
        print get_industry(x)
