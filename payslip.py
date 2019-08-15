import calendar
import glob
import os

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sgw.core import SendGrid

import config
import date_utils
from log import init_logger

logger = init_logger(__file__)


class PaySlip():
    def __init__(self, month, year):
        logger.info('START: Building PaySlip object')
        self.month, self.year = month, year
        self._init_webdriver()

    def _init_webdriver(self):
        # selenium configurations
        options = Options()
        options.headless = True

        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.dir', os.getcwd())
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk',
                               'application/pdf')
        profile.set_preference('pdfjs.migrationVersion', 1)

        self.driver = webdriver.Firefox(
            options=options, firefox_profile=profile)

    def __del__(self):
        self.driver.quit()

    def __str__(self):
        month_name = calendar.month_name[self.month]
        return f'{month_name} {self.year}'

    @property
    def id(self):
        return f'{self.year}{self.month:02}'

    @property
    def filename(self):
        return f'{self.id}.pdf'

    def get_payslip(self, update_last_payslip=True):
        self.clean()

        logger.info('Loading first page')
        self.driver.get(config.PAYSLIP_URL)
        # login
        logger.info('Login')
        element = self.driver.find_element_by_id('username')
        element.send_keys(config.MEDUSA_USERNAME)
        element = self.driver.find_element_by_id('password')
        element.send_keys(config.MEDUSA_PASSWORD)
        element = self.driver.find_element_by_id('btn-login')
        element.click()
        # wait for page to be loaded
        try:
            payslip_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'ultima')))
        except TimeoutException:
            logger.error('Timeout waiting for page loading')
            return False
        element = self.driver.find_element_by_xpath('//*[@id=\
"principal_interior"]/table/tbody/tr[3]/td/table/tbody/tr/td[3]/table/tbody/\
tr/td[2]/table/tbody/tr/td/table[9]/tbody/tr[2]/td[3]')
        month, year = date_utils.parse_date(element.text)

        if month == self.month and year == self.year:
            logger.info('Downloading payslip')
            payslip_button.click()
            os.rename('image.vbs.asp.pdf', self.filename)
            logger.info(f'Payslip {self} successfully downloaded!')
            if update_last_payslip:
                self._update_last_payslip()
            return True
        else:
            logger.warning(f'Payslip {self} is not yet available!')
            return False

    def _update_last_payslip(self):
        logger.info('Updating last-payslip file')
        f = open(config.LAST_DOWNLOADED_PAYSLIP_FILE, "w")
        f.write(self.id)
        f.close()

    def send_payslip(self):
        logger.info('Sending email with attached downloaded payslip')
        email = SendGrid(
            config.SENDGRID_APIKEY,
            config.SENDGRID_FROM_EMAIL,
            config.SENDGRID_FROM_NAME
        )
        email.send(
            to=config.TO_EMAIL_ADDRESS,
            subject=f'Payslip {self}',
            msg="It's only money 💶💶💶 but I like it! 🐼",
            attachments=self.filename
        )

    @staticmethod
    def clean():
        logger.info('Removing previously downloaded payslips in pdf format')
        for f in glob.glob('*.pdf'):
            os.remove(f)
