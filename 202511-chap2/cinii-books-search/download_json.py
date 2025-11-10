"""CiNii Books OpenSearch APIから書籍データをJSON-LD形式で取得するスクリプト

検索条件:
- 著者: @driller
- 出版年: 2015年以降
"""

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


def build_api_url(author: str, year_from: int) -> str:
    """APIリクエスト用のURLを構築する

    Args:
        author: 著者名
        year_from: 検索開始年

    Returns:
        完全なAPIリクエストURL
    """
    base_url = "https://ci.nii.ac.jp/books/opensearch/search"
    params = {
        "author": author,
        "year_from": str(year_from),
        "format": "json",  # JSON-LD形式を指定
    }
    query_string = urllib.parse.urlencode(params)
    return f"{base_url}?{query_string}"


def fetch_books_data(url: str) -> dict[str, Any]:
    """APIからデータを取得する

    Args:
        url: APIリクエストURL

    Returns:
        取得したJSON-LDデータ

    Raises:
        urllib.error.HTTPError: HTTPリクエストエラー
        urllib.error.URLError: URL接続エラー
        json.JSONDecodeError: JSON解析エラー
    """
    print(f"Fetching data from: {url}")

    with urllib.request.urlopen(url, timeout=30) as response:
        if response.status != 200:
            raise Exception(f"HTTP Error: {response.status}")

        data = response.read().decode("utf-8")
        return json.loads(data)


def save_json(data: dict[str, Any], output_path: Path) -> None:
    """JSONデータをファイルに保存する

    Args:
        data: 保存するデータ
        output_path: 出力先ファイルパス
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Data saved to: {output_path}")


def count_items(data: dict[str, Any]) -> int:
    """取得したアイテム数をカウントする

    Args:
        data: JSON-LDデータ

    Returns:
        アイテム数
    """
    # JSON-LDの構造に応じてアイテムをカウント
    if "@graph" in data:
        # @graphがある場合、その中のアイテムをカウント
        graph = data["@graph"]
        if isinstance(graph, list):
            return len(graph)
    return 0


def main() -> None:
    """メイン処理"""
    # 検索条件
    author = "@driller"
    year_from = 2015
    output_path = Path("data/cinii_books.json")

    print("=" * 60)
    print("CiNii Books Data Download")
    print("=" * 60)
    print(f"Author: {author}")
    print(f"Year from: {year_from}")
    print(f"Output: {output_path}")
    print("=" * 60)

    try:
        # APIからデータを取得
        url = build_api_url(author, year_from)
        data = fetch_books_data(url)

        # 取得したアイテム数を表示
        item_count = count_items(data)
        print(f"Items retrieved: {item_count}")

        # JSONファイルに保存
        save_json(data, output_path)

        print("=" * 60)
        print("Download completed successfully!")
        print("=" * 60)

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
