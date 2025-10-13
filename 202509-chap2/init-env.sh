#!/usr/bin/env bash
VERSION=3.13
python${VERSION} -m venv venv${VERSION}
. venv${VERSION}/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
