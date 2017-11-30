MEDUSA = {
    "username": "xxxxxxxxxxxx",
    "password": "xxxxxxxxxxxx"
}

ELASTIC_EMAIL = {
    "URL": "https://api.elasticemail.com/v2/email/send",
    "FROM_MAIL": "xxxxxxxxxxxx",
    "FROM_NAME": "xxxxxxxxxxxx",
    "APIKEY": "xxxxxxxxxxxx"
}

TO_EMAIL_ADDRESS = "xxxxxxxxxxxx"

URL1 = "http://www.gobiernodecanarias.org/educacion/General/Seguridad/\
scripts/SUAGDILogin.asp"
URL2 = "http://www.gobiernodecanarias.org/educacion/General/Seguridad/\
Scripts/SUAGDILoginMetodos.asp"
URL3 = "https://www.gobiernodecanarias.org/educacion/8/Certificados/\
NominillasInter/Scripts/NominillasMain.asp"
URL4 = "https://www.gobiernodecanarias.org/educacion/8/Certificados/\
NominillasInter/Scripts/imprimir_ws.asp?nominilla="

LOGIN_POST_DATA = {
    "h": "",
    "Tipo": "4",
    "id": "1",
    "Nif": MEDUSA["username"],
    "ClaveActual": MEDUSA["password"],
    "submit": "Entrar",
    "opcion": "LoginGDI"
}

ERROR_STRING_IN_RESPONSE = "error|mantenimiento"
LAST_DOWNLOADED_PAYSLIP_FILE = "last_payslip.dat"
LOGFILE = "getpayslip.log"
LOGFILE_MAX_SIZE = 102400
REQUEST_TIMEOUT = 10
