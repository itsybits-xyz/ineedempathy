#!/usr/bin/env bash

set -e

rm -fr dist ineedempathy.pyz

poetry build --format wheel
pip install shiv
pip install -r <(poetry export -f requirements.txt --without-hashes --with-credentials) --target dist/
pip install --no-deps ./dist/backend-0.1.0-py3-none-any.whl --target dist/

shiv --site-packages=dist \
    --python="/home/amjith/opt/python-3.9.5/bin/python3" \
    --output-file=ineedempathy.pyz \
    --entry-point=backend.entrypoint
