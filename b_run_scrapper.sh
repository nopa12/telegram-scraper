#!/bin/bash
cd "$(dirname "$0")"
set -ex

source venv/bin/activate
python ./src/b_run_scrapper.py