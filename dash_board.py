"""
【システム】BOAT RACE DASH BOARD(ボートレースダッシュボート)
【ファイル】dash_board.py
【機能仕様】ボートレース関連情報を画面表示
【動作環境】pythonista3
【開発来歴】2021.03.01 Ver 1.00
"""

"""
使用ライブラリ
    pythonista3　組込済みライブラリー
        ・ui                ui
        ・sqlite3           sqlite3データベース
        ・console           コンソール
        ・urllib.request    WEB操作
        ・re                正規表現操作
        ・import datetime   日付操作
    pythonista3　追加インストールしたライブラリ
        ・BeautifulSoup     HTMLパーサー
	ユーザ定義ライブラリー
		・base_sql			データ検索SQL定義
		・html_sql			検索結果html定義    
"""
import ui
import os
import sqlite3
import console
import urllib.request
import urllib.parse
import re
import unicodedata
from datetime import datetime, date, timedelta
import requests
from bs4 import BeautifulSoup
import base_sql
import base_html

#グローバル変数定義
dbname = "boatrace.db"  #データベース名
in_yyyymmdd = ""			  #画面から入力された日付
in_poolcode = ""			  #画面から入力された場コード
in_raceno = ""			  	#画面から入力されたレース番号
in_playerno = ""			  #画面から入力された選手番号
in_playername = ""      #画面から入力された選手名
in_motorno = ""				  #画面から入力されたモーター番号
kaisai_list = []			  #リストに開催日付を表示するための配列
pool_list = []				  #リストに場名を表示するための配列
race_list = []				  #リストにレース番号を表示するための配列
player_list = []			  #リストに選手情報を表示するための配列
sql_list = []           #データ検索SQL一覧を表示するための配列
old_yyyymmdd = ""
old_poolcode = ""			  
old_raceno = ""			  	
old_playerno = ""			  
old_playername = ""      
old_motorno = ""	

"""
【関　数】button01_action
【引　数】なし
【戻り値】なし
【機　能】出走選択ビューの表示
"""
def button01_action(sender):
  global in_yyyymmdd
  global in_poolcode
  global in_raceno
  global old_yyyymmdd
  global old_poolcode
  global old_raceno
  old_yyyymmdd = in_yyyymmdd
  old_poolcode = in_poolcode
  old_raceno   = in_raceno
  wk_sql  = base_sql.kaisai_list_sql
  #SQLを実行して結果をリストに格納
  key_yyyymmdd = ''
  wk_list = ''
  wk_main = ''
  key_grade = ''
  flg = 0
  conn = sqlite3.connect(dbname)
  cur = conn.cursor()
  for row in cur.execute(wk_sql):
    wk_yyyymmdd = str(row[0])
    wk_pool_name = str(row[1])
    wk_grade = str(row[2])
    wk_title = str(row[3])
    wk_event_date = str(row[4])
    if key_yyyymmdd != wk_yyyymmdd:
      
      if flg == 1:
        wk = key_yyyymmdd + ' ' + wk_main + ' その他[' + wk_list + ']'
        kaisai_list.append(wk)
      else:
        flg = 1
      key_yyyymmdd = wk_yyyymmdd
      key_grade = wk_grade
      wk_list = wk_pool_name
      wk_main = wk_pool_name + ' ' + wk_grade + ' ' +  wk_title + '[' + wk_event_date + ']'
    else:
      wk_list = wk_list + ',' + wk_pool_name
      if ('一般' in key_grade) and (('Ｇ３' in wk_grade) or ('Ｇ２' in wk_grade) or ('Ｇ１' in wk_grade) or ('ＳＧ' in wk_grade)):
        wk_main = wk_pool_name + ' ' + wk_grade + ' ' +  wk_title + '[' + wk_event_date + ']'
        key_grade = wk_grade
      if ('Ｇ３' in key_grade) and (('Ｇ２' in wk_grade) or ('Ｇ１' in wk_grade) or ('ＳＧ' in wk_grade)):
        wk_main = wk_pool_name + ' ' + wk_grade + ' ' +  wk_title + '[' + wk_event_date + ']'
        key_grade = wk_grade
      if ('Ｇ２' in key_grade) and (('Ｇ１' in wk_grade) or ('ＳＧ' in wk_grade)):
        wk_main = wk_pool_name + ' ' + wk_grade + ' ' +  wk_title + '[' + wk_event_date + ']'
        key_grade = wk_grade
      if ('Ｇ１' in key_grade) and (('ＳＧ' in wk_grade)):
        wk_main = wk_pool_name + ' ' + wk_grade + ' ' +  wk_title + '[' + wk_event_date + ']'
        key_grade = wk_grade
  if flg == 1:
    wk = key_yyyymmdd + ' ' + wk_main + ' その他[' + wk_list + ']'
    kaisai_list.append(wk)
  cur.close()
  conn.close()
  #開催日選択テーブルビューに出力
  tableview013_listdata = ui.ListDataSource('')
  tableview013_listdata.items = kaisai_list
  tableview013.delegate = tableview013.data_source = tableview013_listdata
  tableview013_listdata.action = tableview013_action #開催日選択テーブルビューのアイテムが選択された場合に起動される関数
  tableview013.reload_data()
  #出走選択ビューの表示
  view01.present('popover')

"""
【関　数】tableview013_action
【引　数】なし
【戻り値】なし
【機　能】開催日選択テーブルビューのアイテムが選択された時の処理
          選択された日付で、場名選択テーブルビューを出力する。
"""
def tableview013_action(sender):
  global in_yyyymmdd
  pool_list.clear()
  race_list.clear()
  player_list.clear()
  #レースリストクリア
  tableview015_listdata = ui.ListDataSource('')
  tableview015_listdata.items = race_list
  tableview015.delegate = tableview015.data_source = tableview015_listdata
  tableview015.reload_data()

  #日付の抽出
  sel = sender.selected_row
  in_yyyymmdd = kaisai_list[sel][0:8]
	#選択された日付に施行されるボートレース場を検索するSQLを生成
  wk_sql  = base_sql.pool_list_sql
  target = '@yyyymmdd'; wk_sql = wk_sql.replace(target, in_yyyymmdd)
  #SQLを実行して結果をリストに格納
  conn = sqlite3.connect(dbname)
  cur = conn.cursor()
  for row in cur.execute(wk_sql):
    wk_pool_code		= str(row[0]) #場コード
    wk_pool_name		= str(row[1]) #場名
    wk_holding			= str(row[2]) #開催区分
    wk_grade			  = str(row[3]) #グレード
    wk_event_date		= str(row[4]) #開催日
    wk_title			  = str(row[5]) #シリーズタイトル
    wk = wk_pool_code + ':' + wk_pool_name + ' [' + wk_holding + ']' + ' [' + wk_grade  + ']' + ' ' + wk_event_date + ' ' + wk_title
    pool_list.append(wk)
  cur.close()
  conn.close()
  	#ボートレース場選択用のテーブルビューにリストを反映
  tableview014_listdata = ui.ListDataSource('')
  tableview014_listdata.items = pool_list
  tableview014.delegate = tableview014.data_source = tableview014_listdata
  tableview014_listdata.action = tableview014_action #ボートレース場テーブルビューのアイテムが選択された場合に起動される関数
  tableview014.reload_data()


