# http://www.bls.gov/help/hlpforma.htm#NB
# Series ID    NBU10000000000000028007
# Positions       Value           Field Name
# 1-2             NB              Prefix
# 3               U               Seasonal Adjustment Code 
# 4               1               Ownership Code
# 5-6             00              Estimate Code
# 7-11            00000           Industry Code
# 12-16           00000           Occupation Code
# 17-18           00              Subcell Code
# 19-20           28              Datatype Code
# 21-23           007             Provision Code

PREFIX = 'NB'

SEASON_ADJUST = {'adjusted': 'S', 'unadjusted': 'U'}

# http://download.bls.gov/pub/time.series/nb/nb.ownership
# code          text
#  1     Civilian workers
#  2     Private industry workers
#  3     State and local government workers
#  4     State government workers
#  5     Local government workers
OWNERSHIP = {
    'civilian': '1',
    'private': '2',
    'both gov': '3',
    'state gov': '4',
    'local gov': '5',
}

# http://download.bls.gov/pub/time.series/nb/nb.estimate
# code          text
#  00   Benefit combinations
#  05   Paid vacations
#  06   Paid holidays
#  07   Paid sick leave
#  12   Nonproduction bonuses
#  14   Life Insurance
#  15   Health/Medical care benefits
#  16   Short-term disability
#  17   Long-term disability
#  19   Defined benefit
#  20   Defined contribution
#  51   Payroll deduction IRA
#  52   Unmarried domestic partner: Health care benefits, same sex
#  53   Unmarried domestic partner: Health care benefits, opposite sex
#  54   Unmarried domestic partner: Defined benefit retirement survivor benefits, same sex
#  55   Unmarried domestic partner: Defined benefit retirement survivor benefits, opposite sex
#  56   Child care
#  57   Health-related benefits: Retiree health care benefits, Under age 65
#  58   Health-related benefits: Retiree health care benefits, Age 65 and over
#  59   Financial benefits: Financial planning
#  63   Wellness programs
#  64   Employee assistance program
#  66   Subsidized commuting
#  71   Long-term care insurance
#  73   Flexible work site
#  76   Savings plans with no employer contribution
#  77   Flexible benefits
#  78   Health care reimbursement account
#  79   Dependent care reimbursement account
#  80   Stock option - other
#  81   Stock option - performance
#  82   Stock option - signing
#  83   Paid Funeral leave
#  84   Paid Jury Duty
#  85   Paid Military Leave
#  86   Paid Personal Leave
#  87   Paid Family Leave
#  88   Unpaid Family Leave
#  89   Health Savings Account
#  90   All retirement benefits
#  94   All health care benefits
#  95   Stock Access
ESTIMATE = {
    'benefit combinations': '00',
    'paid vacations': '05',
    'paid holidays': '06',
    'paid sick leave': '07',
    'all retirement benefits': '90',
    'all health care benefits': '94',
    'paid funeral leave': '83',
    'paid jury duty': '84',
    'paid military leave': '85',
    'paid personal leave': '86',
    'paid family leave': '87',
    'unpaid family leave': '88',
}

# http://download.bls.gov/pub/time.series/nb/nb.industry
#  code         text
# 000000  All workers
# 220000  Utilities
# 230000  Construction
# 300000  Manufacturing
# 400000  Trade, transportation, and utilities
# 412000  Retail trade
# 420000  Wholesale trade
# 430000  Transportation and warehousing
# 510000  Information
# 520000  Finance and insurance
# 520A00  Financial activities
# 522000  Credit intermediation and related activities
# 524000  Insurance carriers and related activities
# 530000  Real estate and rental and leasing
# 540000  Professional and technical services
# 540A00  Professional and business services
# 560000  Administrative and waste services
# 600000  Education and health services
# 610000  Educational services
# 611100  Elementary and secondary schools
# 612000  Junior colleges, colleges, and universities
# 620000  Health care and social assistance
# 622000  Hospitals
# 700000  Leisure and hospitality
# 720000  Accommodation and food services
# 810000  Other services
# 920000  Public administration
# G00000  Goods-producing industries
# S00000  Service-providing industries
INDUSTRY = {
   'all': '00000',
   'utils': '22000',
   'construction': '23000',
   'manufacturing': '30000',
   'trade transport utils': '40000',
   'retail trade': '41200',
   'wholesale trade': '42000',
   'transportation and warehousing': '43000',
   'information': '51000',
   'finance and insurance': '52000',
   'financial activities': '52000',
   'credit intermediation': '52200',
   'insurance carriers': '52400',
   'real estate, rental, leasing': '53000',
   'technical services': '54000',
   'business services': '54000',
   'administrative and waste services': '56000',
   'education and health services': '60000',
   'educational services': '61000',
   'elementary and secondary schools': '61100',
   'colleges and universities': '61200',
   'health care and social assistance': '62000',
   'hospitals': '62200',
   'leisure and hospitality': '70000',
   'accommodation and food services': '72000',
   'other services': '81000',
   'public administration': '92000',
   'goods-producing industries': 'g0000',
   'service-providing industries': 's0000',
}

