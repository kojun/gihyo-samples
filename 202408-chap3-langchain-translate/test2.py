#!/usr/bin/env python

import os
import requests

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("No OPENAI_API_KEY set!")
    exit(1)

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

try:
    # OpenAIのv1/modelsエンドポイントを直接叩く
    response = requests.get("https://api.openai.com/v1/models", headers=headers)
    print("Status code:", response.status_code)
    print("Response:", response.json())
except requests.exceptions.RequestException as e:
    print("Error:", e)

