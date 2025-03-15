#!/usr/bin/env bash
python3.11 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements-v311-freezed.txt
