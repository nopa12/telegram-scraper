#!/bin/bash
cd "$(dirname "$0")"
set -ex

source venv/bin/activate
python ./src/c_backend.py