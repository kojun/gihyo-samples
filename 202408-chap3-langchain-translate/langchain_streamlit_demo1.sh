#!/usr/bin/env bash -e
. venv/bin/activate
export OPENAI_API_KEY=${MY_OPENAI_API_KEY:-dummy}
streamlit run langchain_streamlit_demo1.py
