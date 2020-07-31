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


class PaySlip:
    def __init__(self, month, year, headless=True):
        logger.info('START: Building PaySlip object')
        self.month, self.year = month, year
        self._init_webdriver(headless)

    def _init_webdriver(self, headless):
        # Selenium configurations
        options = Options()
        options.headless = headless

        profile = webdriver.FirefoxProfile()
        # Controls the default folder to download a file to. 0 indicates the Desktop;
        # 1 indicates the systems default downloads location; 2 indicates a custom folder.
        profile.set_preference('browser.download.folderList', 2)
        # Holds the custom destination folder for downloading
        profile.set_preference('browser.download.dir', os.getcwd())
        # stores a comma-separated list of MIME types to save to disk without asking
        # what to use to open the file
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/pdf')
        # Prevent Firefox from previewing PDFs
        profile.set_preference('pdfjs.disabled', True)
        # Needs to be false, so that Firefox won't scan and load plugins
        profile.set_preference('plugin.scan.plid.all', False)
        # Is a key that holds the minimum allowed version number that Adobe Acrobat
        # is allowed to launch. Setting it to a number larger than currently installed
        # Adobe Acrobat version should do the trick.
        profile.set_preference('plugin.scan.Acrobat', '99.0')

        self.driver = webdriver.Firefox(options=options, firefox_profile=profile)

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
        try:
            self.driver.get(config.PAYSLIP_URL)
            WebDriverWait(self.driver, config.TIME_OUT).until(
                EC.presence_of_element_located((By.ID, 'btn-login'))
            )
        except TimeoutException:
            logger.error('Timeout waiting for page loading')
            return False
        # login
        logger.info('Login')
        element = self.driver.find_element_by_id('username')
        element.send_keys(config.MEDUSA_USERNAME)
        element = self.driver.find_element_by_id('password')
        element.send_keys(config.MEDUSA_PASSWORD)
        element = self.driver.find_element_by_id('btn-login')
        # wait for page to be loaded
        try:
            element.click()
            payslip_button = WebDriverWait(self.driver, config.TIME_OUT).until(
                EC.presence_of_element_located((By.NAME, 'ultima'))
            )
        except TimeoutException:
            logger.error('Timeout waiting for page loading')
            return False
        element = self.driver.find_element_by_xpath(
            '//*[@id=\
"principal_interior"]/table/tbody/tr[3]/td/table/tbody/tr/td[3]/table/tbody/\
tr/td[2]/table/tbody/tr/td/table[9]/tbody/tr[2]/td[3]'
        )
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
            config.SENDGRID_APIKEY, config.SENDGRID_FROM_EMAIL, config.SENDGRID_FROM_NAME
        )
        email.send(
            to=config.TO_EMAIL_ADDRESS,
            subject=f'Payslip {self}',
            msg="It's only money 💶💶💶 but I like it! 🐼",
            attachments=self.filename,
        )

    @staticmethod
    def clean():
        logger.info('Removing previously downloaded payslips in pdf format')
        for f in glob.glob('*.pdf'):
            os.remove(f)
