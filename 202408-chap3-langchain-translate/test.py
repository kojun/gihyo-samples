from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "プログラミングにおける再帰の概念を説明する詩を書いてください。"}
  ]
)

print(completion.choices[0].message)
