#!/usr/bin/env bash
VERSION=3.11
python${VERSION} -m venv venv${VERSION}
. venv${VERSION}/bin/activate
pip install --upgrade pip
pip install -r requirements-v311-freezed.txt
