#!/bin/bash

poetry run python ./script/seed.py
poetry run uvicorn backend.main:app --reload
