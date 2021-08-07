#!/bin/bash

/home/baylee/.local/bin/poetry run python ./script/seed.py
/home/baylee/.local/bin/poetry run uvicorn backend.main:app --reload
