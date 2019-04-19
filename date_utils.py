import datetime
import re

import config

MONTHS_IN_SPANISH = {
    'ENERO': 1,
    'FEBRERO': 2,
    'MARZO': 3,
    'ABRIL': 4,
    'MAYO': 5,
    'JUNIO': 6,
    'JULIO': 7,
    'AGOSTO': 8,
    'SEPTIEMBRE': 9,
    'OCTUBRE': 10,
    'NOVIEMBRE': 11,
    'DICIEMBRE': 12
}


def parse_date(date_str):
    month_str, year_str = re.split(r' +de +', date_str)
    return MONTHS_IN_SPANISH.get(month_str.upper()), int(year_str)


def find_next_month():
    f = open(config.LAST_DOWNLOADED_PAYSLIP_FILE)
    last_downloaded_payslip = f.readline().strip()
    f.close()
    year, month = int(last_downloaded_payslip[:4]),\
        int(last_downloaded_payslip[4:])
    next_date = datetime.date(year=year, month=month, day=1) + \
        datetime.timedelta(days=31)
    return next_date.month, next_date.year
