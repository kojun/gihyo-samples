#!/usr/bin/env bash
. "$(dirname "$0")/demo-env.fnc"
uvicorn main-step2:app --reload
