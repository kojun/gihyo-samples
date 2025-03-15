#!/usr/bin/env bash
. "$(dirname "$0")/demo-env.fnc"
uvicorn main-step3:app --reload
