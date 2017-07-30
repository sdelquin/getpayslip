import click
import datetime
import sys
from log import init_logger
from payslip import PaySlip

logger = init_logger(__file__)
today = datetime.date.today()


@click.command()
@click.option("-m",
              "--month",
              default=today.month,
              help="Ordinal number of month from which takes the payslip")
@click.option("-y",
              "--year",
              default=today.year,
              help="Year from which takes the payslip")
@click.option("-n",
              "--next-month",
              is_flag=True,
              help="Indicates if get the next non-downloaded payslip")
@click.option("-e",
              "--send-mail",
              is_flag=True,
              help="Indicates if an email will be sent")
@click.option("--clean",
              is_flag=True,
              help="Remove already downloaded payslips in pdf format")
def main(month, year, next_month, send_mail, clean):
    p = PaySlip(month, year)

    if clean:
        logger.info("Removing all downloaded payslips in pdf format")
        PaySlip.clean()
        sys.exit()

    if next_month:
        logger.debug("next-month option enabled")
        p.set_next_month()

    logger.info(f"Beginning access to payslip {p.id}")
    try:
        p.get_payslip()
    except:
        logger.error("Exiting...")
        sys.exit()

    if next_month:
        logger.info("Updating last-payslip file")
        p.update_last_payslip()

    if send_mail:
        logger.info("Sending mail attached with downloaded payslip")
        p.send_payslip()


if __name__ == "__main__":
    main()
