#!/usr/bin/env bash
. "$(dirname "$0")/common.fnc"
uvicorn step2:app --reload
