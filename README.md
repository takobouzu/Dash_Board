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
<img width="469" alt="Monosnap 2021-02-28 23-10-51" src="https://user-images.githubusercontent.com/24547343/109421491-dff44c80-7a1a-11eb-8167-6350dddccce1.png">

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
<img width="470" alt="Monosnap 2021-02-28 23-17-33" src="https://user-images.githubusercontent.com/24547343/109421561-3d889900-7a1b-11eb-8c72-2c8a8c76de48.png">

+ iPadのpythonista3を起動して、iPad内のフォルダ「Dash_Board」に格納されている「dash_board.py」を実行する。
<img width="474" alt="Monosnap 2021-02-28 23-28-22" src="https://user-images.githubusercontent.com/24547343/109422177-cc96b080-7a1d-11eb-803e-610ad4aa5210.png">
<img width="466" alt="Monosnap 2021-02-28 23-29-00" src="https://user-images.githubusercontent.com/24547343/109422193-db7d6300-7a1d-11eb-88c3-2128c5941894.png">

+　主な機能

[出走表選択]を選択し、[開催日付]-[ボートレース場]-[レース番号]を選択すると出走表・能力値・展開情報が表示される
<img width="442" alt="Monosnap 2021-02-28 23-29-28" src="https://user-images.githubusercontent.com/24547343/109422198-e46e3480-7a1d-11eb-99d6-4396ccf7621e.png">
<img width="470" alt="Monosnap 2021-02-28 23-31-22" src="https://user-images.githubusercontent.com/24547343/109422213-efc16000-7a1d-11eb-81eb-3eab8316c2ae.png">
<img width="470" alt="Monosnap 2021-02-28 23-32-22" src="https://user-images.githubusercontent.com/24547343/109422222-fc45b880-7a1d-11eb-8835-fc594a338a75.png">

[選手歴・モータ歴・部品歴]を選択し、選手を選択すると、選手の戦歴、モーターの戦歴、モーターの部品交換歴が表示される。
<img width="470" alt="Monosnap 2021-02-28 23-33-02" src="https://user-images.githubusercontent.com/24547343/109422231-08ca1100-7a1e-11eb-8e38-adecbb582626.png">
<img width="473" alt="Monosnap 2021-02-28 23-33-38" src="https://user-images.githubusercontent.com/24547343/109422239-12537900-7a1e-11eb-8d72-abf9175d3f4f.png">
<img width="457" alt="Monosnap 2021-02-28 23-34-10" src="https://user-images.githubusercontent.com/24547343/109422252-1da6a480-7a1e-11eb-9e79-87b08a454402.png">

[twitter]を選択し、選手を選択すると選手名でtwitterの最新投稿検索結果が表示される。
<img width="470" alt="Monosnap 2021-02-28 23-34-52" src="https://user-images.githubusercontent.com/24547343/109422267-3020de00-7a1e-11eb-9578-dc7596ea8e45.png">

[投票]を選択することで、舟券を購入することができる。
<img width="472" alt="Monosnap 2021-02-28 23-35-18" src="https://user-images.githubusercontent.com/24547343/109422282-3fa02700-7a1e-11eb-8616-429942cd7772.png">

[レース結果]を選択することで、出走表として表示されているレースの結果が表示される。表示されているレースリプレイを選択することで、レースや展示のリプレイ再生が可能。
<img width="472" alt="Monosnap 2021-02-28 23-35-36" src="https://user-images.githubusercontent.com/24547343/109422283-4169ea80-7a1e-11eb-8950-f0403addbff9.png">

[データ検索]を選択し、フォルダ「SQL」に格納されているSQLを選択することで、SQLの実行結果が表示される。
<img width="473" alt="Monosnap 2021-02-28 23-36-05" src="https://user-images.githubusercontent.com/24547343/109422284-429b1780-7a1e-11eb-90b1-69412dd5e78f.png">


Dash Boardの機能解説と活用方法は、[wiki](https://github.com/takobouzu/Dash_Board/wiki)に掲載する。


# ライセンス

MIT License.

Copyright (c) 2021 蛸坊主/たこぼうず
