import os

from vars_to_csv import vars_to_csv

"""
USAGE:
python make_csvs.py

CREATES:
1984.csv, 2011.csv
"""

def main():
    CSV1984 = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '1984.csv'))
    with open(CSV1984, 'w+') as f:
        vars_to_csv(
            [
                ('V10474', 'given_vac'),      # JOB GET PD VAC?
                ('V10475', 'hrs_paid_vac'),   # PD VAC HRS
                ('V10553', 'took_vac'),       # WTR VACATION
                ('V10554', 'weeks_vac'),      # WEEKS VACATION
                ('V10419', 'age'),            # AGE OF 1984 HEAD
                ('V10222', 'fam_size'),       # # IN FU-1984
                ('V10277', 'income83'),       # H+W 1983 TAXABLE Y
                ('V10420', 'sex'),            # SEX OF 1984 HEAD
                ('V10463', 'salary'),         # PAY/HR-SALARY
                ('V10453', 'employment'),     # EMPLOYMENT STATUS-HD
            ],
            'fam1984', f)

    CSV2011 = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '2011.csv'))
    with open(CSV2011, 'w+') as f:
        vars_to_csv(
            [
                ('ER47480', 'industry'),     # MAIN IND FOR JOB 1: 2000 CODE
                ('ER47630', 'took_vac'),     # WTR VACATION
                ('ER47631', 'days_vac'),     # DAYS VACATION
                ('ER47633', 'weeks_vac'),    # WEEKS VACATION
                ('ER47635', 'months_vac'),   # MONTHS VACATION
                ('ER47317', 'age'),          # AGE OF HEAD
                ('ER47316', 'fam_size'),     # # IN FU
                ('ER52259', 'income10'),     # HEAD AND WIFE TAXABLE INCOME
                ('ER47318', 'sex'),          # SEX OF HEAD
                ('ER47495', 'salary_amt'),   # SALARY AMOUNT
                ('ER47496', 'salary_unit'),  # SALARY PER WHAT
                ('ER47448', 'employment'),   # EMPLOYMENT STATUS-1ST MENTION
            ],
            'fam2011er', f)


if __name__ == '__main__':
    main()