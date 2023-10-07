#!/bin/bash
cd "$(dirname "$0")"
set -ex

source venv/bin/activate
python ./src/a_get_session_string.py