"""
【関　数】tableview014_action
【引　数】なし
【戻り値】なし
【機　能】場選択テーブルビューが選択された時の処理
          選択された場名で、レース選択テーブルビューを出力する。
"""
def tableview014_action(sender):
  global in_yyyymmdd
  global in_poolcode
  global in_raceno
  in_raceno = ''
  race_list.clear()
  player_list.clear()
  #ボートレース場選択用のテーブルビューから選択された場コードを抽出
  sel = sender.selected_row
  in_poolcode = pool_list[sel][0] + pool_list[sel][1]
  #選択された日付と場コードでにレース一覧を検索するSQLを生成
  wk_sql  = base_sql.race_list_sql
  target = '@yyyymmdd'; wk_sql = wk_sql.replace(target, in_yyyymmdd)
  target = '@poolcode'; wk_sql = wk_sql.replace(target, in_poolcode)
  #SQLを実行して結果をリストに格納
  conn = sqlite3.connect(dbname)
  cur = conn.cursor()
  for row in cur.execute(wk_sql):
    race_list.append(row[0] + ' ' + row[1] + 'R 投票締切時刻 ' + row[2] + ' 「' + row[3] + '」 ' + row[4] + 'm ' + row[5] + ' ' + row[6])
  cur.close()
  conn.close()
  #レース選択用のテーブルビューにリストを反映
  tableview015_listdata = ui.ListDataSource('')
  tableview015_listdata.items = race_list
  tableview015.delegate = tableview015.data_source = tableview015_listdata
  tableview015_listdata.action = tableview015_action #レース番号選択テーブルビューのアイテムが選択された場合に起動される関数
  tableview015.reload_data()

