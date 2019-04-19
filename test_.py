import datetime
import locale
import os
import re

import PyPDF2

from payslip import PaySlip


def getpayslip(month, year):
    p = PaySlip(month, year)
    p.get_payslip(update_last_payslip=False)
    assert os.path.exists(p.filename)

    # get the month name in spanish
    locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")
    date = datetime.date(year, month, 1)
    month_name = date.strftime("%B").upper()
    date_in_spanish = f"{month_name} DE {year}"

    pdf_reader = PyPDF2.PdfFileReader(open(p.filename, "rb"))
    text = pdf_reader.getPage(0).extractText().upper()
    assert re.search(date_in_spanish, text)
    PaySlip.clean()


def test():
    previous_month = datetime.datetime.now() - datetime.timedelta(days=31)
    getpayslip(previous_month.month, previous_month.year)
