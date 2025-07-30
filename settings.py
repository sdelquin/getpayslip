from prettyconf import config

MEDUSA_USERNAME = config('MEDUSA_USERNAME')
MEDUSA_PASSWORD = config('MEDUSA_PASSWORD')

BREVO_API_KEY = config('BREVO_API_KEY')
BREVO_SENDER_EMAIL = config('BREVO_SENDER_EMAIL')
BREVO_SENDER_NAME = config('BREVO_SENDER_NAME')

TO_EMAIL_ADDRESS = config('TO_EMAIL_ADDRESS')

LAST_DOWNLOADED_PAYSLIP_FILE = config('LAST_DOWNLOADED_PAYSLIP_FILE', default='last_payslip.dat')

PAYSLIP_URL = config('PAYSLIP_URL', default='https://www.gobiernodecanarias.org/educacion')

# seconds waiting for each page loading
TIME_OUT = config('TIME_OUT', default=10, cast=int)
