# GetPayslip

Tool for getting the monthly payslips of Consejería de Educación GOBCAN

## Installation

1. Install `python`. Preferably v3.5 / v3.6
2. Create a *virtualenv* .
3. Activate the *virtualenv* and follow these steps:

~~~console
$ pipenv install
$ vi .env    # set the corresponding values
...
~~~

## Requirements

1. Firefox
2. Geckodriver

## Usage

~~~console
Usage: main.py [OPTIONS]

Options:
  -e, --send-mail      Indicates if an email will be sent
  --clean              Remove already downloaded payslips in pdf format
  --help               Show this message and exit.
~~~

## Examples

> Download next payslip:

~~~bash
>> python main.py
~~~

> Download next payslip and send it attached on email:

~~~bash
>> python main.py -e
~~~

## Tests

~~~bash
>> pytest
~~~

## Using with cron

It can be a good approach to use this tool with a cron job.
For example, here we launch the script every day to check if a new payslip is available and send it via email:

~~~bash
>> crontab -l
@daily $HOME/getpayslip/run.sh
~~~
