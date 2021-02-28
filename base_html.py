"""
【システム】BOAT RACE DASH BOARD(ボートレースダッシュボート)
【ファイル】base_html.py
【機能仕様】メイン画面から使用されるhtmlを定義
【動作環境】pythonista3
【開発来歴】2021.01.23 Ver 1.00
"""

"""
【機　能】選手戦歴
【変数名】player_history_html 
【引　数】@detail  明細行
"""
player_history_html = '''
<!DOCTYPE html>
<html>
<head>
	<style>
		.width30{
			width: 20px
		}
		.width60{
			width: 60px
		}
		.width100{
			width: 100px
		}
		.width200{
			width: 200px
		}
		.width300{
			width: 300px
		}
	    .text-left {
			text-align: left;
		}
		.text-right {
			text-align: right;
		}
		.text-center {
			text-align: center;
		}
		.TableColumnColoredCCell1{
  			background-color:#ffd3d3;
		}
		body {
			font-size: 70%;
    		color: #292929;
    		font-family: "ヒラギノ角ゴ Pro W3","Hiragino Kaku Gothic Pro","メイリオ",Meiryo,"ＭＳ Ｐゴシック",Osaka,sans-serif;
    		-webkit-text-size-adjust: 100%;	
		}
		table{
  			width: 3000px;
		}
		th,td{
  			height: 50px;
  			vertical-align: middle;
  			padding: 0 15px;
  			border: 1px solid #ccc;
		}
		.fixed01,
		.fixed02{
  			position: sticky;
  			top: 0;
  			left: 0;
  			color: #fff;
  			background: rgb(9, 4, 96);
  			&:before{
    			content: "";
    			position: absolute;
    			top: -1px;
    			left: -1px;
    			width: 100%;
    			height: 100%;
    			border: 1px solid #ccc;
  			}
		}
		.fixed01{
  			z-index: 2;
		}
		.fixed02{
  			z-index: 1;
		}
	</style>
  	<meta charset="utf-8">
  	<title>選手戦歴</title>
</head>
<body>
	<table>
		@detail
	</table>
</body>
</html>
'''

"""
【機　能】モーター戦歴
【変数名】motor_history_html
【引　数】@detail  明細行
"""
motor_history_html = '''
<!DOCTYPE html>
<html>
<head>
	<style>
		.width30{
			width: 20px
		}
		.width60{
			width: 60px
		}
		.width100{
			width: 100px
		}
		.width200{
			width: 200px
		}
		.width300{
			width: 300px
		}
	    .text-left {
			text-align: left;
		}
		.text-right {
			text-align: right;
		}
		.text-center {
			text-align: center;
		}
		.TableColumnColoredCCell1{
  			background-color:#ffd3d3;
		}
		body {
    		color: #292929;
    		font-family: "ヒラギノ角ゴ Pro W3","Hiragino Kaku Gothic Pro","メイリオ",Meiryo,"ＭＳ Ｐゴシック",Osaka,sans-serif;
    		-webkit-text-size-adjust: 100%;	
		}
		table{
  			width: 5000px;
		}
		th,td{
  			height: 50px;
  			vertical-align: middle;
  			padding: 0 15px;
  			border: 1px solid #ccc;
		}
		.fixed01,
		.fixed02{
  			position: sticky;
  			top: 0;
  			left: 0;
  			color: #fff;
  			background: rgb(9, 4, 96);
  			&:before{
    			content: "";
    			position: absolute;
    			top: -1px;
    			left: -1px;
    			width: 100%;
    			height: 100%;
    			border: 1px solid #ccc;
  			}
		}
		.fixed01{
  			z-index: 2;
		}
		.fixed02{
  			z-index: 1;
		}
	</style>
  	<meta charset="utf-8">
  	<title>モーター戦歴</title>
</head>
<body>
	<table>
		@detail
	</table>
</body>
</html>
'''

