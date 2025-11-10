# download_json.py 実装計画

## 概要
CiNii Books OpenSearch APIから書籍データを取得し、JSON-LD形式で保存するスクリプトを作成します。

## API仕様の確認結果

### エンドポイント
```
https://ci.nii.ac.jp/books/opensearch/search
```

### リクエストパラメータ
| パラメータ | 値 | 説明 |
|-----------|-----|------|
| `author` | `@driller` | 著者名（固定値） |
| `year_from` | `2015` | 出版年（開始年、固定値） |
| `format` | `json` | レスポンス形式（JSON-LD） |
| `count` | `200` | 1ページあたりの取得件数（最大値） |

**注意**: 仕様上`appid`パラメータが必須とされていますが、実際には不要なため含めません。

### レスポンス形式
- JSON-LD形式
- `@context`: 名前空間定義
- `@graph`: 検索結果の配列
  - 各アイテムには`dc:title`, `dc:creator`, `dc:date`, `cinii:ownerCount`などが含まれる

## 実装内容

### 1. `build_api_url()` - APIリクエストURL構築
```python
def build_api_url(author: str, year_from: int, format_type: str = "json") -> str:
    """CiNii Books APIのリクエストURLを構築"""
```

**機能**:
- ベースURL + クエリパラメータを組み立て
- `urllib.parse.urlencode()`を使用
- パラメータ:
  - `author`: 著者名
  - `year_from`: 出版年（開始）
  - `format`: レスポンス形式
  - `count`: 取得件数（デフォルト200）

### 2. `fetch_books_data()` - データ取得
```python
def fetch_books_data(url: str) -> dict[str, Any]:
    """APIからデータを取得してJSONをパース"""
```

**機能**:
- `urllib.request.urlopen()`でHTTPリクエスト
- タイムアウト: 30秒
- UTF-8デコード
- `json.loads()`でパース

**エラーハンドリング**:
- `urllib.error.HTTPError`: HTTPステータスエラー（404, 500など）
- `urllib.error.URLError`: ネットワークエラー、タイムアウト
- `json.JSONDecodeError`: JSONパースエラー

### 3. `save_json()` - JSON保存
```python
def save_json(data: dict[str, Any], output_path: Path) -> None:
    """データをJSON形式でファイルに保存"""
```

**機能**:
- `Path.parent.mkdir(parents=True, exist_ok=True)`でディレクトリ自動作成
- `json.dump()`でファイル書き込み
  - `ensure_ascii=False`: 日本語をそのまま保存
  - `indent=2`: 見やすいインデント

### 4. `count_items()` - 結果サマリー
```python
def count_items(data: dict[str, Any]) -> int:
    """取得したアイテム数をカウント"""
```

**機能**:
- `@graph`キーから配列を取得
- アイテム数をカウント
- 最初の数件のタイトルと著者を表示

### 5. `main()` - メイン処理
```python
def main() -> None:
    """メイン処理"""
```

**処理フロー**:
1. 固定パラメータの設定（`author="@driller"`, `year_from=2015`）
2. APIリクエストURL構築
3. データ取得
4. ファイル保存（`data/cinii_books.json`）
5. 結果サマリー表示
6. エラー発生時は`sys.stderr`に出力して`sys.exit(1)`

## コーディング規約

### Python 3.13の機能活用
- 型ヒント: `dict[str, Any]`, `list[dict[str, Any]]`, `int | None`
- `match/case`パターンマッチング（必要に応じて）
- `pathlib.Path`の使用

### ドキュメンテーション
```python
def function_name(param: type) -> return_type:
    """関数の説明

    Args:
        param: パラメータの説明

    Returns:
        戻り値の説明

    Raises:
        ExceptionType: 例外の説明
    """
```

### エラーハンドリングパターン
```python
try:
    # 処理
except HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
    sys.exit(1)
except URLError as e:
    print(f"Network Error: {e.reason}", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"JSON Parse Error: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Unexpected Error: {e}", file=sys.stderr)
    sys.exit(1)
```

## ファイル構成

```
cinii-books-search/
├── download_json.py          # 新規作成
├── search_books_by_date.py   # 既存（参考にするコードスタイル）
├── main.py                   # 既存
├── data/
│   └── cinii_books.json      # 出力先（既存ファイルを上書き）
├── plans/
│   └── cinii-books-download-json.md  # このファイル
└── pyproject.toml
```

## 使用ライブラリ

すべて標準ライブラリのみ:
- `urllib.request`: HTTP通信
- `urllib.parse`: URLエンコーディング
- `urllib.error`: HTTPエラーハンドリング
- `json`: JSON処理
- `pathlib`: ファイルパス操作
- `sys`: エラー出力と終了コード

## 実行方法

```bash
# スクリプト実行
uv run python download_json.py

# 期待される出力例
Fetching data from CiNii Books API...
Author: @driller
Year from: 2015

Successfully saved data to: data/cinii_books.json
Total items retrieved: 42

Sample results:
1. Title: "例のタイトル" by 著者名
2. Title: "別のタイトル" by 別の著者
...
```

## テスト観点

1. **正常系**:
   - APIから正しくデータを取得できること
   - JSON-LD形式で保存されること
   - `data`ディレクトリが自動作成されること

2. **異常系**:
   - ネットワークエラー時のハンドリング
   - 不正なJSONレスポンスのハンドリング
   - HTTPエラー（404, 500など）のハンドリング

3. **データ検証**:
   - `@graph`キーが存在すること
   - 各アイテムに必要なフィールドが含まれること
   - 日本語が正しくエンコードされていること

## 参考リンク

- CiNii Books OpenSearch API仕様: https://support.nii.ac.jp/ja/cib/api/b_opensearch
- JSON-LD: https://json-ld.org/
