#!/bin/bash
cd "$(dirname "$0")"
set -ex

source venv/bin/activate
cd src
alembic upgrade head
