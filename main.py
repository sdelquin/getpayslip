import datetime
import sys

import click

import lib.date_utils as date_utils
from lib.log import init_logger
from lib.payslip import PaySlip

logger = init_logger(__file__)
today = datetime.date.today()


@click.command()
@click.option(
    '-e',
    '--send-mail',
    is_flag=True,
    help='Indicates if an email will be sent',
)
@click.option(
    '--clean',
    is_flag=True,
    help='Remove already downloaded payslips in pdf format',
)
@click.option(
    '--browser',
    is_flag=True,
    help='Show the browser for debugging purposes',
)
def main(send_mail, clean, browser):
    if clean:
        PaySlip.clean()
        sys.exit()

    p = PaySlip(*date_utils.find_next_month(), headless=not browser)
    try:
        result = p.get_payslip()
    except Exception as err:
        logger.error(err)
        sys.exit()

    if send_mail and result:
        p.send_payslip()


if __name__ == '__main__':
    main()
