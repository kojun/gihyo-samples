＜使い方＞

(1) Claude Codeインストール
npm install -g @anthropic-ai/claude-code
これで、AnthropicのClaude Code Agentがインストールされる。

なお、インストール先をしりたいときは
npm root -g
すればよい。
Homebrewのnode.js環境では、
/opt/homebrew/lib/node_modules
になる。
また、インストールされたモジュール一覧は
npm list -g --depth=0
で知ることができる。
claudeコマンドは、/opt/homebrew/binにインストールされる（実際にはシンボリックリンク）。

(2) Playwright MCPサーバの追加
claude mcp add playwright -- npx -y @playwright/mcp@latest
これで、~/.claude.json にMCPサーバ定義が追加される。

また、claude mcp listで確認できる。
個別に見たいときは、claude mcp get playwright

(3) アプリの作成とPlaywightによる動作確認
claudeを起動して、プロンプトで以下を入力。
生年月日と性別を入力して、星占いをするアプリを作り、Playwright MCPで動作確認を行ってください。

これで、horoscope.htmlっていうファイルができて、なんかいろいろガサガサ動きます。

==============
プロンプトの例
==============

目的:
生年月日(YYYY-MM-DD)と性別を入力して占い結果を返すWebアプリを作成し、
Playwright MCPでE2E検証し、結果報告書を作成・提出してください。

要件:
- コードは ./app に保存。フレームワークは任意（最小構成でOK、ローカルHTTPサーバ可）。
- Playwright MCPで以下のテストを実施:
  1) フォーム表示確認（生年月日・性別ラジオ/セレクトがある）
  2) 正常系: 1990-01-01 / female を入力 → 期待: 星座は山羊座、結果テキストに "Capricorn" を含む
  3) 異常系: 未入力で送信 → エラー表示
- すべてのテストで Assert を入れてPass/Failを判定。consoleに理由を出力。
- スクリーンショットを最大6枚まで ./artifacts に保存。ファイル名は 01-..., 02-... で先頭ゼロ付き。
- 最終成果物として ./REPORT.md を出力。以下の章立てで作成:
  # 1. アプリ概要（構成/依存/起動手順）
  # 2. テスト計画（観点・期待値・環境）
  # 3. テスト結果サマリー（表: 観点/期待/結果/証跡/コメント）
  # 4. 主要スクリーンショット（Markdownで相対パス埋め込み＋各3行説明）
  # 5. 課題と改善案（3項目以上）
  # 6. 付録（実行コマンド・ログ要約）
- 画像は相対パスで `![caption](artifacts/01-form.png)` の形式で埋め込むこと。
- 最後に、作成したファイル一覧を箇条書きで提示。

制約:
- スクショは6枚まで。採用理由を各画像下に記載。
- レポートは2,000〜3,000文字を目安。
- すべてローカルで再現可能にする（起動コマンド、ポート番号明記）。

================
Playwrightの役割
================
役割の分担
フェーズ	どの部分が担当するか	実際にやっていること
① アプリ構築（HTML/JS/Pythonなどの生成）	Claude Code（＝LLM自体）	プロンプトからUIやロジックのコードを生成
② 実行・動作確認	Playwright MCPサーバー	ローカルでブラウザを起動し、アプリにアクセスしてテスト
③ 証跡取得	Playwright MCP	スクリーンショットやログを収集
④ レポート作成	Claude Code（LLM）	収集した証跡やログをもとに報告書を構成