"""
【機　能】部品交換履歴
【変数名】parts_history_html
【引　数】@detail  明細行
"""
parts_history_html = '''
<!DOCTYPE html>
<html>
<head>
	<style>
		.width30{
			width: 20px
		}
		.width60{
			width: 60px
		}
		.width100{
			width: 100px
		}
		.width200{
			width: 200px
		}
		.width300{
			width: 300px
		}
	    .text-left {
			text-align: left;
		}
		.text-right {
			text-align: right;
		}
		.text-center {
			text-align: center;
		}
		.TableColumnColoredCCell1{
  			background-color:#ffd3d3;
		}
		body {
    		color: #292929;
    		font-family: "ヒラギノ角ゴ Pro W3","Hiragino Kaku Gothic Pro","メイリオ",Meiryo,"ＭＳ Ｐゴシック",Osaka,sans-serif;
    		-webkit-text-size-adjust: 100%;	
		}
		table{
  			width: 5000px;
		}
		th,td{
  			height: 50px;
  			vertical-align: middle;
  			padding: 0 15px;
  			border: 1px solid #ccc;
		}
		.fixed01,
		.fixed02{
  			position: sticky;
  			top: 0;
  			left: 0;
  			color: #fff;
  			background: rgb(9, 4, 96);
  			&:before{
    			content: "";
    			position: absolute;
    			top: -1px;
    			left: -1px;
    			width: 100%;
    			height: 100%;
    			border: 1px solid #ccc;
  			}
		}
		.fixed01{
  			z-index: 2;
		}
		.fixed02{
  			z-index: 1;
		}
	</style>
  	<meta charset="utf-8">
  	<title>部品交換履歴</title>
</head>
<body>
	<table>
		@detail
	</table>
</body>
</html>
'''

"""
【機　能】出走表を表示する
【変数名】race_table_html
【引　数】@detail1 出走表
"""
race_table_html = '''
<!DOCTYPE html>
<html>
<head>
	<style>
		.width30{
			width: 20px
		}
		.width60{
			width: 60px
		}
		.width100{
			width: 100px
		}
		.width200{
			width: 200px
		}
		.width300{
			width: 300px
		}
	    .text-left {
			text-align: left;
		}
		.text-right {
			text-align: right;
		}
		.text-center {
			text-align: center;
		}
		.TableColumnColoredCCell1{
  			background-color:#ffd3d3;
		}
		body {
    		color: #292929;
    		font-family: "ヒラギノ角ゴ Pro W3","Hiragino Kaku Gothic Pro","メイリオ",Meiryo,"ＭＳ Ｐゴシック",Osaka,sans-serif;
    		-webkit-text-size-adjust: 100%;	
		}
		table{
  			width: 1800px;
		}
		th,td{
  			height: 50px;
  			vertical-align: middle;
  			padding: 0 15px;
  			border: 1px solid #ccc;
		}
		.fixed01,
		.fixed02{
  			position: sticky;
  			top: 0;
  			left: 0;
  			color: #fff;
  			background: rgb(9, 4, 96);
  			&:before{
    			content: "";
    			position: absolute;
    			top: -1px;
    			left: -1px;
    			width: 100%;
    			height: 100%;
    			border: 1px solid #ccc;
  			}
		}
		.fixed01{
  			z-index: 2;
		}
		.fixed02{
  			z-index: 1;
		}
	</style>
  	<meta charset="utf-8">
  	<title>出走表</title>
</head>
<body>
	@table1
</body>
</html>
'''



