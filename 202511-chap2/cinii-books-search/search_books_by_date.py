"""CiNii Books JSONデータから日付範囲で書籍を検索するスクリプト

dc:dateフィールドを使用して年範囲で書籍を検索します。
"""

import json
import sys
from pathlib import Path
from typing import Any


def load_books_data(file_path: Path) -> dict[str, Any]:
    """JSON-LDファイルから書籍データを読み込む

    Args:
        file_path: JSON-LDファイルのパス

    Returns:
        読み込んだJSON-LDデータ

    Raises:
        FileNotFoundError: ファイルが見つからない場合
        json.JSONDecodeError: JSON解析エラー
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def extract_year_from_date(date_str: str) -> int | None:
    """dc:date文字列から年を抽出する

    Args:
        date_str: dc:dateフィールドの値(例: "2020", "2017")

    Returns:
        抽出された年(整数)、抽出できない場合はNone
    """
    if not date_str:
        return None

    # 文字列から数字部分を取得
    date_str = date_str.strip()

    # 4桁の年として解釈を試みる
    try:
        year = int(date_str)
        # 妥当な年の範囲チェック(1000-9999年)
        if 1000 <= year <= 9999:
            return year
    except ValueError:
        pass

    return None


def filter_books_by_year_range(
    data: dict[str, Any],
    year_from: int | None = None,
    year_to: int | None = None,
    exact_year: int | None = None,
) -> list[dict[str, Any]]:
    """年範囲で書籍をフィルタリングする

    Args:
        data: JSON-LDデータ
        year_from: 開始年(この年以降)
        year_to: 終了年(この年以前)
        exact_year: 特定の年(指定時は他の引数を無視)

    Returns:
        フィルタリングされた書籍のリスト
    """
    # @graphから書籍データを取得
    if "@graph" not in data or not isinstance(data["@graph"], list):
        return []

    graph = data["@graph"]
    if not graph:
        return []

    # 最初の要素がチャネル情報を含む
    channel_data = graph[0]
    if "items" not in channel_data:
        return []

    items = channel_data["items"]
    filtered_items = []

    for item in items:
        # dc:dateフィールドを取得
        dc_date = item.get("dc:date")
        if not dc_date:
            continue

        # 年を抽出
        year = extract_year_from_date(dc_date)
        if year is None:
            continue

        # パターンマッチで検索条件をチェック
        match (exact_year, year_from, year_to):
            case (int(y), _, _):
                # 特定の年検索
                if year == y:
                    filtered_items.append(item)
            case (None, int(from_y), int(to_y)):
                # 範囲検索(両方指定)
                if from_y <= year <= to_y:
                    filtered_items.append(item)
            case (None, int(from_y), None):
                # from以降
                if year >= from_y:
                    filtered_items.append(item)
            case (None, None, int(to_y)):
                # to以前
                if year <= to_y:
                    filtered_items.append(item)

    return filtered_items


def display_search_results(items: list[dict[str, Any]]) -> None:
    """検索結果を表示する

    Args:
        items: 検索結果の書籍リスト
    """
    if not items:
        print("No books found matching the criteria.")
        return

    print(f"\nFound {len(items)} book(s):\n")
    print("=" * 80)

    for i, item in enumerate(items, 1):
        title = item.get("title", "N/A")
        dc_date = item.get("dc:date", "N/A")
        creator = item.get("dc:creator", "N/A")

        # パターンマッチで出版社データの型を処理
        match item.get("dc:publisher", "N/A"):
            case list() as pub_list:
                publisher = ", ".join(pub_list)
            case str() as pub_str:
                publisher = pub_str
            case _:
                publisher = "N/A"

        owner_count = item.get("cinii:ownerCount", "N/A")
        link = item.get("link", {}).get("@id", "N/A")

        print(f"{i}. {title}")
        print(f"   Year: {dc_date}")
        print(f"   Creator: {creator}")
        print(f"   Publisher: {publisher}")
        print(f"   Owner Count: {owner_count}")
        print(f"   URL: {link}")
        print("-" * 80)


def main() -> None:
    """メイン処理"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Search CiNii Books by date range",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search books from 2020 onwards
  python search_books_by_date.py --year-from 2020

  # Search books up to 2020
  python search_books_by_date.py --year-to 2020

  # Search books between 2017 and 2020
  python search_books_by_date.py --year-from 2017 --year-to 2020

  # Search books from exactly 2020
  python search_books_by_date.py --exact-year 2020
""",
    )

    parser.add_argument(
        "--year-from",
        type=int,
        help="Start year (inclusive)",
    )
    parser.add_argument(
        "--year-to",
        type=int,
        help="End year (inclusive)",
    )
    parser.add_argument(
        "--exact-year",
        type=int,
        help="Search for exact year (overrides --year-from and --year-to)",
    )
    parser.add_argument(
        "--data-file",
        type=Path,
        default=Path("data/cinii_books.json"),
        help="Path to the JSON-LD data file (default: data/cinii_books.json)",
    )

    args = parser.parse_args()

    # 引数の検証
    if args.exact_year is None and args.year_from is None and args.year_to is None:
        parser.error(
            "At least one of --year-from, --year-to, or --exact-year must be specified"
        )

    if args.year_from is not None and args.year_to is not None:
        if args.year_from > args.year_to:
            parser.error("--year-from must be less than or equal to --year-to")

    print("=" * 80)
    print("CiNii Books Date Range Search")
    print("=" * 80)

    # パターンマッチで検索条件を表示
    match (args.exact_year, args.year_from, args.year_to):
        case (int(y), _, _):
            print(f"Search Criteria: Exact year = {y}")
        case (None, int(from_y), int(to_y)):
            print(f"Search Criteria: {from_y} - {to_y}")
        case (None, int(from_y), None):
            print(f"Search Criteria: {from_y} onwards")
        case (None, None, int(to_y)):
            print(f"Search Criteria: Up to {to_y}")

    print(f"Data file: {args.data_file}")
    print("=" * 80)

    try:
        # データの読み込み
        data = load_books_data(args.data_file)

        # 検索実行
        results = filter_books_by_year_range(
            data,
            year_from=args.year_from,
            year_to=args.year_to,
            exact_year=args.exact_year,
        )

        # 結果表示
        display_search_results(results)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
