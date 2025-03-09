## ソースコード
以下を参照<br>
https://github.com/mkazutaka/software-design-202408-llmapp

## JetBrainsのIDEの設定
WebStormで実行できるようにしてみる。Gitは、python(llm)とnext.js(web)が両方入ったモノレポ構成とする。

## python環境構築
```
mkdir llm
cd llm
python3 -m venv venv
source venv/bin/activate
pip install langchain==0.2.3 langchain-openai==0.1.8 langgraph==0.0.66 langserve==0.2.2 langchain-community==0.2.4 fastapi==0.111.0
# 追加分
pip install sse_starlette
または
pip install -r requirements.txt
```
★★ Pythonは3.11を使用。3.13だと一部うまく動かないものがあるっぽい。
★★ なお、Python 3.11でも上記だけだともしかするとうまく動かないかも。いちおう、v3.11のvenv環境で pip freeze した結果を、requirements-v311-freezed.txt に保管してある。

### 以下でうまくいった。
```
mkdir llm
cd llm
python3.11 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements-v311-freezed.txt
```

## Next.js環境構築（初期作成時）
```
cd ..
npx create-next-app@14.2.3
> What is your project name? ... web
それ以外はそのまま選択

これでwebディレクトリができてその中に初期テンプレートができるので、その後、諸々修正を加える。
```

## Next.js環境構築（展開時）
```
cd web
npm install
これで、初期環境構築した時と同じものがインストールされる、はず。
```

## ステップ毎の設定内容
#### STEP1
- LLM側
```
curl -X POST 'http://localhost:8000/openai/invoke' -H 'Content-Type: application/json' -d '{"input":[{"type":"human","content":"最近の技術の進歩が早すぎてちょっと心配です"}]}' | jq -r .
```
なお、invokeをstreamに変えることで、ストリームでのレスポンスを受け取れるようだ。
ドキュメント（OpenAPI）は http://localhost:8000/docs

#### STEP2
- LLM側
```
curl -X POST 'http://localhost:8000/graph/invoke' -H 'Content-Type: application/json' -d '{"input":{"messages": [["user","天気おしえろ"]]}}' | jq -r .
```
#### STEP3
- LLM側
```
curl -X POST 'http://localhost:8000/graph/invoke' -H 'Content-Type: application/json' -d '{"input":{"messages": [["user","直近の世界情勢をもとに、気の利いたジョークを言ってみてください"]]}}' | jq -r .
```
- WEB側
```
npm run dev

npm install ai@3.1.35
```