"""
【関　数】tableview015_action
【引　数】なし
【戻り値】なし
【機　能】レース番号選択ビューテーブルのアイテムが選択された時の処理
          出走表を表示して、出走表選択ビューを閉じる
"""
def tableview015_action(sender):
  global in_yyyymmdd
  global in_poolcode
  global in_raceno
  sel = sender.selected_row
  wk_arry = race_list[sel].split(' ')
  wk_arry = wk_arry[1].split('R')
  in_raceno = wk_arry[0]
	
  wk_table1 = ''
  wk_sql = base_sql.race_table_sql
  target = '@yyyymmdd'; wk_sql = wk_sql.replace(target, in_yyyymmdd)
  target = '@poolcode'; wk_sql = wk_sql.replace(target, in_poolcode)
  target = '@raceno'; wk_sql = wk_sql.replace(target, in_raceno)
  conn = sqlite3.connect(dbname)
  cur = conn.execute(wk_sql)
  names = [description[0] for description in cur.description]
  rows = cur.fetchall()
	#HTMLテーブルのヘッダ行の生成
  wk_table1 = wk_table1 + '<table>'
  wk_table1 = wk_table1 + '<tr>'
  n = 0
  for name in names:
  	n = n + 1
  	if n == 1:
  		#ヘッダの一番左の項目を固定
  		wk_table1 = wk_table1 + '<th class="fixed01 text-center">' + name + '</th>' 
  	else:
  		#ヘッダ行を固定
  		wk_table1 = wk_table1 + '<th class="fixed02 text-center">' + name + '</th>' 
  wk_table1 = wk_table1 + '</tr>'
	#HTMLテーブルの明細行の生成
  for row in rows:
	  n = 0
	  wk_table1 = wk_table1 + '<tr>'
	  for i in range(len(row)):
		  n = n + 1
		  if n == 1:
			  #明細行の一番左の項目を固定
			  wk_table1 = wk_table1 + '<th class="fixed02 text-left">' + str(row[i]) + '</th>' 
		  else:
			  #明細行の生成
			  wk_table1 = wk_table1 + '<td class="text-right">' + str(row[i]) + '</td>' 
	  wk_table1 = wk_table1 + '</tr>'
  cur.close()
  conn.close()
  wk_table1 = wk_table1 + '</table>'
	#生成したHTMLファイルを画面表示
  wk_html = base_html.race_table_html
  if wk_table1 != '':
	  target = '@table1'; wk_html = wk_html.replace(target,wk_table1)
  else:
	  target = '@table1'; wk_html = wk_html.replace(target,'')
  webview0a.load_html(wk_html)
  main_view.name = race_list[sel]

  #能力表の作成
  wk_table1 = ''
  wk_sql = base_sql.race_table_sql2
  target = '@yyyymmdd'; wk_sql = wk_sql.replace(target, in_yyyymmdd)
  target = '@poolcode'; wk_sql = wk_sql.replace(target, in_poolcode)
  target = '@raceno'; wk_sql = wk_sql.replace(target, in_raceno)
  conn = sqlite3.connect(dbname)
  cur = conn.execute(wk_sql)
  names = [description[0] for description in cur.description]
  rows = cur.fetchall()
	#HTMLテーブルのヘッダ行の生成
  wk_table1 = wk_table1 + '<table>'
  wk_table1 = wk_table1 + '<tr>'
  n = 0
  for name in names:
  	n = n + 1
  	if n == 1:
  		#ヘッダの一番左の項目を固定
  		wk_table1 = wk_table1 + '<th class="fixed01 text-center">' + name + '</th>' 
  	else:
  		#ヘッダ行を固定
  		wk_table1 = wk_table1 + '<th class="fixed02 text-center">' + name + '</th>' 
  wk_table1 = wk_table1 + '</tr>'
	#HTMLテーブルの明細行の生成
  for row in rows:
	  n = 0
	  wk_table1 = wk_table1 + '<tr>'
	  for i in range(len(row)):
		  n = n + 1
		  if n == 1:
			  #明細行の一番左の項目を固定
			  wk_table1 = wk_table1 + '<th class="fixed02 text-left">' + str(row[i]) + '</th>' 
		  else:
			  #明細行の生成
			  wk_table1 = wk_table1 + '<td class="text-right">' + str(row[i]) + '</td>' 
	  wk_table1 = wk_table1 + '</tr>'
  cur.close()
  conn.close()
  wk_table1 = wk_table1 + '</table>'
	#生成したHTMLファイルを画面表示
  wk_html = base_html.race_table_html
  if wk_table1 != '':
	  target = '@table1'; wk_html = wk_html.replace(target,wk_table1)
  else:
	  target = '@table1'; wk_html = wk_html.replace(target,'')
  webview0b.load_html(wk_html)

  #展示ビューの表示
  wk_html = base_html.tenji_html

  #基本情報の転記
  wk_sql = base_sql.race_table_sql3
  target = '@yyyymmdd'; wk_sql = wk_sql.replace(target, in_yyyymmdd)
  target = '@poolcode'; wk_sql = wk_sql.replace(target, in_poolcode)
  target = '@raceno'; wk_sql = wk_sql.replace(target, in_raceno)
  conn = sqlite3.connect(dbname)
  cur = conn.execute(wk_sql)
  rows = cur.fetchall()
  n = 0
  for row in rows:
    n = n + 1
    target = '@選手情報' + str(n); wk_html = wk_html.replace(target,str(row[0]))
    target = '@能力' + str(n); wk_html = wk_html.replace(target,str(row[1]))
    target = '@直近能力' + str(n); wk_html = wk_html.replace(target,str(row[2]))
    target = '@直近ＳＴ' + str(n); wk_html = wk_html.replace(target,str(row[3]))
    target = '@Ｍ能力' + str(n); wk_html = wk_html.replace(target,str(row[4]))

  #得票率の転記
  focus_list = []
  focus_list.append('1-2-3'); focus_list.append('2-1-3'); focus_list.append('3-1-2'); focus_list.append('4-1-2'); focus_list.append('5-1-2'); focus_list.append('6-1-2')
  focus_list.append('1-2-4'); focus_list.append('2-1-4'); focus_list.append('3-1-4'); focus_list.append('4-1-3'); focus_list.append('5-1-3'); focus_list.append('6-1-3')
  focus_list.append('1-2-5'); focus_list.append('2-1-5'); focus_list.append('3-1-5'); focus_list.append('4-1-5'); focus_list.append('5-1-4'); focus_list.append('6-1-4')
  focus_list.append('1-2-6'); focus_list.append('2-1-6'); focus_list.append('3-1-6'); focus_list.append('4-1-6'); focus_list.append('5-1-6'); focus_list.append('6-1-5')
  focus_list.append('1-3-2'); focus_list.append('2-3-1'); focus_list.append('3-2-1'); focus_list.append('4-2-1'); focus_list.append('5-2-1'); focus_list.append('6-2-1')
  focus_list.append('1-3-4'); focus_list.append('2-3-4'); focus_list.append('3-2-4'); focus_list.append('4-2-3'); focus_list.append('5-2-3'); focus_list.append('6-2-3')
  focus_list.append('1-3-5'); focus_list.append('2-3-5'); focus_list.append('3-2-5'); focus_list.append('4-2-5'); focus_list.append('5-2-4'); focus_list.append('6-2-4')
  focus_list.append('1-3-6'); focus_list.append('2-3-6'); focus_list.append('3-2-6'); focus_list.append('4-2-6'); focus_list.append('5-2-6'); focus_list.append('6-2-5')
  focus_list.append('1-4-2'); focus_list.append('2-4-1'); focus_list.append('3-4-1'); focus_list.append('4-3-1'); focus_list.append('5-3-1'); focus_list.append('6-3-1')
  focus_list.append('1-4-3'); focus_list.append('2-4-3'); focus_list.append('3-4-2'); focus_list.append('4-3-2'); focus_list.append('5-3-2'); focus_list.append('6-3-2')
  focus_list.append('1-4-5'); focus_list.append('2-4-5'); focus_list.append('3-4-5'); focus_list.append('4-3-5'); focus_list.append('5-3-4'); focus_list.append('6-3-4')
  focus_list.append('1-4-6'); focus_list.append('2-4-6'); focus_list.append('3-4-6'); focus_list.append('4-3-6'); focus_list.append('5-3-6'); focus_list.append('6-3-5')
  focus_list.append('1-5-2'); focus_list.append('2-5-1'); focus_list.append('3-5-1'); focus_list.append('4-5-1'); focus_list.append('5-4-1'); focus_list.append('6-4-1')
  focus_list.append('1-5-3'); focus_list.append('2-5-3'); focus_list.append('3-5-2'); focus_list.append('4-5-2'); focus_list.append('5-4-2'); focus_list.append('6-4-2')
  focus_list.append('1-5-4'); focus_list.append('2-5-4'); focus_list.append('3-5-4'); focus_list.append('4-5-3'); focus_list.append('5-4-3'); focus_list.append('6-4-3')
  focus_list.append('1-5-6'); focus_list.append('2-5-6'); focus_list.append('3-5-6'); focus_list.append('4-5-6'); focus_list.append('5-4-6'); focus_list.append('6-4-5')
  focus_list.append('1-6-2'); focus_list.append('2-6-1'); focus_list.append('3-6-1'); focus_list.append('4-6-1'); focus_list.append('5-6-1'); focus_list.append('6-5-1')
  focus_list.append('1-6-3'); focus_list.append('2-6-3'); focus_list.append('3-6-2'); focus_list.append('4-6-2'); focus_list.append('5-6-2'); focus_list.append('6-5-2')
  focus_list.append('1-6-4'); focus_list.append('2-6-4'); focus_list.append('3-6-4'); focus_list.append('4-6-3'); focus_list.append('5-6-3'); focus_list.append('6-5-3')
  focus_list.append('1-6-5'); focus_list.append('2-6-5'); focus_list.append('3-6-5'); focus_list.append('4-6-5'); focus_list.append('5-6-4'); focus_list.append('6-5-4') 

  wk_url = 'https://www.boatrace.jp/owpc/pc/race/odds3t?rno=@raceno&jcd=@poolcode&hd=@yyyymmdd'
  target = '@raceno';   wk_url = wk_url.replace(target, str(int(in_raceno)))
  target = '@poolcode'; wk_url = wk_url.replace(target, in_poolcode)
  target = '@yyyymmdd'; wk_url = wk_url.replace(target, in_yyyymmdd)
  
  flg = 0
  r = requests.get(wk_url)
  html = r.text
  if 'データがありません。' in html:
      flg = 1
  if 'レース中止' in html:
      flg = 1
  if '※ 該当レースは中止になりました。' in html:
      flg = 1
  if flg == 0:
      t1 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
      t2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
      t3 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
      soup = BeautifulSoup(html, 'html.parser')
      base_count = 0
      for tag1 in soup.find_all('td', class_='oddsPoint'):
          #オッズの抽出
          wk_arry = str(tag1).split('>')
          wk_arry = str(wk_arry[1]).split('<')
          t_odds_odds = str(wk_arry[0]).strip()
          #組番の抽出
          t_odds_focus  = focus_list[base_count]
          if t_odds_odds != '欠場':
              i1 = int(t_odds_focus[0])
              i2 = int(t_odds_focus[2])
              i3 = int(t_odds_focus[4])
              wk =  (1.0 / float(t_odds_odds)); t1[i1] = t1[i1] + wk; t1[0] = t1[0] + wk
              wk =  (1.0 / float(t_odds_odds)); t2[i2] = t2[i2] + wk; t2[0] = t2[0] + wk
              wk =  (1.0 / float(t_odds_odds)); t3[i3] = t3[i3] + wk; t3[0] = t3[0] + wk
          #カウンターをインクリメント
          base_count = base_count + 1
      #得票率の算出
      n = 0
      for i in range(6):
          n = n + 1
          if t1[0] != 0.0 and t2[0] != 0.0 and t3[0] != 0.0:
              ans1 = '%5.2f' % ((t1[n] / t1[0]) * 100.0)
              ans2 = '%5.2f' % ((t2[n] / t2[0]) * 100.0)
              ans3 = '%5.2f' % ((t3[n] / t3[0]) * 100.0)
              target = '@得票率１着' + str(n); wk_html = wk_html.replace(target, ans1)
              target = '@得票率２着' + str(n); wk_html = wk_html.replace(target, ans2)
              target = '@得票率３着' + str(n); wk_html = wk_html.replace(target, ans3)
                
  #展示情報の転記
  rehearsal_time  = ['', '', '', '', '', '', '']
  tilt            = ['', '', '', '', '', '', '']
  start_course    = ['', '', '', '', '', '', '']
  start_time      = ['', '', '', '', '', '', '']
  parts           = ['', '', '', '', '', '', '']


  wk_url = 'https://www.boatrace.jp/owpc/pc/race/beforeinfo?rno=@raceno&jcd=@poolcode&hd=@yyyymmdd'
  target = '@raceno';   wk_url = wk_url.replace(target, str(int(in_raceno)))
  target = '@poolcode'; wk_url = wk_url.replace(target, in_poolcode)
  target = '@yyyymmdd'; wk_url = wk_url.replace(target, in_yyyymmdd)
  r = requests.get(wk_url)
  html = r.text
  soup = BeautifulSoup(html, 'html.parser')
  if 'データがありません。' in html:
    flg = 1
  #展示タイムが一つも無い場合は直前情報は出力しない
  if flg == 0:
    rtime = ''
    rtime_count = 0
    base_count = 0
    for tag1 in soup.find_all('tbody'):
        if 'is-fs12' in str(tag1):
            base_count = base_count + 1
            n = 0
            for tag2 in str(tag1).splitlines():
                n =  n + 1
                if n == 7:
                    rtime = ''
                    wk_arry = str(tag2).strip().split('>')
                    rtime = str(wk_arry[1]).replace('</td','')
                    break
            if rtime != ' ':
                rtime_count = rtime_count + 1
    if rtime_count == 0:
        flg = 1
  #部品交換情報の取得
  if flg == 0:
    base_count = 0
    for tag1 in soup.find_all('tbody'):
        if 'is-fs12' in str(tag1):
            base_count = base_count + 1
            parts_flg = 0
            parts_list = ''
            n = 0
            for tag2 in str(tag1).splitlines():
                n = n + 1
                if  n == 9 and ('新' in str(tag2)):
                    if parts_flg  == 0:
                        parts_list = 'ペラ'; parts_flg = 1
                    else:
                        parts_list = parts_list + '・' + 'ペラ'
                if 'label4 is-type1' in str(tag2):
                    wk_arry = str(tag2).split('>')
                    wk_arry = str(wk_arry[2]).split('<')
                    wk = str(wk_arry[0]).strip()
                    if parts_flg  == 0:
                        parts_list = wk; parts_flg = 1
                    else:
                        parts_list = parts_list + '・' + wk      
            if parts_flg == 0:
                parts[base_count] = '　            　　　　'
            else:
                parts[base_count] = parts_list
  #直前情報の取得
  if flg == 0:
    base_count = 0
    for tag1 in soup.find_all('tbody'):
        if 'is-fs12' in str(tag1):
            base_count = base_count + 1
            #選手単位の明細項目の抽出(展示タイム)
            n = 0
            for tag2 in str(tag1).splitlines():
                n =  n + 1
                if n == 7:
                    wk_arry = str(tag2).strip().split('>')
                    rehearsal_time[base_count] = str(wk_arry[1]).replace('</td','')
                    break 
            #選手単位の明細項目の抽出(チルト)
            n = 0
            for tag2 in str(tag1).splitlines():
                n =  n + 1
                if n == 8:
                    wk_arry = str(tag2).strip().split('>')
                    tilt[base_count] = str(wk_arry[1]).replace('</td','')
                    break 
            
            #選手単位の明細項目の抽出(スタート展示コース)
            n = 0
            for tag2 in soup.find_all('span'):
                if 'table1_boatImage1Number' in str(tag2):
                    n = n + 1
                    wk_arry = str(tag2).strip().split('>')
                    wk_str = str(wk_arry[1]).replace('</span','')
                    if str(base_count) == wk_str:
                        start_course[base_count] = str(n)
                        break
            #選手単位の明細項目の抽出(フライング区分_スタート展示タイム)
            n = 0
            for tag2 in soup.find_all('span'):
                if 'table1_boatImage1Time' in str(tag2):
                    n = n + 1
                    wk_arry = str(tag2).strip().split('>')
                    wk_str = str(wk_arry[1]).replace('</span','')
                    if str(start_course[base_count]) == str(n):
                            start_time[base_count] = wk_str
                            break
  #直前情報と部品交換情報を転記
  if flg == 0:
    n = 0
    for i in range(6):
      n = n + 1
      target = '@展示時計' + str(n); wk_html = wk_html.replace(target, rehearsal_time[n])
      target = '@チルト' + str(n); wk_html = wk_html.replace(target, tilt[n])
      target = '@進入' + str(n); wk_html = wk_html.replace(target, start_course[n])
      target = '@ＳＴ' + str(n); wk_html = wk_html.replace(target, start_time[n])
      target = '@交換部品' + str(n); wk_html = wk_html.replace(target, parts[n])

  #展開指数の転記
  if flg == 0:
    wk_sql = base_sql.race_table_sql3
    target = '@yyyymmdd'; wk_sql = wk_sql.replace(target, in_yyyymmdd)
    target = '@poolcode'; wk_sql = wk_sql.replace(target, in_poolcode)
    target = '@raceno'; wk_sql = wk_sql.replace(target, in_raceno)
    conn = sqlite3.connect(dbname)
    cur = conn.execute(wk_sql)
    rows = cur.fetchall()
    n = 0
    for row in rows:
      n = n + 1
      if  start_course[n] == '1':
          target = '@進入別能力' + str(n);        wk_html = wk_html.replace(target,str(row[5]))
          target = '@進入別Ｍ能力' + str(n);      wk_html = wk_html.replace(target,str(row[25]))
          target = '@逃げ逃がし率' + str(n);      wk_html = wk_html.replace(target,str(row[11]))
          target = '@まくりまくられ率' + str(n);  wk_html = wk_html.replace(target,str(row[12]))
          target = '@差され差し率' + str(n);      wk_html = wk_html.replace(target,str(row[13]))
      if  start_course[n] == '2':
          target = '@進入別能力' + str(n);        wk_html = wk_html.replace(target,str(row[6]))
          target = '@進入別Ｍ能力' + str(n);      wk_html = wk_html.replace(target,str(row[26]))
          target = '@逃げ逃がし率' + str(n);      wk_html = wk_html.replace(target,str(row[14]))
          target = '@まくりまくられ率' + str(n);  wk_html = wk_html.replace(target,str(row[15]))
          target = '@差され差し率' + str(n);      wk_html = wk_html.replace(target,str(row[16]))   
      if  start_course[n] == '3':
          target = '@進入別能力' + str(n);        wk_html = wk_html.replace(target,str(row[7]))
          target = '@進入別Ｍ能力' + str(n);      wk_html = wk_html.replace(target,str(row[27]))
          target = '@まくりまくられ率' + str(n);  wk_html = wk_html.replace(target,str(row[17]))
          target = '@差され差し率' + str(n);      wk_html = wk_html.replace(target,str(row[18])) 
      if  start_course[n] == '4':
          target = '@進入別能力' + str(n);        wk_html = wk_html.replace(target,str(row[8]))
          target = '@進入別Ｍ能力' + str(n);      wk_html = wk_html.replace(target,str(row[28]))
          target = '@まくりまくられ率' + str(n);  wk_html = wk_html.replace(target,str(row[19]))
          target = '@差され差し率' + str(n);      wk_html = wk_html.replace(target,str(row[20]))   
      if  start_course[n] == '5':
          target = '@進入別能力' + str(n);        wk_html = wk_html.replace(target,str(row[9]))
          target = '@進入別Ｍ能力' + str(n);      wk_html = wk_html.replace(target,str(row[29]))
          target = '@まくりまくられ率' + str(n);  wk_html = wk_html.replace(target,str(row[21]))
          target = '@差され差し率' + str(n);      wk_html = wk_html.replace(target,str(row[22])) 
      if  start_course[n] == '6':
          target = '@進入別能力' + str(n);        wk_html = wk_html.replace(target,str(row[10]))
          target = '@進入別Ｍ能力' + str(n);      wk_html = wk_html.replace(target,str(row[30]))
          target = '@まくりまくられ率' + str(n);  wk_html = wk_html.replace(target,str(row[23]))
          target = '@差され差し率' + str(n);      wk_html = wk_html.replace(target,str(row[24])) 
           
  #オリジナル展示データの転記
  if flg == 0 and (in_poolcode == '10' or in_poolcode == '13' or in_poolcode == '15' or in_poolcode == '21' or in_poolcode == '23'):
    html = r.text
    r = ''
    time_pos1 = 0; time_pos2 = 0; time_pos3 = 0
    t1 = ['', '', '', '', '', '', '']
    t2 = ['', '', '', '', '', '', '']
    t3 = ['', '', '', '', '', '', '']
    if in_poolcode == '10':
      r = requests.get('http://www.boatrace-mikuni.jp/modules/yosou/group-cyokuzen.php?day=20210224&race=12&if=1&kind=2')
      time_pos1 = 7; time_pos2 = 8; time_pos3 = 9
    if in_poolcode == '13':
      r = requests.get('https://www.boatrace-amagasaki.jp/modules/yosou/group-cyokuzen.php?day=20210224&race=4&if=1&kind=2')
      time_pos1 = 8; time_pos2 = 9; time_pos3 = 10 #直線タイムはない
    if in_poolcode == '15':
      r = requests.get('https://www.marugameboat.jp/modules/yosou/group-cyokuzen.php?day=20210224&race=4&if=1&kind=2')
      time_pos1 = 8; time_pos2 = 9; time_pos3 = 10
    if in_poolcode == '21':
      r = requests.get('https://www.boatrace-ashiya.com/modules/yosou/group-cyokuzen.php?day=20210224&race=1&if=1&kind=2')
      time_pos1 = 8; time_pos2 = 9; time_pos3 = 10
    if in_poolcode == '23':
      r = requests.get('https://www.boatrace-karatsu.jp/modules/yosou/group-cyokuzen.php?day=20210224&race=1&if=1&kind=2')
      time_pos1 = 7; time_pos2 = 8; time_pos3 = 9
    if 'Information' in html:
      flg = 1
    if flg == 0:
      html = r.text
      soup = BeautifulSoup(html, 'html.parser')
      base_count = 0
      for tag1 in soup.find_all('tr',class_=['odd', 'even', 'line_position']):
        n = 0
        for tag2 in str(tag1).splitlines():
            n = n + 1
            #一周
            if n == time_pos1:
                base_count = base_count + 1
                wk_arry = str(tag2).strip().split('>')
                t1[base_count] = str(wk_arry[1]).replace('</td','')
            #まわり足
            if n == time_pos2:
                wk_arry = str(tag2).strip().split('>')
                t2[base_count] = str(wk_arry[1]).replace('</td','')
            #直線
            if n == time_pos3:
                wk_arry = str(tag2).strip().split('>')
                t3[base_count] = str(wk_arry[1]).replace('</td','')
      n = 0
      for i in range(6):
        n = n + 1
        target = '@一周' + str(n); wk_html = wk_html.replace(target,t1[n])
        target = '@まわり足' + str(n); wk_html = wk_html.replace(target,t2[n])
        target = '@直線' + str(n); wk_html = wk_html.replace(target,t3[n])

  #展示の未記入箇所のクリア  
  n = 0
  for i in range(6):
    n = n + 1
    target = '@選手情報' + str(n); wk_html = wk_html.replace(target,'')
    target = '@能力' + str(n); wk_html = wk_html.replace(target,'')
    target = '@直近能力' + str(n); wk_html = wk_html.replace(target,'')
    target = '@Ｍ能力' + str(n); wk_html = wk_html.replace(target,'')
    target = '@得票率１着' + str(n); wk_html = wk_html.replace(target,'')
    target = '@得票率２着' + str(n); wk_html = wk_html.replace(target,'')
    target = '@得票率３着' + str(n); wk_html = wk_html.replace(target,'')
    target = '@展示時計' + str(n); wk_html = wk_html.replace(target,'')
    target = '@チルト' + str(n); wk_html = wk_html.replace(target,'')
    target = '@進入' + str(n); wk_html = wk_html.replace(target,'')
    target = '@ＳＴ' + str(n); wk_html = wk_html.replace(target,'')
    target = '@一周' + str(n); wk_html = wk_html.replace(target,'')
    target = '@まわり足' + str(n); wk_html = wk_html.replace(target,'')
    target = '@直線' + str(n); wk_html = wk_html.replace(target,'')
    target = '@進入' + str(n); wk_html = wk_html.replace(target,'')
    target = '@進入別能力' + str(n); wk_html = wk_html.replace(target,'')
    target = '@進入別Ｍ能力' + str(n); wk_html = wk_html.replace(target,'')
    target = '@逃げ逃がし率' + str(n); wk_html = wk_html.replace(target,'')
    target = '@まくりまくられ率' + str(n); wk_html = wk_html.replace(target,'')
    target = '@差され差し率' + str(n); wk_html = wk_html.replace(target,'')
    target = '@交換部品' + str(n); wk_html = wk_html.replace(target,'')

  webview0c.load_html(wk_html)
  view01.close() #出走表選択ビューを閉じる

