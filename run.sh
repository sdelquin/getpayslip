#!/bin/bash
# Master script.

cd "$(dirname "$0")"
source $HOME/.virtualenvs/getpayslip/bin/activate
python main.py -n -e
