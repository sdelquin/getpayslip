#!/bin/bash
# Master script.

source ~/.virtualenvs/getpayslip/bin/activate
cd "$(dirname "$0")"
exec python main.py -e