"""
【関　数】button011_action
【引　数】なし
【戻り値】なし
【機　能】出走表選択ビューの取消ボタン押下処理
"""
def button011_action(sender):
  global in_yyyymmdd
  global in_poolcode
  global in_raceno
  global old_yyyymmdd
  global old_poolcode
  global old_raceno
  in_yyyymmdd = old_yyyymmdd
  in_poolcode = old_poolcode
  in_raceno   = old_raceno
  view01.close() #出走表選択ビューを閉じる

"""
【関　数】button03_action
【引　数】なし
【戻り値】なし
【機　能】選手戦歴ビューの表示
"""
def button03_action(sender):
  global in_yyyymmdd
  global in_poolcode
  global in_raceno
  player_list.clear()
  #選手テーブルリストの表示
  view03.name = '選手個別情報 -' + main_view.name + '-'
	#選択された日付と場コードとレース番号で選手一覧を検索するSQLを生成
  wk_sql  = base_sql.player_list_sql
  target = '@yyyymmdd'; wk_sql = wk_sql.replace(target, in_yyyymmdd)
  target = '@poolcode'; wk_sql = wk_sql.replace(target, in_poolcode)
  target = '@raceno'; wk_sql = wk_sql.replace(target, in_raceno)
	#SQLを実行して結果をリストに格納
  conn = sqlite3.connect(dbname)
  cur = conn.cursor()
  for row in cur.execute(wk_sql):
	  player_list.append(row[0] + '号艇 ' + row[1] + ' ' + row[2] + '[' + row[3] + '] ' + row[4] + '支部　モーターNo.' + row[5]  )
  cur.close()
  conn.close()
  tableview032_listdata = ui.ListDataSource('')
  tableview032_listdata.items = player_list
  tableview032.delegate = tableview032.data_source = tableview032_listdata
  tableview032_listdata.action = tableview032_action #選手リストの選択処理
  tableview032.reload_data()
  webview033.load_html(base_html.clear_html)
  view03.present('popover')

