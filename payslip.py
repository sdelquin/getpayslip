import requests
import config
import glob
import os
from log import init_logger
import datetime
from dateutil.relativedelta import relativedelta
import sys
import re
import calendar
import elasticemail

logger = init_logger(__file__)


class PaySlip():
    def __init__(self):
        today = datetime.date.today()
        self.year, self.month = today.year, today.month

    def id(self):
        return "{}{:02}".format(self.year, self.month)

    def clean(self):
        for f in glob.glob("*.pdf"):
            os.remove(f)
        sys.exit()

    def set_next_month(self):
        try:
            f = open(config.LAST_DOWNLOADED_PAYSLIP_FILE)
            last_downloaded_payslip = f.readline().strip()
            f.close()
            year, month = int(last_downloaded_payslip[:4]),\
                int(last_downloaded_payslip[4:])
            next_date = datetime.date(year=year, month=month, day=1) + \
                relativedelta(months=+1)
            self.year, self.month = next_date.year, next_date.month
            logger.info("Setting target payslip {}/{}".format(
                self.month, self.year
            ))
        except Exception as err:
            logger.error(err)

    def get_payslip(self):
        logger.debug("Getting the first ASP session cookie")
        try:
            r = requests.get(config.URL1,
                             timeout=config.REQUEST_TIMEOUT)
            cookies = dict(r.cookies)
        except Exception as err:
            logger.error(err)
            logger.error("First ASP session cookie NOT FOUND! Exiting...")
            sys.exit()

        logger.debug("Getting the SUA cookie")
        try:
            r = requests.post(config.URL2,
                              data=config.LOGIN_POST_DATA,
                              cookies=cookies,
                              timeout=config.REQUEST_TIMEOUT)
            new_cookies = dict(r.history[0].cookies)
            cookies = {**cookies, **new_cookies}
        except Exception as err:
            logger.error(err)
            logger.error("SUA cookie NOT FOUND! Exiting...")
            sys.exit()

        logger.debug("Getting the second ASP session cookie")
        try:
            r = requests.get(config.URL3,
                             cookies=cookies,
                             timeout=config.REQUEST_TIMEOUT)
            new_cookies = dict(r.history[0].cookies)
            cookies = {**cookies, **new_cookies}
        except Exception as err:
            logger.error(err)
            logger.error(
                "Second ASP session cookie NOT FOUND! Exiting..."
            )
            sys.exit()

        logger.debug("Getting the payslip in PDF format")
        payslip_url = config.URL4 + self.id()
        try:
            r = requests.get(payslip_url,
                             cookies=cookies,
                             timeout=config.REQUEST_TIMEOUT)
        except Exception as err:
            logger.error(err)
            logger.error("Timeout in getting the payslip! Exiting...")
            sys.exit()

        if not re.search(r"{}".format(config.ERROR_STRING_IN_RESPONSE),
                         r.text, re.IGNORECASE):
            self.output_filename = "{}.pdf".format(self.id())
            logger.debug("Writing response to {}".format(self.output_filename))
            f = open("{}".format(self.output_filename), "wb")
            f.write(r.content)
            f.close()
        else:
            logger.warning("Payslip does no exist!")
            sys.exit()

    def update_last_payslip(self):
        f = open(config.LAST_DOWNLOADED_PAYSLIP_FILE, "w")
        f.write(self.id())
        f.close()

    def send_payslip(self):
        month_name = calendar.month_name[self.month]
        elasticemail.send(
            to=config.TO_EMAIL_ADDRESS,
            subject="Payslip {} {}".format(month_name, self.year),
            body="It's only money 💶💶💶 but I like it! 🐼",
            attachments=self.output_filename
        )
        logger.debug("Deleting {}".format(self.output_filename))
        os.remove(self.output_filename)
