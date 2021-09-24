#!/bin/sh -e

export SOURCE_FILES="app.py"

set -x

black $SOURCE_FILES
isort $SOURCE_FILES