"""
【関　数】tableview032_action
【引　数】なし
【戻り値】なし
【機　能】選手名選択リストの選択時の処理
"""
def tableview032_action(sender):
  global in_playerno
  global in_motorno
  in_playerno = ''
  in_motorno = ''
  sel = sender.selected_row
  wk_arry = player_list[sel].split('[')
  wk_arry = wk_arry[0].split(' ')
  in_playerno = wk_arry[1]
  wk_arry = player_list[sel].split('.')
  in_motorno = wk_arry[1]
  #選手の戦歴を検索して、htmlを作成する。
  wk_detail = ''
  wk_sql = base_sql.player_history_sql
  target = '@playerno'; wk_sql = wk_sql.replace(target, in_playerno)
  conn = sqlite3.connect(dbname)
  cur = conn.execute(wk_sql)
  names = [description[0] for description in cur.description]
  rows = cur.fetchall()
  #HTMLテーブルのヘッダ行の生成
  wk_detail = wk_detail + '<tr>'
  n = 0
  for name in names:
    n = n + 1
    if n == 1:
      #ヘッダの一番左の項目を固定
      wk_detail = wk_detail + '<th class="fixed01 text-center">' + name + '</th>' 
    else:
      #ヘッダ行を固定
      wk_detail = wk_detail + '<th class="fixed02 text-center">' + name + '</th>' 
  wk_detail = wk_detail + '</tr>'
  #HTMLテーブルの明細行の生成
  for row in rows:
    n = 0
    wk_detail = wk_detail + '<tr>'
    for i in range(len(row)):
      n = n + 1
      if n == 1:
        #明細行の一番左の項目を固定
        wk_detail = wk_detail + '<th class="fixed02 text-left">' + str(row[i]) + '</th>' 
      else:
        #明細行の生成
        wk_detail = wk_detail + '<td class="text-right">' + str(row[i]) + '</td>' 
    wk_detail = wk_detail + '</tr>'
  cur.close()
  conn.close()
  #生成したHTMLファイルを画面表示
  wk_html = base_html.player_history_html
  if wk_detail != '':
    target = '@detail'; wk_html = wk_html.replace(target,wk_detail)
  else:
    target = '@detail'; wk_html = wk_html.replace(target,'')
  webview033.load_html(wk_html)