# http://download.bls.gov/pub/time.series/nb/nb.occupation
#  code         text
# 000000  All workers
# 111300  Management, business, and financial
# 112900  Management, professional and related
# 152900  Professional and related
# 250001  Teachers
# 252000  Primary, secondary, and special education school teachers
# 291111  Registered nurses
# 313900  Service
# 330000  Protective service occupations
# 410000  Sales and related occupations
# 414300  Sales and office
# 430000  Office and administrative support occupations
# 454700  Construction, extraction, farming, fishing, and forestry
# 454900  Natural resources, construction, and maintenance
# 490000  Installation, maintenance, and repair occupations
# 510000  Production occupations
# 515300  Production, transportation, and material moving
# 530000  Transportation and material moving occupations
OCCUPATION = {
    'all': '00000',
    # 'management business and financial': '111300',
    # 'management professional and related': '112900',
    # 'professional and related': '152900',
    # 'teachers': '250001',
    # 'school teachers': '252000',
    # 'registered nurses': '291111',
    # 'service': '313900',
    # 'protective service': '330000',
    # 'sales and related': '410000',
    # 'sales and office': '414300',
    # 'office and administrative support': '430000',
    # 'construction extraction farming fishing and forestry': '454700',
    # 'natural resources construction and maintenance': '454900',
    # 'installation maintenance and repair': '490000',
    # 'production': '510000',
    # 'production transportation and material moving': '515300',
    # 'transportation and material moving': '530000',
}

# http://download.bls.gov/pub/time.series/nb/nb.subcell
# code          text
#  00  All workers
#  01  1 to 99 workers
#  02  1 to 49 workers
#  04  50-99 workers
#  05  100 workers or more
#  06  100-499 workers
#  07  500 workers or more
#  08  Northeast
#  09  New England
#  10  Middle Atlantic
#  11  South
#  12  South Atlantic
#  13  East South Central
#  14  West South Central
#  15  Midwest
#  16  East North Central
#  17  West North Central
#  18  West
#  19  Mountain
#  20  Pacific
#  23  Union
#  24  Nonunion
#  25  Full time
#  26  Part time
#  34  AHR < Civilian 10th wage percentile
#  36  Civilian 25th wage percentile <= AHR < 50th
#  37  Civilian 50th wage percentile <= AHR < 75th
#  39  AHR >= Civilian 90th wage percentile
#  40  AHR < Private 10th wage percentile
#  42  Private 25th wage percentile <= AHR < 50th
#  43  Private 50th wage percentile <= AHR < 75th
#  45  AHR >= Private 90th wage percentile
#  46  AHR < Government 10th wage percentile
#  48  Government 25th wage percentile <= AHR < 50th
#  49  Government 50th wage percentile <= AHR < 75th
#  51  AHR >= Government 90th wage percentile
#  54  AHR < Civilian 25th wage percentile
#  55  AHR >= Civilian 75th wage percentile
#  56  AHR < Private 25th wage percentile
#  57  AHR >= Private 75th wage percentile
#  58  AHR < Government 25th wage percentile
#  59  AHR >= Government 75th wage percentile
#  AA  Establishment Size
#  AB  Region and Division
#  AC  Metropolitan Statistical Areas
#  AD  Bargaining Status
#  AE  Full-time and Part-time Work Status
#  AF  Time and Incentive Status
#  AG  Average Wage
#  AH  Civilian Wage Percentiles
#  AI  Private Wage Percentiles
#  AJ  Government Wage Percentiles
#  AK  Plan Sponsor
SUBCELL = {
    'all': '00',
    '1-99 w': '01',
    '1-49 w': '02',
    '50-99 w': '04',
    '100+ w': '05',
    '100-499 w': '06',
    '500+ w': '07',
    'northeast': '08',
    'new england': '09',
    'middle atlantic': '10',
    'south': '11',
    'south atlantic': '12',
    'east south central': '13',
    'west south central': '14',
    'midwest': '15',
    'east north central': '16',
    'west north central': '17',
    'west': '18',
    'mountain': '19',
    'pacific': '20',
    'union': '23',
    'nonunion': '24',
    'full time': '25',
    'part time': '26',
}

