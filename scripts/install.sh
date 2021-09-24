#!/bin/sh -e

set -x

python -m pip install -U pip
pip install -r requirements-dev.txt