"""
【関　数】button031_action
【引　数】なし
【戻り値】なし
【機　能】選手情報ビューのクローズ
"""
def button031_action(sender):
  view03.close()

"""
【関　数】button032_action
【引　数】なし
【戻り値】なし
【機　能】選手情報ビュー 選手戦歴ボタンの押下時の処理
"""
def  button032_action(sender):
  global in_playerno
  if in_playerno != '':
    #選手の戦歴を検索して、htmlを作成する。
    wk_detail = ''
    wk_sql = base_sql.player_history_sql
    target = '@playerno'; wk_sql = wk_sql.replace(target, in_playerno)
    conn = sqlite3.connect(dbname)
    cur = conn.execute(wk_sql)
    names = [description[0] for description in cur.description]
    rows = cur.fetchall()
    #HTMLテーブルのヘッダ行の生成
    wk_detail = wk_detail + '<tr>'
    n = 0
    for name in names:
      n = n + 1
      if n == 1:
        #ヘッダの一番左の項目を固定
        wk_detail = wk_detail + '<th class="fixed01 text-center">' + name + '</th>' 
      else:
        #ヘッダ行を固定
        wk_detail = wk_detail + '<th class="fixed02 text-center">' + name + '</th>' 
    wk_detail = wk_detail + '</tr>'
    #HTMLテーブルの明細行の生成
    for row in rows:
      n = 0
      wk_detail = wk_detail + '<tr>'
      for i in range(len(row)):
        n = n + 1
        if n == 1:
          #明細行の一番左の項目を固定
          wk_detail = wk_detail + '<th class="fixed02 text-left">' + str(row[i]) + '</th>' 
        else:
          #明細行の生成
          wk_detail = wk_detail + '<td class="text-right">' + str(row[i]) + '</td>' 
      wk_detail = wk_detail + '</tr>'
    cur.close()
    conn.close()
    #生成したHTMLファイルを画面表示
    wk_html = base_html.player_history_html
    if wk_detail != '':
      target = '@detail'; wk_html = wk_html.replace(target,wk_detail)
    else:
      target = '@detail'; wk_html = wk_html.replace(target,'')
    webview033.load_html(wk_html)

"""
【関　数】button033_action
【引　数】なし
【戻り値】なし
【機　能】選手個別情報ビュー モータ戦歴ボタンの押下時の処理
"""
def  button033_action(sender):
  global in_motorno
  global in_poolcode
  if in_poolcode != '' and in_motorno != '':
    #最新のモーター交換日付を取得する
    wk_new_motorno_yyyymmdd = ''
    wk_sql = base_sql.new_motor_sql
    target = '@poolcode'; wk_sql = wk_sql.replace(target, in_poolcode)
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    for row in cur.execute(wk_sql):
      wk_new_motorno_yyyymmdd = str(row[0])
    cur.close()
    conn.close()
		#モーター戦歴を検索して、htmlを作成する。
    wk_detail = ''
    wk_sql = base_sql.motor_history_sql
    target = '@new_motor_yyyymmdd'; wk_sql = wk_sql.replace(target, wk_new_motorno_yyyymmdd)
    target = '@poolcode'; wk_sql = wk_sql.replace(target, in_poolcode)
    target = '@motorno'; wk_sql = wk_sql.replace(target, in_motorno)
    conn = sqlite3.connect(dbname)
    cur = conn.execute(wk_sql)
    names = [description[0] for description in cur.description]
    rows = cur.fetchall()
    #HTMLテーブルのヘッダ行の生成
    wk_detail = wk_detail + '<tr>'
    n = 0
    for name in names:
      n = n + 1
      if n == 1:
				#ヘッダの一番左の項目を固定
        wk_detail = wk_detail + '<th class="fixed01 text-center">' + name + '</th>' 
      else:
        #ヘッダ行を固定
        wk_detail = wk_detail + '<th class="fixed02 text-center">' + name + '</th>' 
    wk_detail = wk_detail + '</tr>'
		#HTMLテーブルの明細行の生成
    for row in rows:
      n = 0
      wk_detail = wk_detail + '<tr>'
      for i in range(len(row)):
        n = n + 1
        if n == 1:
          #明細行の一番左の項目を固定
          wk_detail = wk_detail + '<th class="fixed02 text-left">' + str(row[i]) + '</th>' 
        else:
          #明細行の生成
          wk_detail = wk_detail + '<td class="text-right">' + str(row[i]) + '</td>' 
      wk_detail = wk_detail + '</tr>'
    cur.close()
    conn.close()
		#生成したHTMLファイルを画面表示
    wk_html = base_html.player_history_html
    if wk_detail != '':
      target = '@detail'; wk_html = wk_html.replace(target,wk_detail)
    else:
      target = '@detail'; wk_html = wk_html.replace(target,'')
    webview033.load_html(wk_html)

"""
【関　数】button034_action
【引　数】なし
【戻り値】なし
【機　能】選手個別情報ビュー 部品交換履ボタンの押下時の処理
"""
def  button034_action(sender):
  global in_motorno
  global in_poolcode
  if in_poolcode != '' and in_motorno != '':
    #最新のモーター交換日付を取得する
    wk_new_motorno_yyyymmdd = ''
    wk_sql = base_sql.new_motor_sql
    target = '@poolcode'; wk_sql = wk_sql.replace(target, in_poolcode)
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    for row in cur.execute(wk_sql):
      wk_new_motorno_yyyymmdd = str(row[0])
    cur.close()
    conn.close()
    #部品交換履歴を検索して、htmlを作成する。
    wk_detail = ''
    wk_sql = base_sql.parts_history_sql
    target = '@new_motor_yyyymmdd'; wk_sql = wk_sql.replace(target, wk_new_motorno_yyyymmdd)
    target = '@poolcode'; wk_sql = wk_sql.replace(target, in_poolcode)
    target = '@motorno'; wk_sql = wk_sql.replace(target, in_motorno)
    conn = sqlite3.connect(dbname)
    cur = conn.execute(wk_sql)
    names = [description[0] for description in cur.description]
    rows = cur.fetchall()
    #HTMLテーブルのヘッダ行の生成
    wk_detail = wk_detail + '<tr>'
    n = 0
    for name in names:
      n = n + 1
      if n == 1:
        #ヘッダの一番左の項目を固定
        wk_detail = wk_detail + '<th class="fixed01 text-center">' + name + '</th>' 
      else:
        #ヘッダ行を固定
        wk_detail = wk_detail + '<th class="fixed02 text-center">' + name + '</th>' 
    wk_detail = wk_detail + '</tr>'
    #HTMLテーブルの明細行の生成
    wk_detail = wk_detail + '<tr>'
    for row in rows:
      n = 0
      wk_detail = wk_detail + '<tr>'
      for i in range(len(row)):
        n = n + 1
        if n == 1:
          #明細行の一番左の項目を固定
          wk_detail = wk_detail + '<th class="fixed02 text-left">' + str(row[i]) + '</th>' 
        else:
          #明細行の生成
          wk_detail = wk_detail + '<td class="text-right">' + str(row[i]) + '</td>' 
      wk_detail = wk_detail + '</tr>'
    cur.close()
    conn.close()
    #生成したHTMLファイルを画面表示
    wk_html = base_html.player_history_html
    if wk_detail != '':
      target = '@detail'; wk_html = wk_html.replace(target,wk_detail)
    else:
      target = '@detail'; wk_html = wk_html.replace(target,'')
    webview033.load_html(wk_html)


