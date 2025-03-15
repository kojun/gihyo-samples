#!/usr/bin/env python

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.prompts.chat import SystemMessagePromptTemplate

temlate = ChatPromptTemplate.from_messages(
    messages=[
        (
            "system",
            "単語を{language}に変換して",
        ),
        ("user", "Hello"),
    ]
)
# もしくは
prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "与えた単語を{language}に変換してください"
        ),
        HumanMessage(content="Hello"),
    ]
)

print("===パターン1===")
result = temlate.invoke({"language": "日本語"})
print(result)

print("\n===パターン2===")
result2 = prompt_template.invoke({"language": "日本語"})
print(result2)
