#!/usr/bin/env python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo")
messages = [("user", "こんにちは")]
result = model.invoke(messages)
print(result)
