#!/usr/bin/env python

from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex concepts with creative flair."},
    {"role": "user", "content": "鎮痛剤の機序について語ってください"}
  ]
)

print(completion.choices[0].message)
