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

URL1 = 'http://www.gobiernodecanarias.org/educacion/General/Seguridad/\
scripts/SUAGDILogin.asp'
URL2 = 'http://www.gobiernodecanarias.org/educacion/General/Seguridad/\
Scripts/SUAGDILoginMetodos.asp'
URL3 = 'https://www.gobiernodecanarias.org/educacion/8/Certificados/\
NominillasInter/Scripts/NominillasMain.asp'
URL4 = 'https://www.gobiernodecanarias.org/educacion/8/Certificados/\
NominillasInter/Scripts/imprimir_ws.asp?nominilla='

LOGIN_POST_DATA = {
    'h': '',
    'Tipo': '4',
    'id': '1',
    'Nif': MEDUSA_USERNAME,
    'ClaveActual': MEDUSA_PASSWORD,
    'submit': 'Entrar',
    'opcion': 'LoginGDI'
}

ERROR_STRING_IN_RESPONSE = 'error|mantenimiento'
REQUEST_TIMEOUT = 10
