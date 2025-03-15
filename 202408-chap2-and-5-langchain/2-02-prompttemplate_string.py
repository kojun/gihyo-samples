#!/usr/bin/env python
from langchain_core.prompts import (
    PromptTemplate,
)

prompt_template = PromptTemplate.from_template(
    "与えた単語を{language}に変換してください"
)
result = prompt_template.invoke({"language": "日本語"})
print(result)