"""
【関　数】button04_action
【引　数】なし
【戻り値】なし
【機　能】twitter検索ビューの表示
"""
def button04_action(sender):
  global in_yyyymmdd
  global in_poolcode
  global in_raceno
  player_list.clear()
  #選手テーブルリストの表示
  view04.name = 'twitterでの選手情報検索 -' + main_view.name + '-'
	#選択された日付と場コードとレース番号で選手一覧を検索するSQLを生成
  wk_sql  = base_sql.player_list_sql
  target = '@yyyymmdd'; wk_sql = wk_sql.replace(target, in_yyyymmdd)
  target = '@poolcode'; wk_sql = wk_sql.replace(target, in_poolcode)
  target = '@raceno'; wk_sql = wk_sql.replace(target, in_raceno)
	#SQLを実行して結果をリストに格納
  conn = sqlite3.connect(dbname)
  cur = conn.cursor()
  for row in cur.execute(wk_sql):
	  player_list.append(row[0] + '号艇 ' + row[1] + ' ' + row[2] + '[' + row[3] + '] ' + row[4] + '支部　モーターNo.' + row[5]  )
  cur.close()
  conn.close()
  tableview042_listdata = ui.ListDataSource('')
  tableview042_listdata.items = player_list
  tableview042.delegate = tableview042.data_source = tableview042_listdata
  tableview042_listdata.action = tableview042_action #選手リストの選択処理
  tableview042.reload_data()
  webview043.load_html(base_html.clear_html)
  view04.present('popover')

"""
【関　数】tableview042_action
【引　数】なし
【戻り値】なし
【機　能】twitter検索ビューの選手名選択リストの選択時の処理
"""
def tableview042_action(sender):
  sel = sender.selected_row
  wk_arry = player_list[sel].split('[')
  wk_arry = wk_arry[0].split(' ')
  in_playername = wk_arry[2]
  wk_url = 'https://twitter.com/search?q=@playername&f=live'
  wk_player_name = urllib.parse.quote(in_playername)
  wk_url = wk_url.replace('@playername', wk_player_name)
  webview043.load_url(wk_url)

"""
【関　数】button041_action
【引　数】なし
【戻り値】なし
【機　能】twitter検索ビューのクローズ
"""
def button041_action(sender):
  view04.close()


"""
【関　数】button05_action
【引　数】なし
【戻り値】なし
【機　能】投票ビューの表示
"""
def button05_action(sender):
  webview052.load_url('https://spweb.brtb.jp/')
  view05.present('popover')

"""
【関　数】button051_action
【引　数】なし
【戻り値】なし
【機　能】投票ビューのクローズ
"""
def button051_action(sender):
  view05.close()

"""
【関　数】button06_action
【引　数】なし
【戻り値】なし
【機　能】レース結果ビューの表示
"""
def button06_action(sender):
  global in_yyyymmdd
  global in_poolcode
  global in_raceno
  if in_yyyymmdd !='' and in_poolcode != '' and in_raceno != '':
    view06.name = 'レース結果 -' + main_view.name + '-'
    wk_url = 'https://www.boatrace.jp/owpc/pc/race/raceresult?rno=@raceno&jcd=@poolcode&hd=@yyyymmdd'
    target = '@raceno';   wk_url = wk_url.replace(target, str(int(in_raceno)))
    target = '@poolcode'; wk_url = wk_url.replace(target, in_poolcode)
    target = '@yyyymmdd'; wk_url = wk_url.replace(target, in_yyyymmdd)
    webview062.load_url(wk_url)
    view06.present('popover')

"""
【関　数】button051_action
【引　数】なし
【戻り値】なし
【機　能】レース結果ビューのクローズ
"""
def button061_action(sender):
  view06.close()


"""
【関　数】button07_action
【引　数】なし
【戻り値】なし
【機　能】データー検索ビューの表示
"""
def button07_action(sender):
  global in_yyyymmdd
  global in_poolcode
  global in_raceno
  in_path = './sql'
  for item in os.listdir(path=in_path):
      if '.sql' in item:
        sql_list.append(item)
  tableview072_listdata = ui.ListDataSource('')
  tableview072_listdata.items = sql_list
  tableview072.delegate = tableview072.data_source = tableview072_listdata
  tableview072_listdata.action = tableview072_action #SQL一覧の表示
  tableview072.reload_data()


  webview073.load_html(base_html.clear_html)
  view07.present('popover')

"""
【関　数】button071_action
【引　数】なし
【戻り値】なし
【機　能】データ検索ビューのクローズ
"""
def button071_action(sender):
  view07.close()

"""
【関　数】tableview072_action
【引　数】なし
【戻り値】なし
【機　能】データ検索ビューでSQLを選択したときの処理
"""
def  tableview072_action(sender):
  global in_yyyymmdd
  global in_poolcode
  if in_yyyymmdd != '' and in_poolcode != '':
    sel = sender.selected_row
    in_file = str(os.getcwd())
    in_file = in_file + '/sql/' + sql_list[sel]
    fb = open(in_file, 'r', encoding='utf-8')
    wk_sql = fb.read()
    fb.close()
    wk_detail = ''
    wk_sql = str(wk_sql)
    target = '@yyyymmdd'; wk_sql = wk_sql.replace(target, in_yyyymmdd)
    conn = sqlite3.connect(dbname)
    cur = conn.execute(wk_sql)
    names = [description[0] for description in cur.description]
    rows = cur.fetchall()
    #HTMLテーブルのヘッダ行の生成
    wk_detail = wk_detail + '<tr>'
    n = 0
    for name in names:
      n = n + 1
      if n == 1:
        #ヘッダの一番左の項目を固定
        wk_detail = wk_detail + '<th class="fixed01 text-center">' + name + '</th>' 
      else:
        #ヘッダ行を固定
        wk_detail = wk_detail + '<th class="fixed02 text-center">' + name + '</th>' 
    wk_detail = wk_detail + '</tr>'
    #HTMLテーブルの明細行の生成
    wk_detail = wk_detail + '<tr>'
    for row in rows:
      n = 0
      wk_detail = wk_detail + '<tr>'
      for i in range(len(row)):
        n = n + 1
        if n == 1:
          #明細行の一番左の項目を固定
          wk_detail = wk_detail + '<th class="fixed02 text-left">' + str(row[i]) + '</th>' 
        else:
          #明細行の生成
          wk_detail = wk_detail + '<td class="text-right">' + str(row[i]) + '</td>' 
      wk_detail = wk_detail + '</tr>'
    cur.close()
    conn.close()
    #生成したHTMLファイルを画面表示
    wk_html = base_html.data_html
    if wk_detail != '':
      target = '@detail'; wk_html = wk_html.replace(target,wk_detail)
    else:
      target = '@detail'; wk_html = wk_html.replace(target,'')
    webview073.load_html(wk_html)

"""
【関　数】main
【引　数】なし
【戻り値】なし
【機　能】1.メインビューの定義
          7.投票画面
"""
#1.メインビューの定義
main_view = ui.View(frame=(0, 0, 768, 1024))
main_view.name = 'BOAT RACE Dash Board'
main_view.background_color = ('white')
#出走表ボタン
button01 = ui.Button()
button01.frame = (5, 5, 80, 50)
button01.title = '出走表選択'
button01.border_color = ('brack')
button01.border_width = 1
button01.action = button01_action
main_view.add_subview(button01)

#選手戦歴・モータ戦歴・部品交換歴ボタン
button03 = ui.Button()
button03.frame = (175, 5, 200, 50)
button03.title = '選手歴・モータ歴・部品歴'
button03.border_color = ('brack')
button03.border_width = 1
button03.action = button03_action
main_view.add_subview(button03)

#twitter検索ボタン
button04 = ui.Button()
button04.frame = (380, 5, 80, 50)
button04.title = 'twitter'
button04.border_color = ('brack')
button04.border_width = 1
button04.action = button04_action
main_view.add_subview(button04)