"""
【機　能】展示情報
【変数名】tenji_html
【引　数】
"""
tenji_html = '''
<!DOCTYPE html>
<html>
<head>
	<style>
		.width30{
			width: 20px
		}
		.width60{
			width: 60px
		}
		.width100{
			width: 100px
		}
		.width200{
			width: 200px
		}
		.width300{
			width: 300px
		}
	    .text-left {
			text-align: left;
		}
		.text-right {
			text-align: right;
		}
		.text-center {
			text-align: center;
		}
		.TableColumnColoredCCell1{
  			background-color:#ffd3d3;
		}
		body {
    		color: #292929;
    		font-family: "ヒラギノ角ゴ Pro W3","Hiragino Kaku Gothic Pro","メイリオ",Meiryo,"ＭＳ Ｐゴシック",Osaka,sans-serif;
    		-webkit-text-size-adjust: 100%;	
		}
		table{
  			width: 2600px;
		}
		th,td{
  			height: 50px;
  			vertical-align: middle;
  			padding: 0 15px;
  			border: 1px solid #ccc;
		}
		.fixed01,
		.fixed02{
  			position: sticky;
  			top: 0;
  			left: 0;
  			color: #fff;
  			background: rgb(9, 4, 96);
  			&:before{
    			content: "";
    			position: absolute;
    			top: -1px;
    			left: -1px;
    			width: 100%;
    			height: 100%;
    			border: 1px solid #ccc;
  			}
		}
		.fixed01{
  			z-index: 2;
		}
		.fixed02{
  			z-index: 1;
		}
	</style>
  	<meta charset="utf-8">
  	<title>展示情報</title>
</head>
<body>
	<table>
		<tr>
			<th class="fixed01 text-center">選手情報</th>
			<th class="fixed02 text-center">能力</th>
			<th class="fixed02 text-center">直近能力</th>
			<th class="fixed02 text-center">Ｍ能力</th>
			<th class="fixed02 text-center">得票率１着</th>
			<th class="fixed02 text-center">得票率２着</th>
			<th class="fixed02 text-center">得票率３着</th>
			<th class="fixed02 text-center">展示時計</th>
			<th class="fixed02 text-center">チルト</th>
			<th class="fixed02 text-center">進入</th>
			<th class="fixed02 text-center">ＳＴ</th>
			<th class="fixed02 text-center">直近ＳＴ</th>
			<th class="fixed02 text-center">一周</th>
			<th class="fixed02 text-center">まわり足</th>
			<th class="fixed02 text-center">直線</th>			
			<th class="fixed02 text-center">進入</th>
			<th class="fixed02 text-center">進入別能力</th>
			<th class="fixed02 text-center">進入別Ｍ能力</th>
			<th class="fixed02 text-center">逃げ逃がし率</th>
			<th class="fixed02 text-center">まくりまくられ率</th>
			<th class="fixed02 text-center">差され差し率</th>
			<th class="fixed02 text-center">交換部品</th>
		</tr>
		<tr>
			<th class="fixed02 text-left">@選手情報1</th>
			<td class="text-right">@能力1</td>
			<td class="text-right">@直近能力1</td>
			<td class="text-right">@Ｍ能力1</td>
			<td class="text-right">@得票率１着1</td>
			<td class="text-right">@得票率２着1</td>
			<td class="text-right">@得票率３着1</td>
			<td class="text-right">@展示時計1</td>
			<td class="text-right">@チルト1</td>
			<td class="text-right">@進入1</td>
			<td class="text-right">@ＳＴ1</td>
			<td class="text-right">@直近ＳＴ1</td>
			<td class="text-right">@一周1</td>
			<td class="text-right">@まわり足1</td>
			<td class="text-right">@直線1</td>			
			<td class="text-right">@進入1</td>
			<td class="text-right">@進入別能力1</td>
			<td class="text-right">@進入別Ｍ能力1</td>
			<td class="text-right">@逃げ逃がし率1</td>
			<td class="text-right">@まくりまくられ率1</td>
			<td class="text-right">@差され差し率1</td>
			<td class="text-left">@交換部品1</td>
		</tr>
		<tr>
			<th class="fixed02 text-left">@選手情報2</th>
			<td class="text-right">@能力2</td>
			<td class="text-right">@直近能力2</td>
			<td class="text-right">@Ｍ能力2</td>
			<td class="text-right">@得票率１着2</td>
			<td class="text-right">@得票率２着2</td>
			<td class="text-right">@得票率３着2</td>
			<td class="text-right">@展示時計2</td>
			<td class="text-right">@チルト2</td>
			<td class="text-right">@進入2</td>
			<td class="text-right">@ＳＴ2</td>
			<td class="text-right">@直近ＳＴ2</td>
			<td class="text-right">@一周2</td>
			<td class="text-right">@まわり足2</td>
			<td class="text-right">@直線2</td>			
			<td class="text-right">@進入2</td>
			<td class="text-right">@進入別能力2</td>
			<td class="text-right">@進入別Ｍ能力2</td>
			<td class="text-right">@逃げ逃がし率2</td>
			<td class="text-right">@まくりまくられ率2</td>
			<td class="text-right">@差され差し率2</td>
			<td class="text-left">@交換部品2</td>
		</tr>
		<tr>
			<th class="fixed02 text-left">@選手情報3</th>
			<td class="text-right">@能力3</td>
			<td class="text-right">@直近能力3</td>
			<td class="text-right">@Ｍ能力3</td>
			<td class="text-right">@得票率１着3</td>
			<td class="text-right">@得票率２着3</td>
			<td class="text-right">@得票率３着3</td>
			<td class="text-right">@展示時計3</td>
			<td class="text-right">@チルト3</td>
			<td class="text-right">@進入3</td>
			<td class="text-right">@ＳＴ3</td>
			<td class="text-right">@直近ＳＴ3</td>
			<td class="text-right">@一周3</td>
			<td class="text-right">@まわり足3</td>
			<td class="text-right">@直線3</td>			
			<td class="text-right">@進入3</td>
			<td class="text-right">@進入別能力3</td>
			<td class="text-right">@進入別Ｍ能力3</td>
			<td class="text-right">@逃げ逃がし率3</td>
			<td class="text-right">@まくりまくられ率3</td>
			<td class="text-right">@差され差し率3</td>
			<td class="text-left">@交換部品3</td>
		</tr>
		<tr>
			<th class="fixed02 text-left">@選手情報4</th>
			<td class="text-right">@能力4</td>
			<td class="text-right">@直近能力4</td>
			<td class="text-right">@Ｍ能力4</td>
			<td class="text-right">@得票率１着4</td>
			<td class="text-right">@得票率２着4</td>
			<td class="text-right">@得票率３着4</td>
			<td class="text-right">@展示時計4</td>
			<td class="text-right">@チルト4</td>
			<td class="text-right">@進入4</td>
			<td class="text-right">@ＳＴ4</td>
			<td class="text-right">@直近ＳＴ4</td>
			<td class="text-right">@一周4</td>
			<td class="text-right">@まわり足4</td>
			<td class="text-right">@直線4</td>			
			<td class="text-right">@進入4</td>
			<td class="text-right">@進入別能力4</td>
			<td class="text-right">@進入別Ｍ能力4</td>
			<td class="text-right">@逃げ逃がし率4</td>
			<td class="text-right">@まくりまくられ率4</td>
			<td class="text-right">@差され差し率4</td>
			<td class="text-left">@交換部品4</td>
		</tr>
		<tr>
			<th class="fixed02 text-left">@選手情報5</th>
			<td class="text-right">@能力5</td>
			<td class="text-right">@直近能力5</td>
			<td class="text-right">@Ｍ能力5</td>
			<td class="text-right">@得票率１着5</td>
			<td class="text-right">@得票率２着5</td>
			<td class="text-right">@得票率３着5</td>
			<td class="text-right">@展示時計5</td>
			<td class="text-right">@チルト5</td>
			<td class="text-right">@進入5</td>
			<td class="text-right">@ＳＴ5</td>
			<td class="text-right">@直近ＳＴ5</td>
			<td class="text-right">@一周5</td>
			<td class="text-right">@まわり足5</td>
			<td class="text-right">@直線5</td>			
			<td class="text-right">@進入5</td>
			<td class="text-right">@進入別能力5</td>
			<td class="text-right">@進入別Ｍ能力5</td>
			<td class="text-right">@逃げ逃がし率5</td>
			<td class="text-right">@まくりまくられ率5</td>
			<td class="text-right">@差され差し率5</td>
			<td class="text-left">@交換部品5</td>
		</tr>
		<tr>
			<th class="fixed02 text-left">@選手情報6</th>
			<td class="text-right">@能力6</td>
			<td class="text-right">@直近能力6</td>
			<td class="text-right">@Ｍ能力6</td>
			<td class="text-right">@得票率１着6</td>
			<td class="text-right">@得票率２着6</td>
			<td class="text-right">@得票率３着6</td>
			<td class="text-right">@展示時計6</td>
			<td class="text-right">@チルト6</td>
			<td class="text-right">@進入6</td>
			<td class="text-right">@ＳＴ6</td>
			<td class="text-right">@直近ＳＴ6</td>
			<td class="text-right">@一周6</td>
			<td class="text-right">@まわり足6</td>
			<td class="text-right">@直線6</td>			
			<td class="text-right">@進入6</td>
			<td class="text-right">@進入別能力6</td>
			<td class="text-right">@進入別Ｍ能力6</td>
			<td class="text-right">@逃げ逃がし率6</td>
			<td class="text-right">@まくりまくられ率6</td>
			<td class="text-right">@差され差し率6</td>
			<td class="text-left">@交換部品6</td>
		</tr>
	</table>
</body>
</html>
'''


