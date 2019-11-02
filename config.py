from prettyconf import config

MEDUSA_USERNAME = config('MEDUSA_USERNAME')
MEDUSA_PASSWORD = config('MEDUSA_PASSWORD')

SENDGRID_APIKEY = config('SENDGRID_APIKEY')
SENDGRID_FROM_EMAIL = config('SENDGRID_FROM_EMAIL')
SENDGRID_FROM_NAME = config('SENDGRID_FROM_NAME')

TO_EMAIL_ADDRESS = config('TO_EMAIL_ADDRESS')

LAST_DOWNLOADED_PAYSLIP_FILE = config(
    'LAST_DOWNLOADED_PAYSLIP_FILE',
    default='last_payslip.dat'
)

PAYSLIP_URL = config('PAYSLIP_URL',
                     default='https://www.gobiernodecanarias.org/educacion')
