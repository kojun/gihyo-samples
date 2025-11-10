# Claude Codeを使ってみる
## プロジェクトの作成
まず、以下でプロジェクトを作成。
```
uv init cinii-books-search
cd cinii-books-search
uv add ruff mypy pytest --dev
```
## claudeの初期化
- Claude Codeで /init を実行する。これで、CLAUDE.mdが作成される。
- Claude Codeには、プロジェクトの設定やルールなどを記憶するメモリ機能がある。その中心になるのがCLAUDE.mdである。
- 個人の共通設定はグローバル設定（~/.claude/CLAUDE.md）に記載すればよい。
## プランモードで計画立案
- Shift-TABで実装モードを切り替えられる。Accept Editsモード、デフォルトモード、プランモード。プランモードではファイル変更が行われないので安全。
- 今回はプランモードでたとえば以下のように入力する。
```
URLからAPIの仕様を確認し、JSON形式のデータを保存するdownload_json.pyを作成します。深く考えて実装の計画を立ててください。

URL: https://support.nii.ac.jp/ja/cib/api/b_opensearch
検索条件:
- author: @driller
- year_from: 2015年
レスポンス仕様: JSON-LD
保存先: data/cinii_books.json
特記事項: appidが必須となっているが不要
```
- なお、プランモードで計画提示後にESCで入力画面に戻り、デフォルトまたはAccept Editsモードで次のように指示すると、計画を記録することができる。んでもって、この実装計画に従って実装を進めてよ、っていうこともできる。
```
この実装計画をplans/cinii-books-download-json.mdに記録してください
```
## カスタムスラッシュコマンド
頻繁に使用するプロンプトは、カスタムスラッシュコマンドとして登録可能。.claude/commandsディレクトリにMarkdownを配置すると、独自コマンドとして使える。プロンプトで、
```
ruff, mypy, pytestを利用したコードの品質を確認・修正・テストするプロンプトを .cloaude/commands/quality-fix.md に作成してください。
```
とか書くと、.claude/commands/quality-fix.mdがいい感じで作成される。
## Conext7 MCPサーバの活用
```
claude mcp add -s project context7 -- npx -y @upstash/context7-mcp
```
これで、プロジェクトスコープでContext7が使えるようになる。プロンプトで、「Use context7」っていう文言を含めると、なんか魔法のようなことが起きるようだ。