#投票ボタン
button05 = ui.Button()
button05.frame = (465, 5, 80, 50)
button05.title = '投票'
button05.border_color = ('brack')
button05.border_width = 1
button05.action = button05_action
main_view.add_subview(button05)

#レース結果
button06 = ui.Button()
button06.frame = (550, 5, 80, 50)
button06.title = 'レース結果'
button06.border_color = ('brack')
button06.border_width = 1
button06.action = button06_action
main_view.add_subview(button06)


#データ検索ボタン
button07 = ui.Button()
button07.frame = (635,5, 80, 50)
button07.title = 'データ検索'
button07.border_color = ('brack')
button07.border_width = 1
button07.action = button07_action
main_view.add_subview(button07)


#出走表　基本
webview0a = ui.WebView()
webview0a.frame = (5, 60, 758, 300)
webview0a.border_color = ('brack')
webview0a.border_width = 1
main_view.add_subview(webview0a)

#出走表　能力
webview0b = ui.WebView()
webview0b.frame = (5, 365, 758, 300)
webview0b.border_color = ('brack')
webview0b.border_width = 1
main_view.add_subview(webview0b)

#展示
webview0c = ui.WebView()
webview0c.frame = (5, 670, 758, 300)
webview0c.border_color = ('brack')
webview0c.border_width = 1
main_view.add_subview(webview0c)

#出走表選択ビューの定義
view01 = ui.View(frame=(0, 0, 768, 1024))
view01.name = 'BOAT RACE Dash Board 【出走表選択】'
view01.background_color = ('white')
#取消ボタン
button011 = ui.Button()
button011.frame = (5, 5, 80, 50)
button011.title = '取消'
button011.border_color = ('brack')
button011.border_width = 1
button011.action = button011_action
view01.add_subview(button011)

#開催日選択テーブルビュー
tableview013 = ui.TableView()
tableview013.frame = (5, 60, 758, 50)

tableview013.data_source_items = ''
tableview013.data_source_number_of_lines = 1
tableview013.data_source_delete_enabled = False
tableview013.data_source_font_size = 18
tableview013.row_height = 44
view01.add_subview(tableview013)
#場名選択テーブルビュー
tableview014 = ui.TableView()
tableview014.frame = (5, 115, 758, 50)
tableview014.data_source_items = ''
tableview014.data_source_number_of_lines = 1
tableview014.data_source_delete_enabled = False
tableview014.data_source_font_size = 18
tableview014.row_height = 44
view01.add_subview(tableview014)
#レース番号選択テーブルビュー
tableview015 = ui.TableView()
tableview015.frame = (5, 170, 758, 50)
tableview015.data_source_items = ''
tableview015.data_source_number_of_lines = 1
tableview015.data_source_delete_enabled = False
tableview015.data_source_font_size = 18
tableview015.row_height = 44
view01.add_subview(tableview015)

#選手戦歴ビューの定義
view03 = ui.View(frame=(0, 0, 768, 1024))
view03.name = '選手戦歴ビュー'
view03.background_color = ('white')
#戻るボタン
button031 = ui.Button()
button031.frame = (5, 5, 80, 50)
button031.title = '戻る'
button031.border_color = ('brack')
button031.border_width = 1
button031.action = button031_action
view03.add_subview(button031)
#選手戦歴ボタン
button032 = ui.Button()
button032.frame = (90, 5, 80, 50)
button032.title = '選手戦歴'
button032.border_color = ('brack')
button032.border_width = 1
button032.action = button032_action
view03.add_subview(button032)
#モーター戦歴ボタン
button033 = ui.Button()
button033.frame = (175, 5, 80, 50)
button033.title = 'モータ戦歴'
button033.border_color = ('brack')
button033.border_width = 1
button033.action = button033_action
view03.add_subview(button033)
#部品交換歴ボタン
button034 = ui.Button()
button034.frame = (260, 5, 80, 50)
button034.title = '部品交換歴'
button034.border_color = ('brack')
button034.border_width = 1
button034.action = button034_action
view03.add_subview(button034)

#選手選択ビュー
tableview032 = ui.TableView()
tableview032.frame = (5, 60, 758, 50)
tableview032.data_source_items = ''
tableview032.data_source_number_of_lines = 1
tableview032.data_source_delete_enabled = False
tableview032.data_source_font_size = 18
tableview032.row_height = 44
view03.add_subview(tableview032)
#Webビュー
webview033 = ui.WebView()
webview033.frame = (5, 115, 758, 900)
webview033.border_color = ('brack')
webview033.border_width = 1
webview033.scales_page_to_fit = False	
view03.add_subview(webview033)

#twitterビューの定義
view04 = ui.View(frame=(0, 0, 768, 1024))
view04.name = 'twitterによる選手情報検索'
view04.background_color = ('white')
#戻るボタン
button041 = ui.Button()
button041.frame = (5, 5, 80, 50)
button041.title = '戻る'
button041.border_color = ('brack')
button041.border_width = 1
button041.action = button041_action
view04.add_subview(button041)
#選手選択ビュー
tableview042 = ui.TableView()
tableview042.frame = (5, 60, 758, 50)
tableview042.data_source_items = ''
tableview042.data_source_number_of_lines = 1
tableview042.data_source_delete_enabled = False
tableview042.data_source_font_size = 18
tableview042.row_height = 44
view04.add_subview(tableview042)
#Webビュー
webview043 = ui.WebView()
webview043.frame = (5, 115, 758, 900)
webview043.border_color = ('brack')
webview043.border_width = 1
webview043.scales_page_to_fit = False	
view04.add_subview(webview043)


#投票ビューの定義
view05 = ui.View(frame=(0, 0, 768, 1024))
view05.name = 'BOAT RACE Dash Board 【投票】'
view05.background_color = ('white')
#戻るボタン
button051 = ui.Button()
button051.frame = (5, 5, 80, 50)
button051.title = '戻る'
button051.border_color = ('brack')
button051.border_width = 1
button051.action = button051_action
view05.add_subview(button051)
#Webビュー
webview052 = ui.WebView()
webview052.frame = (5, 60, 758, 960)
webview052.border_color = ('brack')
webview052.border_width = 1
view05.add_subview(webview052)

#レース結果ビューの定義
view06 = ui.View(frame=(0, 0, 768, 1024))
view06.name = 'BOAT RACE Dash Board 【レース結果】'
view06.background_color = ('white')
#戻るボタン
button061 = ui.Button()
button061.frame = (5, 5, 80, 50)
button061.title = '戻る'
button061.border_color = ('brack')
button061.border_width = 1
button061.action = button061_action
view06.add_subview(button061)
#Webビュー
webview062 = ui.WebView()
webview062.frame = (5, 60, 758, 960)
webview062.border_color = ('brack')
webview062.border_width = 1
view06.add_subview(webview062)

#データ検索ビューの定義
view07 = ui.View(frame=(0, 0, 768, 1024))
view07.name = 'データ検索'
view07.background_color = ('white')
#戻るボタン
button071 = ui.Button()
button071.frame = (5, 5, 80, 50)
button071.title = '戻る'
button071.border_color = ('brack')
button071.border_width = 1
button071.action = button071_action
view07.add_subview(button071)
#選手選択ビュー
tableview072 = ui.TableView()
tableview072.frame = (5, 60, 758, 50)
tableview072.data_source_items = ''
tableview072.data_source_number_of_lines = 1
tableview072.data_source_delete_enabled = False
tableview072.data_source_font_size = 18
tableview072.row_height = 44
view07.add_subview(tableview072)
#Webビュー
webview073 = ui.WebView()
webview073.frame = (5, 115, 758, 900)
webview073.border_color = ('brack')
webview073.border_width = 1
webview073.scales_page_to_fit = False	
view07.add_subview(webview073)




#メインビューの描画
main_view.present('sheet')