"""
【機　能】データ検索
【変数名】data_html 
【引　数】@detail  明細行
"""
data_html = '''
<!DOCTYPE html>
<html>
<head>
	<style>
		.width30{
			width: 20px
		}
		.width60{
			width: 60px
		}
		.width100{
			width: 100px
		}
		.width200{
			width: 200px
		}
		.width300{
			width: 300px
		}
	    .text-left {
			text-align: left;
		}
		.text-right {
			text-align: right;
		}
		.text-center {
			text-align: center;
		}
		.TableColumnColoredCCell1{
  			background-color:#ffd3d3;
		}
		body {
			font-size: 70%;
    		color: #292929;
    		font-family: "ヒラギノ角ゴ Pro W3","Hiragino Kaku Gothic Pro","メイリオ",Meiryo,"ＭＳ Ｐゴシック",Osaka,sans-serif;
    		-webkit-text-size-adjust: 100%;	
		}
		table{
  			width: 2000px;
		}
		th,td{
  			height: 50px;
  			vertical-align: middle;
  			padding: 0 15px;
  			border: 1px solid #ccc;
		}
		.fixed01,
		.fixed02{
  			position: sticky;
  			top: 0;
  			left: 0;
  			color: #fff;
  			background: rgb(9, 4, 96);
  			&:before{
    			content: "";
    			position: absolute;
    			top: -1px;
    			left: -1px;
    			width: 100%;
    			height: 100%;
    			border: 1px solid #ccc;
  			}
		}
		.fixed01{
  			z-index: 2;
		}
		.fixed02{
  			z-index: 1;
		}
	</style>
  	<meta charset="utf-8">
  	<title>選手戦歴</title>
</head>
<body>
	<table>
		@detail
	</table>
</body>
</html>
'''



