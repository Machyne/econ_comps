import os
import re

import numpy as np
import pymongo

CROSSWALK = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'naics_census_crosswalk.csv'))

# note: "unspecific" means that the entire category is broken down into smaller
#       subcategories. These unspecific categories will be ignored.
ncs_lookup = {
    'Utilities': ('22',),
    'Construction': ('23',),
    'Manufacturing': ('3',),
    'Trade, transportation, and utilities': ('40', '41', '43', '46', '47'),
    'Retail trade': ('44', '45'),
    'Wholesale trade': ('42',),
    'Transportation and warehousing': ('48', '49'),
    'Information': ('51',),
    'Finance and insurance': ('52X',),  # unspecific
    'Financial activities': ('521', '523', '525'),
    'Credit intermediation and related activities': ('522',),
    'Insurance carriers and related activities': ('524',),
    'Real estate and rental and leasing': ('53',),
    'Professional and technical services':
        ('5413', '5415', '5416', '5417', '54190'),
    'Professional and business services':
        ('5411', '5412', '5414', '5418', '54194'),
    'Administrative and waste services': ('56',),
    'Education and health services': ('6X',),  # unspecific
    'Educational services': ('6114', '6115', '6116', '6117') ,
    'Elementary and secondary schools': ('6111',),
    'Junior colleges, colleges, and universities': ('612', '6113'),
    'Health care and social assistance': ('621', '623', '624'),
    'Hospitals': ('622',),
    'Leisure and hospitality': ('71',),
    'Accommodation and food services': ('72',),
    'Other services': ('81',),
    'Public administration': ('92',),
    'Goods-producing industries': ('11', '21'),
    'Service-providing industries': ('55',),
}


def get_ind_days():
    db = pymongo.MongoClient().ncs
    ind_days = {}  # industry: days
    provision_prefix = "Mean # of paid "
    for ind in db.ebs.distinct('industry'):
        pipeline = [
            {'$match': {'industry': ind}},
            {'$group': {
                    '_id': '$provision',
                    'val': {'$sum': '$value'},
                    'count': {'$sum': 1},
                }
            }
        ]
        results = db.ebs.aggregate(pipeline)['result']
        count = results[0]['count']
        results = [(provision['_id'][len(provision_prefix):],
                    provision['val']) for provision in results]
        vacation = [x[1] for x in results if x[0].startswith('vacation')]
        vacation = sum(map(float, vacation)) / len(vacation)
        ind_days[ind] = vacation / count
        # holidays = [x[1] for x in results if x[0].startswith('holidays')]
        # holidays = sum(map(float, holidays)) / len(holidays)
        # ind_days[ind] = (vacation + holidays) / count
    return ind_days


def naics_to_days(ind_days, naics):
    for ind, starts in ncs_lookup.items():
        if any(n.startswith(s) for n in naics for s in starts):
            return ind_days[ind]
    return np.nan


def get_census_days():
    census_days = {}
    ind_days = get_ind_days()
    with open(CROSSWALK) as csv:
        csv.readline()  # read off headers
        for line in csv:
            census, _, naics = line.strip().partition(',')
            census = int(census)
            naics = naics.strip().replace('"', '')
            naics = tuple(map(lambda x: x + '0', re.split(r',\s*', naics)))
            days = naics_to_days(ind_days, naics)
            census_days[census] = days
    return census_days


def get_census_mapper():
    cd = get_census_days()
    def mapper(census):
        return cd.get(census, np.nan)
    return mapper

if __name__ == '__main__':
    i_d = get_ind_days()
    print 'INDUSTRY: DAYS'
    print '\n'.join('{}: {}'.format(i, d) for i, d in i_d.items())
    cd = get_census_days()
    print '\n'
    print 'Total industries in the census:', len(cd)
    sum_ = sum(x for x in map(cd.get, cd) if x is not np.nan)
    print 'Average vacation:', sum_ / len(cd)
