#!/usr/bin/env bash
. "$(dirname "$0")/common.fnc"
uvicorn step1:app --reload
