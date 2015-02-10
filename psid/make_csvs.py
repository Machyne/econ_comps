from vars_to_csv import vars_to_csv

"""
USAGE:
python make_csvs.py

CREATES:
1984.csv, 2011er.csv
"""

def main():
    with open('1984.csv', 'w+') as f:
        vars_to_csv(
            [
                ('V10475', 'hrs_paid_vac'),   # PD VAC HRS
                ('V10476', 'type_paid_vac'),  # TYPE PAID VAC
                ('V10553', 'took_vac'),       # WTR VACATION
                ('V10554', 'weeks_vac'),      # WEEKS VACATION
                ('V10419', 'age'),            # AGE OF 1984 HEAD
                ('V10222', 'fam_size'),       # # IN FU-1984
                ('V10277', 'income83'),       # H+W 1983 TAXABLE Y
                ('V10420', 'sex'),            # SEX OF 1984 HEAD
                ('V10463', 'salary'),         # PAY/HR-SALARY
            ],
            'fam1984', f)

    with open('2011er.csv', 'w+') as f:
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
                ('ER47495', 'salary_amt'),   # SALARY AMOUNT"
                ('ER47496', 'salary_unit'),  # SALARY PER WHAT"
            ],
            'fam2011er', f)


if __name__ == '__main__':
    main()