## MCPサーバの基本的な例。
サンプルプログラムは以下を参照。<br>
https://github.com/iwamot/ai-agent-mcp-samples<br>
pythonの初期化は以下で実施。
- uv init
- uv add 'strands-agents[openai]'
- uv add prompt_toolkit
- uv add mcp
- uv add mcp-server-fetch
- uv add mcp-server-time

### agent.py
- AIモデルを指定してやりとりするだけのシンプルな例。AIモデルの知識範囲でしか答えられない。外部参照とかはできない。

### agent2.py
- Fetch MCP Serverを使って、指定したURLから情報を取得できるようにした例。
- 元のサンプルはdocker経由でmcp/fetchを起動しているが、例によってnetskopeの壁に阻まれるため、サンプルのままでは動かない。以下のように修正し、uv run agent2.py で動かせばOK（uv経由じゃなくても動くはず）。
- 事前に uv add mcp mcp-server-fetch しておく（uvを使う場合）。
- 環境変数 REQUESTS_CA_BUNDLE や SSL_CERT_FILE は設定した状態で動かすこと。
```
<< BEFORE >>
fetch_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="docker",
            args=["run", "-i", "--rm", "mcp/fetch"],
        )
    )
)

<< AFTER >>
fetch_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command=sys.executable,
            args=["-m", "mcp_server_fetch"],
            env={**os.environ},
        )
    )
)
```

### agent3.py
- mcp/fetchとmcp/sequentialthinkingを組み合わせた例。
- 入力例：「https://tech.enechange.co.jp/entry/2025/06/11/173107 を全て読んで、段階的に考えてレビューして」
- ソースの修正は、fetch_mcp_clientについては agent2.py と同様。もうひとつの seq_think_mcp_client については、dockerではやはり証明書エラーになるので、同等のNode.js部品を用いる。
```
<< BEFORE >>
seq_think_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="docker",
            args=["run", "-i", "--rm", "mcp/sequentialthinking"],
        )
    )
)

<< AFTER >>
seq_think_mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-sequential-thinking"],
        )
    )
)
```

### agent5.py
- agent3.pyに、MCP Time Serverを追加しただけのもの。

