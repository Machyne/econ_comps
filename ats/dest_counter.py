import os
import re

"""
USAGE:
python dest_counter.py

NOTES:
data downloaded from
http://www.transtats.bts.gov/tables.asp?db_id=505&DB_Name=
"""

LAST_STATE = 56  # the code for Wyoming. Everything else is outside the US.

def get_counts():
    domestic = 0
    international = 0
    csv_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'state_codes.csv'))
    with open(csv_file) as f:
        f.readline()  # read off headers
        for line in f:
            nums = re.findall(r'"(\d+)",', line)
            if len(nums):
                nums = map(int, nums)
                for num in nums:
                    if num > LAST_STATE:
                        international += 1
                    else:
                        domestic += 1
    return domestic, international

if __name__ == '__main__':
    domestic, international = get_counts()
    print 'Total vacations take by US citizens'
    print 'domestic:', domestic, 'international', international
    print '{} more trips domestic trips.'.format(domestic - international)
    pct = float(domestic) / (domestic + international)
    print '%0.2f%% of trips were domestic.' % (pct * 100)
