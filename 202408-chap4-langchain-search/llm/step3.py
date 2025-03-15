from typing import (
    TypedDict,
    Annotated,
    Literal,
)
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langserve import add_routes
from langgraph.graph import (
    StateGraph,
    END,
    START,
)
from langgraph.graph.message import (
    add_messages,
)
from langgraph.prebuilt import ToolNode
from langchain_core.runnables import (
    RunnableConfig,
)
from langchain_community.tools.tavily_search import (
    TavilySearchResults,
)
import pprint

app = FastAPI(
    title="LangChain Server",
    version="1.0",
)


class State(TypedDict):
    messages: Annotated[
        list, add_messages
    ]


def call_model(
    state: State, config: RunnableConfig
):
    messages = state["messages"]
    print("####### call_modelが呼ばれました。stateの値を表示します。この中のmessagesの値を使ってmodelを呼び出します")
    pprint.pprint(state)
    response = model.invoke(
        messages, config
    )
    print("####### modelからレスポンスが返ってきました。responseの値を表示します。この値をmessagesの値としたものが新たなstateとなります")
    pprint.pprint(response)
    return {"messages": response}


def should_continue(
    state: State,
) -> Literal["__end__", "tools"]:
    messages = state["messages"]
    last_message = messages[-1]
    # messagesには、一般的に、HumanMessage, AIMessage, ToolMessageが含まれるようだ。
    # このうち、最後のメッセージがAIMessageになっていて、それがtools_callsを返すことがあり(ツールのサポートが必要と判断したということ）、その場合のみ、toolsノードに遷移させる。
    # AIMessageオブジェクトはたとえば以下のような構造を返す。以下の例の場合はtool_callsを返しているので、toolsに遷移する。
    #    AIMessage(
    #      content='',
    #      additional_kwargs={'tool_calls': [{'index': 0, 'id': 'call_rqeuqw3GWcBBHEoTLXBe3xri', 'function': {'arguments': '{"query":"大谷翔平 今日 成績"}', 'name': 'tavily_search_results_json'}, 'type': 'function'}]},
    #      response_metadata={'finish_reason': 'tool_calls'},
    #      id='run-01ccc771-edab-41fe-a5ae-6d569d98c045',
    #      tool_calls=[{'name': 'tavily_search_results_json', 'args': {'query': '大谷翔平 今日 成績'}, 'id': 'call_rqeuqw3GWcBBHEoTLXBe3xri', 'type': 'tool_call'}])
    print("******* should_continueが呼ばれました。stateの値を表示します。この中のmessagesの最後の要素の値をもとに遷移先を判定します")
    pprint.pprint(state)
    if not last_message.tool_calls:
        print("   ******* ENDに遷移しますね。")
        return END
    else:
        print("   ******* toolsに遷移しますね。")
        return "tools"


tools = [
    TavilySearchResults(max_results=2)
]

model = ChatOpenAI(
    model="gpt-4o-2024-05-13"
)
model = model.bind_tools(tools)

graph = StateGraph(State)
tool_node = ToolNode(tools)

# "agent"ノードは、AIモデルをコールする。
graph.add_node("agent", call_model)

# "tools"ノードは、以下のようなコードになっているようだ。
# tools_by_name = {tool.name: tool for tool in tools}
# def tool_node(state:dict):
#   result = []
#   for tool_call in state["messages"][-1].tool_calls:
#     tool = tools_by_name[tool_call["name"]]
#     observation = tool.invoke(tool_call["args"])
#     result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
#   return {"messages": result}
graph.add_node("tools", tool_node)

# 最初はagentノードから始める
graph.add_edge(START, "agent")

# agentがおわったら、should_continueの結果によってtoolsに行くかENDにするかを決める
graph.add_conditional_edges(
    "agent", should_continue
)

# toolsから返ってきたらagentに戻す（このときMessageの最後はToolMessageになってるのでそれを使ってAIMessageを追加するイメージ）
graph.add_edge("tools", "agent")

compiled = graph.compile()

add_routes(
    app,
    compiled,
    path="/graph",
)
