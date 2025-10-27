## MCPサーバの基本的な例。
サンプルプログラムは以下を参照。<br>
https://github.com/iwamot/ai-agent-mcp-samples<br>
pythonの初期化は以下で実施。
- uv init
- uv add 'strands-agents[openai]'
- uv add prompt_toolkit

### agent.py
- AIモデルを指定してやりとりするだけのシンプルな例。AIモデルの知識範囲でしか答えられない。外部参照とかはできない。

### agent2.py
- Fetch MCP Serverを使って、指定したURLから情報を取得できるようにした例。
- 元のサンプルはdocker経由でmcp/fetchを起動しているが、例によってnetskopeの壁に阻まれるため、サンプルのままでは動かない。


