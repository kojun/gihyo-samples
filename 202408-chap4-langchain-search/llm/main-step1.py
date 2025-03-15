from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langserve import add_routes

app = FastAPI(
    title="LangChain Server",
    version="1.0",
)

add_routes(
    app,
	ChatOpenAI(model="gpt-4o-2024-05-13"),
    path="/openai",
)
