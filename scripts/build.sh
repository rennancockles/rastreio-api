#!/bin/sh -e

set -x


pip install -r requirements.txt -t ./reqs
cd reqs && zip -r9 ../lambda.zip . && cd ..
zip -r lambda.zip app.py
