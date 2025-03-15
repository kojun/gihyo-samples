#!/usr/bin/env python

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
)
from langchain.chains import LLMChain

#model = ChatOpenAI(model="gpt-3.5-turbo")
model = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "与えた単語を{language}に変換してください",
        ),
        ("user", "Shit, you son of a bitch"),
    ]
)

chain = LLMChain(llm=model, prompt=prompt)
result = chain.run(
    {
        "language": "江戸っ子の言葉",
    }
)
print(result)