"""
【機　能】画面クリア
【変数名】clear_html
【引　数】
"""
clear_html = '''
<!DOCTYPE html>
<html>
<head>
	<style>
		.width30{
			width: 20px
		}
		.width60{
			width: 60px
		}
		.width100{
			width: 100px
		}
		.width200{
			width: 200px
		}
		.width300{
			width: 300px
		}
	    .text-left {
			text-align: left;
		}
		.text-right {
			text-align: right;
		}
		.text-center {
			text-align: center;
		}
		.TableColumnColoredCCell1{
  			background-color:#ffd3d3;
		}
		body {
    		color: #292929;
    		font-family: "ヒラギノ角ゴ Pro W3","Hiragino Kaku Gothic Pro","メイリオ",Meiryo,"ＭＳ Ｐゴシック",Osaka,sans-serif;
    		-webkit-text-size-adjust: 100%;	
		}
		table{
  			width: 1900px;
		}
		th,td{
  			height: 50px;
  			vertical-align: middle;
  			padding: 0 15px;
  			border: 1px solid #ccc;
		}
		.fixed01,
		.fixed02{
  			position: sticky;
  			top: 0;
  			left: 0;
  			color: #fff;
  			background: rgb(9, 4, 96);
  			&:before{
    			content: "";
    			position: absolute;
    			top: -1px;
    			left: -1px;
    			width: 100%;
    			height: 100%;
    			border: 1px solid #ccc;
  			}
		}
		.fixed01{
  			z-index: 2;
		}
		.fixed02{
  			z-index: 1;
		}
	</style>
  	<meta charset="utf-8">
  	<title>画面初期化</title>
</head>
<body>
</body>
</html>
'''
