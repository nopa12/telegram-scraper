#!/bin/bash
cd "$(dirname "$0")"
set -ex

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt