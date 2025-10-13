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
