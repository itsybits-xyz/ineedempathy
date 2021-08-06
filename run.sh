#!/bin/bash

poetry run uvicorn backend.main:app --reload