# http://download.bls.gov/pub/time.series/nb/nb.datatype
# code          text
#  20  Percent participation (duplicated totals
#  21  10th percentile
#  22  25th percentile
#  23  Median
#  24  75th percentile
#  25  90th percentile
#  26  Percent participation across all workers
#  27  Establishments offering benefit
#  28  Access to benefit - occupation-level
#  29  Access to benefit - plan-level
#  30  Mean
#  31  Share of premiums
#  32  Take-up rate
#  33  Access to benefit - plan/occ-level
DATATYPE = {
    '% participation': '20',
    '10th %': '21',
    '25th %': '22',
    'median': '23',
    '75th %': '24',
    '90th %': '25',
    '% participation across all workers': '26',
    'establishments offering benefit': '27',
    'access to benefit occupation-level': '28',
    'access to benefit plan-level': '29',
    'access to benefit both': '33',
    'mean': '30',
    'share of premiums': '31',
    'take-up rate': '32',
}

# http://download.bls.gov/pub/time.series/nb/nb.provision
# code          text
# 023 Access to personal leave, sick leave, paid family leave, or vacation
# 025 Access to sick leave and vacation
# 027 Access to personal leave, vacation, or holidays
# 028 Access to personal leave and vacation
# 029 Access to vacation and holidays
# 030 Access to paid vacation
# 031 Mean # of annual paid vacation days after one yr of service
# 032 Median # of annual paid vacation days after one yr of service
# 039 Mean # of annual paid vacation days after five yrs of service
# 040 Median # of annual paid vacation days after five yrs of service
# 047 Mean # of annual paid vacation days after ten yrs of service
# 048 Median # of annual paid vacation days after ten yrs of service
# 055 Mean # of annual paid vacation days after twenty yrs of service
# 056 Median # of annual paid vacation days after twenty yrs of service
# 069 Mean # of paid vacation days after 1 yr of service for workers w/out consolidated leave plans
# 070 Mean # of paid vacation days after 5 yrs of service for workers w/out consolidated leave plans
# 071 Mean # of paid vacation days after 10 yrs of service for workers w/out consolidated leave plans
# 072 Mean # of paid vacation days after 20 yrs of service for workers w/out consolidated leave plans
PROVISION = {
    'acc to personal, sick, paid family, or vacation': '023',
    'acc to sick and vacation': '025',
    'acc to personal, vacation, or holidays': '027',
    'acc to personal and vacation': '028',
    'acc to vacation and holidays': '029',
    'acc to paid vacation': '030',
    'mean after 1yr': '031',
    'median after 1yr': '032',
    'mean after 5yrs': '039',
    'median after 5yrs': '040',
    'mean after 10yrs': '047',
    'median after 10yrs': '048',
    'mean after 20yrs': '055',
    'median after 20yrs': '056',
    'mean after 1yr w/o clp': '069',
    'mean after 5yrs w/o clp': '070',
    'mean after 10yrs w/o clp': '071',
    'mean after 20yrs w/o clp': '072',
}


def _reverse(dict_):
    # assumes no two keys correspond to the same value
    return {v: k for k, v in dict_.iteritems()}


def _find_or_questions(item, dict_):
    if item in dict_:
        return dict_[item]
    return '???'


def decode_series_id(series_id):
    pref = PREFIX
    seasonal = _find_or_questions(
        series_id[2], _reverse(SEASON_ADJUST))
    ownership = _find_or_questions(
        series_id[3], _reverse(OWNERSHIP))
    estimate = _find_or_questions(
        series_id[4 : 6], _reverse(ESTIMATE))
    industry = _find_or_questions(
        series_id[6 : 11], _reverse(INDUSTRY))
    occupation = _find_or_questions(
        series_id[12 : 16], _reverse(OCCUPATION))
    subcell = _find_or_questions(
        series_id[16 : 18], _reverse(SUBCELL))
    datatype = _find_or_questions(
        series_id[18 : 20], _reverse(DATATYPE))
    provision = _find_or_questions(
        series_id[20 : 23], _reverse(PROVISION))
    return ', '.join([pref, seasonal, ownership, estimate, industry,
                      occupation, subcell, datatype, provision])
