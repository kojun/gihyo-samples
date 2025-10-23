# MCPサーバの構築例

AWS What's NewのRSSフィードから、与えられたキーワードで最新のコンテンツを検索します。

## 機能
- Tool: `search_aws_updates`
  - キーワードを入力すると、最新のAWSアップデートを最大3件まで検索して返す

## 使い方
- python環境セットアップ（略）
- python aws_updates.py を実行し、エラーなくスクリプト実行状態になればOK。
  - 確認後はctrl-Cで停止してよい。
- 手動でMCPサーバを登録。~/.claude.jsonが更新される。
  - claude mcp add aws-updates $(which python) $(pwd)/aws_updates.py

## 利用方法

claude codeを起動して「Amazon Bedrockのアップデートを検索して」などと入力。
