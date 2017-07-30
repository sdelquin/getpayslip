# GetPayslip

Tool for getting the monthly payslips of Consejería de Educación GOBCAN

## Installation

1. Install `python`. Preferably v3.5 / v3.6
2. Create a *virtualenv* .
3. Activate the *virtualenv* and follow these steps:
~~~console
$> pip install -r requirements.txt
$> cp config.example.py config.py
# edit config.py with your own values
~~~

## Usage

~~~console
Usage: main.py [OPTIONS]

Options:
  -m, --month INTEGER  Ordinal number of month from which takes the payslip
  -y, --year INTEGER   Year from which takes the payslip
  -n, --next-month     Indicates if get the next non-downloaded payslip
  -e, --send-mail      Indicates if an email will be sent
  --clean              Remove already downloaded payslips in pdf format
  --help               Show this message and exit.
~~~

## Examples

> Download payslip of April 2015

~~~console
$> python main.py -m 4 -y 2015
~~~

> Download next payslip (based on last execution)

~~~console
$> python main.py -n
~~~

> Download next payslip and send it attached on email.
> You should configure your email in `config.py`.

~~~console
$> python main.py -n -e
# this is the same as:
$> run.sh
~~~

## Tests

~~~console
$> pytest
~~~
