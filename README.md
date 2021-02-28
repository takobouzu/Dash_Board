# Dash_Board

Dash_Boardは、[ボートレースデータベース「BOAT_RACE_DB」](https://github.com/takobouzu/BOAT_RACE_DB)のiPadクライアントである。

# 目次

- [動作環境](#動作環境)
- [インストール](#インストール)
- [使い方](#使い方)
- [ライセンス](#ライセンス)

# 動作環境

| OS/パッケージ      | バージョン | 用途                   |
| ------------------ | ---------- | ---------------------- |
| iOS         | 12.3.1     | OS                     |
| pythonista3 | 3.7.3      | python3実行環境           |


# インストール

iPad内のフォルダ「Dash_Board」を作成して、フォルダ「Dash_Board」に下記のファイルを格納する。

## ファイル構成

| ファイル名      | 用途                   |
| ------------- | ---------------------- |
|dash_board.py  | Dash_Board本体         |
|base_html.py| HTMLテンプレート           |
|base_sql.py| SQL定義          |
|sql| データ検索用SQL格納フォルダ           |
|sql/000_本日の逃げ狙い目.sql|データ検索用SQLサンプルル          |
|boatrace.db|BOAT_RACE_DB](https://github.com/takobouzu/BOAT_RACE_DB)で構築したDBファイル|


# 使い方

+ boatrace.dbは常に最新の状態をiPad内のフォルダ「Dash_Board」に格納しておくこと。
+ iPadのpythonista3を起動して、iPad内のフォルダ「Dash_Board」に格納されている「dash_board.py」を実行する。

# ライセンス

MIT License.

Copyright (c) 2021 蛸坊主/たこぼうず
