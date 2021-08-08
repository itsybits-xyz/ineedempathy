#!/usr/bin/env bash

set -e

# frontend
cd frontend
npm run build
cd ..

# Backend
rm -fr dist ineedempathy.pyz

poetry build --format wheel
pip install shiv
pip install -r <(poetry export -f requirements.txt --without-hashes --with-credentials) --target dist/
pip install --no-deps ./dist/backend-0.1.0-py3-none-any.whl --target dist/

shiv --site-packages=dist \
    --python="/usr/bin/python" \
    --output-file=ineedempathy.pyz \
    --entry-point=backend.entrypoint

# Identification
echo $GITHUB_SHA > latest_sha.txt
echo $GITHUB_SHA > templates/latest_sha.txt
