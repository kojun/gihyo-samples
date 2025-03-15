#!/usr/bin/env python

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
)
from langchain_core.output_parsers import (
    StrOutputParser,
)

model = ChatOpenAI(model="gpt-3.5-turbo")
parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "与えた単語を{language}に変換してください",
        ),
        ("user", "What the hell is going on here?"),
    ]
)

chain = prompt | model | parser
result = chain.invoke(
    {
        "language": "日本語(名古屋弁)",
    }
)
print(result)
# => こんにちわ
