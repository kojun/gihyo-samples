#!/usr/bin/env bash
. "$(dirname "$0")/common.fnc"
uvicorn step3:app --reload
