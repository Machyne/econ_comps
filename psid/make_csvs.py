from vars_to_csv import vars_to_csv


def main():
    with open('1984.csv', 'w+') as f:
        vars_to_csv(
            [
                'V10475',  # PD VAC HRS
                'V10476',  # TYPE PAID VAC
                'V10419',  # AGE OF 1984 HEAD
                'V10420',  # SEX OF 1984 HEAD
                'V10554',  # WEEKS VACATION
                'V10463',  # PAY/HR-SALARY
            ],
            'fam1984', f)

    with open('2007er.csv', 'w+') as f:
        vars_to_csv(
            [
                'ER36133',  # MAIN IND FOR JOB 1: 2000 CODE
                'ER36291',  # DAYS VACATION
            ],
            'fam2007er', f)

    with open('2009er.csv', 'w+') as f:
        vars_to_csv(
            [
                'ER42168',  # MAIN IND FOR JOB 1: 2000 CODE
                'ER42318',  # DAYS VACATION
            ],
            'fam2009er', f)

    with open('2011er.csv', 'w+') as f:
        vars_to_csv(
            [
                'ER47480',  # MAIN IND FOR JOB 1: 2000 CODE
                'ER47631',  # DAYS VACATION
            ],
            'fam2011er', f)


if __name__ == '__main__':
    main()