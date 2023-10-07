#!/bin/bash
cd "$(dirname "$0")"
set -ex

source venv/bin/activate
cd src
alembic revision --autogenerate -m "autogenerate message"
