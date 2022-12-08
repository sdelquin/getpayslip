#!/bin/bash
# Master script.

source ~/.pyenv/versions/getpayslip/bin/activate
cd "$(dirname "$0")"
exec python main.py -e
