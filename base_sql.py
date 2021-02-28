"""
【システム】BOAT RACE DASH BOARD(ボートレースダッシュボート)
【ファイル】user_sql.py
【機能仕様】メイン画面から使用されるSQLを定義
【動作環境】pythonista3
【開発来歴】2021.01.23 Ver 1.00
"""

"""
【機　能】開催リストを取得
【変数名】kaisai_list_sql 
【引　数】なし
"""
kaisai_list_sql = '''
SELECT 
x_race_t.yyyymmdd,x_race_t.pool_name, x_race_t.grade,x_race_t.title,x_race_t.event_date
FROM
x_race_t
ORDER BY x_race_t.yyyymmdd DESC,x_race_t.pool_code ASC
'''


"""
【機　能】開催日に施行されているボートレース場を検索する
【変数名】pool_list_sql
【引　数】@yyyymmdd	開催日
"""
pool_list_sql = '''
SELECT 
	x_race_h.pool_code,x_race_h.pool_name,x_race_t.holding,x_race_t.grade,x_race_t.event_date,x_race_t.title
FROM
	x_race_h,x_race_t
WHERE
    x_race_h.race_no= '01' AND
	x_race_h.yyyymmdd = '@yyyymmdd' AND
	x_race_t.yyyymmdd = x_race_h.yyyymmdd AND
	x_race_t.pool_code = x_race_h.pool_code
	ORDER BY x_race_h.pool_code ASC
'''

"""
【機　能】開催日と場コードに一致するレース情報を検索する
【変数名】race_list_sql
【引　数】@yyyymmdd	開催日
		  @poolcode 場コード
"""
race_list_sql = """
SELECT 
	x_race_h.pool_name,
	x_race_h.race_no,
	x_race_h.scheduled_deadline,
	x_race_h.race_name,
	x_race_h.distance,
	x_race_h.approach,
	x_race_h.stabilizer
FROM
	x_race_h
WHERE
	x_race_h.yyyymmdd = '@yyyymmdd' AND
	x_race_h.pool_code = '@poolcode'
	ORDER BY x_race_h.race_no ASC
"""

"""
【機　能】開催日と場コードとレース番号に一致する選手情報を検索する
【変数名】player_list_sql
【引　数】@yyyymmdd	開催日
		  @poolcode 場コード
		  @raceno   レース番号
"""
player_list_sql = '''
SELECT
	x_race_d.entry_no,
	x_race_d.player_no,
	x_race_d.player_name,
	x_race_d.class,
	x_race_d.area,
	x_race_d.motor_no
FROM
	x_race_d
WHERE
	x_race_d.yyyymmdd = '@yyyymmdd' AND
	x_race_d.pool_code = '@poolcode' AND
	x_race_d.race_no = '@raceno'
	ORDER BY x_race_d.race_no ASC
'''
"""
【機　能】選手の戦歴情報を検索する
【変数名】player_history_sql
【引　数】@playerno 選手登録番号
"""
player_history_sql = '''
SELECT
	(t_race_t.yyyymmdd || "[" || t_race_t.pool_name || "][" || t_race_t.grade|| "][" || t_race_t.event_date || "][" || t_race_h.race_no || "R][" || t_result_d.ranking || "]") as 選手戦歴情報,
	t_race_t.yyyymmdd as 日付,
	t_race_t.pool_name as 場名,
	t_race_t.grade as 区分,
	t_race_t.title as タイトル,
	t_race_t.event_date as 開催日,
	t_race_h.race_no as レース番号,
	t_race_h.race_name as レース名,
	t_result_h.weather as 天候,
	t_result_h.temperature as 気温,
	t_result_h.water_temperature as 水温,
	t_result_h.wave_height as 波高,
	t_result_h.wind as 風向,
	t_result_h.wind_speed as 風速,
	t_result_h.situdo as 湿度,
	t_result_h.kiatu as 気圧,
	t_race_d.player_no as 登番,
	t_race_d.player_name as 選手名,
	t_race_d.area as 支部,
	t_race_d.class as 等級,
	ROUND(t_index.ability,1) as 能力,
	ROUND(t_index.ability2,1) as 直近能力,
	ROUND(t_race_d.flying_count,1) as F回数,
	t_info_d.body_weight as 重量,
	t_info_d.adjusted_weight as 調整,
	t_race_d.motor_no as Ｍ番号,
	ROUND(t_index.rate_win_motor,1) as Ｍ能力,
	t_race_d.entry_no as  艇番,
	t_info_d.start_course as 展示コース,
	t_info_d.flying as 展示F,
	t_info_d.start_time as 展示ST,
	t_info_d.rehearsal_time as 展示時計,
	t_result_d.course as 進入,
	t_result_d.flying as F,
	t_result_d.start_time as ST,
	t_result_d.flying as F,
	t_result_d.ranking as 着,
	t_result_d.decisive_facto as 決まり手
FROM
	t_race_t,t_race_h,t_race_d,t_result_d,t_info_d,t_result_h,t_index
WHERE
	t_race_d.player_no = '@playerno' AND
	t_race_t.yyyymmdd = t_race_h.yyyymmdd AND
	t_race_t.pool_code = t_race_h.pool_code AND
	t_race_h.yyyymmdd = t_race_d.yyyymmdd AND
	t_race_h.pool_code = t_race_d.pool_code AND
	t_race_h.race_no = t_race_d.race_no AND
	t_race_h.yyyymmdd = t_result_h.yyyymmdd AND
	t_race_h.pool_code = t_result_h.pool_code AND
	t_race_h.race_no = t_result_h.race_no AND
	t_race_d.yyyymmdd = t_result_d.yyyymmdd AND
	t_race_d.pool_code = t_result_d.pool_code AND
	t_race_d.race_no = t_result_d.race_no AND
	t_race_d.entry_no = t_result_d.entry_no AND
	t_race_d.yyyymmdd = t_info_d.yyyymmdd AND
	t_race_d.pool_code = t_info_d.pool_code AND
	t_race_d.race_no = t_info_d.race_no AND
	t_race_d.entry_no = t_info_d.entry_no AND
	t_race_d.yyyymmdd = t_index.yyyymmdd AND
	t_race_d.pool_code = t_index.pool_code AND
	t_race_d.race_no = t_index.race_no AND
	t_race_d.entry_no = t_index.entry_no
ORDER BY t_result_d.yyyymmdd DESC, t_result_d.race_no DESC
'''

"""
【機　能】最新のモーター交換日付を取得
【変数名】new_motor_sql
【引　数】@poolcode 場コード
"""
new_motor_sql = '''
SELECT  yyyymmdd
	FROM (
		SELECT
			pool_code,yyyymmdd
		FROM
			(SELECT
				t_tenken.yyyy as yyyy,
				t_tenken.yyyymmdd AS yyyymmdd,
				t_tenken.pool_code  as pool_code,
				t_tenken.title  as title,
				count(t_tenken.motor_no)  as motor_count
				FROM
					t_tenken
				WHERE
					t_tenken.pool_code = '@poolcode'
					AND  t_tenken.motor_double_rate = 0.0
				GROUP BY t_tenken.yyyy,t_tenken.yyyymmdd,t_tenken.pool_code,t_tenken.title)
		WHERE
			motor_count >= 40 
		ORDER BY yyyymmdd DESC)
GROUP by pool_code
'''

"""
【機　能】モーター戦歴を取得
【変数名】motor_history_sql
【引　数】@new_motor_yyyymmdd　新モーター交換日付
　　　　　@poolcode　　　　　　場コード
　　　　　@motorno             モーター番号
"""
motor_history_sql = '''
SELECT
    (t_race_h.yyyymmdd || " [" || t_race_t.grade || "] [" || t_race_t.event_date || "] " || t_race_h.race_no || "R [" || t_result_d.ranking || "]") as モーター情報,
	t_race_t.yyyymmdd as 日付,
	t_race_t.pool_name as 場名,
	t_race_t.grade as 区分,
	t_race_t.title as タイトル,
	t_race_t.event_date as 開催日,
	t_race_h.race_no as レース番号,
	t_race_h.race_name as レース名,
	t_result_h.weather as 天候,
	t_result_h.temperature as 気温,
	t_result_h.water_temperature as 水温,
	t_result_h.wave_height as 波高,
	t_result_h.wind as 風向,
	t_result_h.wind_speed as 風速,
	t_result_h.situdo as 湿度,
	t_result_h.kiatu as 気圧,
	t_race_d.player_no as 登番,
	t_race_d.player_name as 選手名,
	t_race_d.area as 支部,
	t_race_d.class as 等級,
	ROUND(t_index.ability,1) as 能力,
	ROUND(t_index.ability2,1) as 直近能力,
	t_race_d.flying_count as F回数,
	t_info_d.body_weight as 重量,
	t_info_d.adjusted_weight as 調整,
	t_race_d.motor_no as Ｍ番号,
	ROUND(t_index.rate_win_motor,1) as Ｍ能力,
	t_race_d.entry_no as  艇番,
	t_info_d.start_course as 展示コース,
	t_info_d.flying as 展示F,
	t_info_d.start_time as 展示ST,
	t_info_d.rehearsal_time as 展示時計,
	t_result_d.course as 進入,
	t_result_d.flying as F,
	t_result_d.start_time as ST,
	t_result_d.flying as F,
	t_result_d.ranking as 着,
	t_result_d.decisive_facto as 決まり手
FROM
	t_race_t,t_race_h,t_race_d,t_result_d,t_info_d,t_result_h,t_index
WHERE
	t_race_t.yyyymmdd >= '@new_motor_yyyymmdd' AND
	t_race_t.pool_code = '@poolcode' AND
	t_race_d.motor_no = '@motorno' AND 
	t_race_t.yyyymmdd = t_race_h.yyyymmdd AND
	t_race_t.pool_code = t_race_h.pool_code AND
	t_race_h.yyyymmdd = t_race_d.yyyymmdd AND
	t_race_h.pool_code = t_race_d.pool_code AND
	t_race_h.race_no = t_race_d.race_no AND
	t_race_h.yyyymmdd = t_result_h.yyyymmdd AND
	t_race_h.pool_code = t_result_h.pool_code AND
	t_race_h.race_no = t_result_h.race_no AND
	t_race_d.yyyymmdd = t_result_d.yyyymmdd AND
	t_race_d.pool_code = t_result_d.pool_code AND
	t_race_d.race_no = t_result_d.race_no AND
	t_race_d.entry_no = t_result_d.entry_no AND
	t_race_d.yyyymmdd = t_info_d.yyyymmdd AND
	t_race_d.pool_code = t_info_d.pool_code AND
	t_race_d.race_no = t_info_d.race_no AND
	t_race_d.entry_no = t_info_d.entry_no AND
	t_race_d.yyyymmdd = t_index.yyyymmdd AND
	t_race_d.pool_code = t_index.pool_code AND
	t_race_d.race_no = t_index.race_no AND
	t_race_d.entry_no = t_index.entry_no
ORDER BY t_result_d.yyyymmdd DESC, t_result_d.race_no DESC
'''

"""
【機　能】部品交換履歴
【変数名】parts_history_sql
【引　数】@new_motor_yyyymmdd　新モーター交換日付
　　　　　@poolcode　　　　　　場コード
　　　　　@motorno             モーター番号
"""
parts_history_sql = '''
SELECT
    (t_race_t.yyyymmdd || " [" || t_info_p.parts || "]") as 交換部品情報,
	t_race_t.grade as 区分,
	t_race_t.title as タイトル,
	t_race_t.event_date as 開催日,
	t_race_h.race_no as レース番号,
	t_race_h.race_name as レース名,
	t_result_h.weather as 天候,
	t_result_h.temperature as 気温,
	t_result_h.water_temperature as 水温,
	t_result_h.wave_height as 波高,
	t_result_h.wind as 風向,
	t_result_h.wind_speed as 風速,
	t_result_h.situdo as 湿度,
	t_result_h.kiatu as 気圧,
	t_race_d.player_no as 登番,
	t_race_d.player_name as 選手名,
	t_race_d.area as 支部,
	t_race_d.class as 等級,
	ROUND(t_index.ability,1) as 能力,
	ROUND(t_index.ability2,1) as 直近能力,
	t_race_d.flying_count as F回数,
	t_info_d.body_weight as 重量,
	t_info_d.adjusted_weight as 調整,
	t_race_d.motor_no as Ｍ番号,
	ROUND(t_index.rate_win_motor,1) as Ｍ能力,
	t_race_d.entry_no as  艇番,
	t_info_d.start_course as 展示コース,
	t_info_d.flying as 展示F,
	t_info_d.start_time as 展示ST,
	t_info_d.rehearsal_time as 展示時計,
	t_result_d.course as 進入,
	t_result_d.flying as F,
	t_result_d.start_time as ST,
	t_result_d.flying as F,
	t_result_d.ranking as 着,
	t_result_d.decisive_facto as 決まり手
FROM
	t_race_t,t_race_h,t_race_d,t_result_d,t_info_d,t_result_h,t_index,t_info_p
WHERE
	t_race_t.yyyymmdd >= '@new_motor_yyyymmdd' AND
	t_race_t.pool_code = '@poolcode' AND
	t_race_d.motor_no = '@motorno' AND 
	t_race_t.yyyymmdd = t_race_h.yyyymmdd AND
	t_race_t.pool_code = t_race_h.pool_code AND
	t_race_h.yyyymmdd = t_race_d.yyyymmdd AND
	t_race_h.pool_code = t_race_d.pool_code AND
	t_race_h.race_no = t_race_d.race_no AND
	t_race_h.yyyymmdd = t_result_h.yyyymmdd AND
	t_race_h.pool_code = t_result_h.pool_code AND
	t_race_h.race_no = t_result_h.race_no AND
	t_race_d.yyyymmdd = t_result_d.yyyymmdd AND
	t_race_d.pool_code = t_result_d.pool_code AND
	t_race_d.race_no = t_result_d.race_no AND
	t_race_d.entry_no = t_result_d.entry_no AND
	t_race_d.yyyymmdd = t_info_d.yyyymmdd AND
	t_race_d.pool_code = t_info_d.pool_code AND
	t_race_d.race_no = t_info_d.race_no AND
	t_race_d.entry_no = t_info_d.entry_no AND
	t_race_d.yyyymmdd = t_index.yyyymmdd AND
	t_race_d.pool_code = t_index.pool_code AND
	t_race_d.race_no = t_index.race_no AND
	t_race_d.entry_no = t_index.entry_no AND
	t_race_d.yyyymmdd = t_info_p.yyyymmdd AND
	t_race_d.pool_code = t_info_p.pool_code AND
	t_race_d.race_no = t_info_p.race_no AND
	t_race_d.entry_no = t_info_p.entry_no
ORDER BY t_result_d.yyyymmdd DESC, t_result_d.race_no DESC
'''

"""
【機　能】基本的な出走表
【変数名】race_table_sql
【引　数】@yyyymmdd		開催年月日
　　　　　@poolcode		場コード
　　　　　@raceno		レース番号
"""
race_table_sql = '''
WITH QUERY_A AS (
    SELECT
        x_race_d.entry_no as 艇番,
        x_race_d.player_no as 登番,
        x_race_d.player_name as 選手名,
        x_race_d.class as 級別,
        x_race_d.area as 支部,
        x_race_d.age as 年齢,
        x_race_d.body_weight as 体重,
        x_race_d.flying_count as Ｆ数,
        x_race_d.lost_count as Ｌ数,
        x_race_d.st as ST,
        x_race_d.nationwide_win_rate as 全勝率,
        x_race_d.nationwide_double_rate as 全二連,
        x_race_d.nationwide_triple_rate as 全三連,
        x_race_d.local_win_rate as 当勝率,
        x_race_d.local_double_rate as 当二連,
        x_race_d.local_triple_rate as 当三連,
        x_race_d.motor_no as Ｍ番号,
        x_race_d.motor_double_rate as Ｍ二連,
        x_race_d.motor_triple_rate as Ｍ三連,
        x_race_d.boat_no as Ｂ番号,
        x_race_d.boat_double_rate as Ｂ二連,
        x_race_d.boat_triple_rate as Ｂ三連	
    FROM x_race_t, x_race_h,x_race_d
    WHERE x_race_t.yyyymmdd =  '@yyyymmdd' AND x_race_t.pool_code = '@poolcode' AND x_race_h.race_no = '@raceno'
    AND (x_race_t.yyyymmdd = x_race_h.yyyymmdd AND x_race_t.pool_code = x_race_h.pool_code)
    AND (x_race_h.yyyymmdd = x_race_d.yyyymmdd AND x_race_h.pool_code = x_race_d.pool_code AND x_race_h.race_no = x_race_d.race_no)
    ORDER by x_race_t.yyyymmdd ASC, x_race_t.pool_code ASC, x_race_h.race_no ASC,x_race_d.entry_no ASC
),QUERY_B AS (
	SELECT * FROM (
		SELECT
			t_index.player_no as 登番,
			t_index.yyyymmdd as 日付,
			t_index.pool_code as 場コード,
			t_index.race_no as レース番号,
			t_index.entry_no as 艇番,
			t_index.motor_no as Ｍ番号,
			ROUND(t_index.ability, 1) as 能力,
			t_index.st as ST,
			ROUND(t_index.ability2, 1) as 直近能力,
			t_index.st2 as 直近ST,
			ROUND(t_index.ability_course_1, 1) as 能力１,
			ROUND(t_index.ability_course_2, 1) as 能力２,
    	    ROUND(t_index.ability_course_3, 1) as 能力３,
        	ROUND(t_index.ability_course_4, 1) as 能力４,
            ROUND(t_index.ability_course_5, 1) as 能力５,
            ROUND(t_index.ability_course_6, 1) as 能力６,
            ROUND(t_index.sinnyu_course_1, 1)  as 進入１,
            ROUND(t_index.sinnyu_course_2, 1)  as 進入２,
            ROUND(t_index.sinnyu_course_3, 1)  as 進入３,
            ROUND(t_index.sinnyu_course_4, 1)  as 進入４,
            ROUND(t_index.sinnyu_course_5, 1)  as 進入５,
            ROUND(t_index.sinnyu_course_6, 1)  as 進入６,
			ROUND(t_index.nige_win_rate_course_1, 1) as 逃げ率１,
			ROUND(t_index.makuri_lost_rate_course_1, 1) as まくられ率１,
			ROUND(t_index.sashi_lost_rate_course_1, 1)as 差され率１,
			ROUND(t_index.nige_lost_rate_course_2, 1)as 逃し率２,
			ROUND(t_index.makuri_win_rate_course_2, 1) as まくり率２,
			ROUND(t_index.makuri_win_rate_course_3, 1) as まくり率３,
			ROUND(t_index.sashi_win_rate_course_3, 1) as 差し率３,
			ROUND(t_index.makuri_win_rate_course_4, 1) as まくり率４,
			ROUND(t_index.sashi_win_rate_course_4, 1) as 差し率４,
			ROUND(t_index.makuri_win_rate_course_5, 1) as まくり率５,
			ROUND(t_index.sashi_win_rate_course_5, 1) as 差し率５,
			ROUND(t_index.makuri_win_rate_course_6, 1) as まくり率６,
			ROUND(t_index.sashi_win_rate_course_6, 1) as 差し率６
		FROM
			t_index
		WHERE t_index.player_no in  (SELECT  x_race_d.player_no FROM x_race_d WHERE x_race_d.yyyymmdd =  '@yyyymmdd' AND x_race_d.pool_code = '@poolcode' AND x_race_d.race_no = '@raceno')
		ORDER BY t_index.player_no ASC,t_index.yyyymmdd DESC, t_index.race_no DESC
    ) GROUP BY 登番
),QUERY_C AS (
	SELECT * FROM (
		SELECT
			t_index.motor_no as Ｍ番号,
			ROUND(t_index.rate_win_motor, 1) as Ｍ能力,
			ROUND(t_index.rate_win_motor_course1, 1) as Ｍ能力１,
			ROUND(t_index.rate_win_motor_course2, 1) as Ｍ能力２,
			ROUND(t_index.rate_win_motor_course3, 1) as Ｍ能力３,
			ROUND(t_index.rate_win_motor_course4, 1) as Ｍ能力４,
			ROUND(t_index.rate_win_motor_course5, 1) as Ｍ能力５,
			ROUND(t_index.rate_win_motor_course6, 1) as Ｍ能力６
		FROM
			t_index
		WHERE t_index.motor_no in  (SELECT  x_race_d.motor_no FROM x_race_d WHERE x_race_d.yyyymmdd =  '@yyyymmdd' AND x_race_d.pool_code = '@poolcode' AND x_race_d.race_no = '@raceno')
		ORDER BY t_index.motor_no  ASC,t_index.yyyymmdd DESC, t_index.race_no DESC
    ) GROUP BY Ｍ番号
)
SELECT
    (A.艇番 || "号艇[" || A.級別 || "][" || A.登番 || "]" || A.選手名) as 選手,
    A.支部,
    A.年齢,
    A.体重,
    A.Ｆ数,
    A.Ｌ数,
    A.ST,
    A.全勝率,
	A.全二連,
	A.全三連,
    A.当勝率,
	A.当二連,
	A.当三連,
    A.Ｍ番号,
    A.Ｍ二連,
    A.Ｍ三連,
    A.Ｂ番号,
    A.Ｂ二連,
    A.Ｂ三連
FROM
QUERY_A A
	INNER JOIN QUERY_B B ON A.登番 = B.登番
	INNER JOIN QUERY_C C ON A.Ｍ番号 = C.Ｍ番号
'''

"""
【機　能】能力値出走表
【変数名】race_table_sql2
【引　数】@yyyymmdd		開催年月日
　　　　　@poolcode		場コード
　　　　　@raceno		レース番号
"""
race_table_sql2 = '''
WITH QUERY_A AS (
    SELECT
        x_race_d.entry_no as 艇番,
        x_race_d.player_no as 登番,
        x_race_d.player_name as 選手名,
        x_race_d.class as 級別,
        x_race_d.area as 支部,
        x_race_d.age as 年齢,
        x_race_d.body_weight as 体重,
        x_race_d.flying_count as Ｆ数,
        x_race_d.lost_count as Ｌ数,
        x_race_d.st as ST,
        x_race_d.nationwide_win_rate as 全勝率,
        x_race_d.nationwide_double_rate as 全二連,
        x_race_d.nationwide_triple_rate as 全三連,
        x_race_d.local_win_rate as 当勝率,
        x_race_d.local_double_rate as 当二連,
        x_race_d.local_triple_rate as 当三連,
        x_race_d.motor_no as Ｍ番号,
        x_race_d.motor_double_rate as Ｍ二連,
        x_race_d.motor_triple_rate as Ｍ三連,
        x_race_d.boat_no as Ｂ番号,
        x_race_d.boat_double_rate as Ｂ二連,
        x_race_d.boat_triple_rate as Ｂ三連	
    FROM x_race_t, x_race_h,x_race_d
    WHERE x_race_t.yyyymmdd =  '@yyyymmdd' AND x_race_t.pool_code = '@poolcode' AND x_race_h.race_no = '@raceno'
    AND (x_race_t.yyyymmdd = x_race_h.yyyymmdd AND x_race_t.pool_code = x_race_h.pool_code)
    AND (x_race_h.yyyymmdd = x_race_d.yyyymmdd AND x_race_h.pool_code = x_race_d.pool_code AND x_race_h.race_no = x_race_d.race_no)
    ORDER by x_race_t.yyyymmdd ASC, x_race_t.pool_code ASC, x_race_h.race_no ASC,x_race_d.entry_no ASC
),QUERY_B AS (
	SELECT * FROM (
		SELECT
			t_index.player_no as 登番,
			t_index.yyyymmdd as 日付,
			t_index.pool_code as 場コード,
			t_index.race_no as レース番号,
			t_index.entry_no as 艇番,
			t_index.motor_no as Ｍ番号,
			ROUND(t_index.ability, 1) as 能力,
			t_index.st as ST,
			ROUND(t_index.ability2, 1) as 直近能力,
			t_index.st2 as 直近ST,
			ROUND(t_index.ability_course_1, 1) as 能力１,
			ROUND(t_index.ability_course_2, 1) as 能力２,
    	    ROUND(t_index.ability_course_3, 1) as 能力３,
        	ROUND(t_index.ability_course_4, 1) as 能力４,
            ROUND(t_index.ability_course_5, 1) as 能力５,
            ROUND(t_index.ability_course_6, 1) as 能力６,
            ROUND(t_index.sinnyu_course_1, 1)  as 進入１,
            ROUND(t_index.sinnyu_course_2, 1)  as 進入２,
            ROUND(t_index.sinnyu_course_3, 1)  as 進入３,
            ROUND(t_index.sinnyu_course_4, 1)  as 進入４,
            ROUND(t_index.sinnyu_course_5, 1)  as 進入５,
            ROUND(t_index.sinnyu_course_6, 1)  as 進入６,
			ROUND(t_index.nige_win_rate_course_1, 1) as 逃げ率１,
			ROUND(t_index.makuri_lost_rate_course_1, 1) as まくられ率１,
			ROUND(t_index.sashi_lost_rate_course_1, 1)as 差され率１,
			ROUND(t_index.nige_lost_rate_course_2, 1)as 逃し率２,
			ROUND(t_index.makuri_win_rate_course_2, 1) as まくり率２,
			ROUND(t_index.makuri_win_rate_course_3, 1) as まくり率３,
			ROUND(t_index.sashi_win_rate_course_3, 1) as 差し率３,
			ROUND(t_index.makuri_win_rate_course_4, 1) as まくり率４,
			ROUND(t_index.sashi_win_rate_course_4, 1) as 差し率４,
			ROUND(t_index.makuri_win_rate_course_5, 1) as まくり率５,
			ROUND(t_index.sashi_win_rate_course_5, 1) as 差し率５,
			ROUND(t_index.makuri_win_rate_course_6, 1) as まくり率６,
			ROUND(t_index.sashi_win_rate_course_6, 1) as 差し率６
		FROM
			t_index
		WHERE t_index.player_no in  (SELECT  x_race_d.player_no FROM x_race_d WHERE x_race_d.yyyymmdd =  '@yyyymmdd' AND x_race_d.pool_code = '@poolcode' AND x_race_d.race_no = '@raceno')
		ORDER BY t_index.player_no ASC,t_index.yyyymmdd DESC, t_index.race_no DESC
    ) GROUP BY 登番
),QUERY_C AS (
	SELECT * FROM (
		SELECT
			t_index.motor_no as Ｍ番号,
			ROUND(t_index.rate_win_motor, 1) as Ｍ能力,
			ROUND(t_index.rate_win_motor_course1, 1) as Ｍ能力１,
			ROUND(t_index.rate_win_motor_course2, 1) as Ｍ能力２,
			ROUND(t_index.rate_win_motor_course3, 1) as Ｍ能力３,
			ROUND(t_index.rate_win_motor_course4, 1) as Ｍ能力４,
			ROUND(t_index.rate_win_motor_course5, 1) as Ｍ能力５,
			ROUND(t_index.rate_win_motor_course6, 1) as Ｍ能力６
		FROM
			t_index		
		WHERE t_index.motor_no in  (SELECT  x_race_d.motor_no FROM x_race_d WHERE x_race_d.yyyymmdd =  '@yyyymmdd' AND x_race_d.pool_code = '@poolcode' AND x_race_d.race_no = '@raceno')
		ORDER BY t_index.motor_no  ASC,t_index.yyyymmdd DESC, t_index.race_no DESC
    ) GROUP BY Ｍ番号
)
SELECT
    (A.艇番 || "号艇[" || A.級別 || "][" || A.登番 || "]" || A.選手名) as 選手,
	B.能力,
    B.直近能力,
	B.ST,
	B.直近ST,
	C.Ｍ能力,
    B.進入１,
    B.進入２,
    B.進入３,
    B.進入４,
    B.進入５,
    B.進入６,
    B.能力１,
    B.能力２,
    B.能力３,
    B.能力４,
    B.能力５,
    B.能力６
FROM
QUERY_A A
	INNER JOIN QUERY_B B ON A.登番 = B.登番
	INNER JOIN QUERY_C C ON A.Ｍ番号 = C.Ｍ番号
'''


"""
【機　能】展示出走表
【変数名】race_table_sql3
【引　数】@yyyymmdd		開催年月日
　　　　　@poolcode		場コード
　　　　　@raceno		レース番号
"""
race_table_sql3 = '''
WITH QUERY_A AS (
    SELECT
        x_race_d.entry_no as 艇番,
        x_race_d.player_no as 登番,
        x_race_d.player_name as 選手名,
        x_race_d.class as 級別,
        x_race_d.area as 支部,
        x_race_d.age as 年齢,
        x_race_d.body_weight as 体重,
        x_race_d.flying_count as Ｆ数,
        x_race_d.lost_count as Ｌ数,
        x_race_d.st as ST,
        x_race_d.nationwide_win_rate as 全勝率,
        x_race_d.nationwide_double_rate as 全二連,
        x_race_d.nationwide_triple_rate as 全三連,
        x_race_d.local_win_rate as 当勝率,
        x_race_d.local_double_rate as 当二連,
        x_race_d.local_triple_rate as 当三連,
        x_race_d.motor_no as Ｍ番号,
        x_race_d.motor_double_rate as Ｍ二連,
        x_race_d.motor_triple_rate as Ｍ三連,
        x_race_d.boat_no as Ｂ番号,
        x_race_d.boat_double_rate as Ｂ二連,
        x_race_d.boat_triple_rate as Ｂ三連	
    FROM x_race_t, x_race_h,x_race_d
    WHERE x_race_t.yyyymmdd =  '@yyyymmdd' AND x_race_t.pool_code = '@poolcode' AND x_race_h.race_no = '@raceno'
    AND (x_race_t.yyyymmdd = x_race_h.yyyymmdd AND x_race_t.pool_code = x_race_h.pool_code)
    AND (x_race_h.yyyymmdd = x_race_d.yyyymmdd AND x_race_h.pool_code = x_race_d.pool_code AND x_race_h.race_no = x_race_d.race_no)
    ORDER by x_race_t.yyyymmdd ASC, x_race_t.pool_code ASC, x_race_h.race_no ASC,x_race_d.entry_no ASC
),QUERY_B AS (
	SELECT * FROM (
		SELECT
			t_index.player_no as 登番,
			t_index.yyyymmdd as 日付,
			t_index.pool_code as 場コード,
			t_index.race_no as レース番号,
			t_index.entry_no as 艇番,
			t_index.motor_no as Ｍ番号,
			ROUND(t_index.ability, 1) as 能力,
			t_index.st as ST,
			ROUND(t_index.ability2, 1) as 直近能力,
			t_index.st2 as 直近ST,
			ROUND(t_index.ability_course_1, 1) as 能力１,
			ROUND(t_index.ability_course_2, 1) as 能力２,
    	    ROUND(t_index.ability_course_3, 1) as 能力３,
        	ROUND(t_index.ability_course_4, 1) as 能力４,
            ROUND(t_index.ability_course_5, 1) as 能力５,
            ROUND(t_index.ability_course_6, 1) as 能力６,
            ROUND(t_index.sinnyu_course_1, 1)  as 進入１,
            ROUND(t_index.sinnyu_course_2, 1)  as 進入２,
            ROUND(t_index.sinnyu_course_3, 1)  as 進入３,
            ROUND(t_index.sinnyu_course_4, 1)  as 進入４,
            ROUND(t_index.sinnyu_course_5, 1)  as 進入５,
            ROUND(t_index.sinnyu_course_6, 1)  as 進入６,
			ROUND(t_index.nige_win_rate_course_1, 1) as 逃げ率１,
			ROUND(t_index.makuri_lost_rate_course_1, 1) as まくられ率１,
			ROUND(t_index.sashi_lost_rate_course_1, 1)as 差され率１,
			ROUND(t_index.nige_lost_rate_course_2, 1)as 逃し率２,
			ROUND(t_index.makuri_win_rate_course_2, 1) as まくり率２,
			ROUND(t_index.sashi_win_rate_course_2, 1) as 差し率２,
			ROUND(t_index.makuri_win_rate_course_3, 1) as まくり率３,
			ROUND(t_index.sashi_win_rate_course_3, 1) as 差し率３,
			ROUND(t_index.makuri_win_rate_course_4, 1) as まくり率４,
			ROUND(t_index.sashi_win_rate_course_4, 1) as 差し率４,
			ROUND(t_index.makuri_win_rate_course_5, 1) as まくり率５,
			ROUND(t_index.sashi_win_rate_course_5, 1) as 差し率５,
			ROUND(t_index.makuri_win_rate_course_6, 1) as まくり率６,
			ROUND(t_index.sashi_win_rate_course_6, 1) as 差し率６
		FROM
			t_index
		WHERE t_index.player_no in  (SELECT  x_race_d.player_no FROM x_race_d WHERE x_race_d.yyyymmdd =  '@yyyymmdd' AND x_race_d.pool_code = '@poolcode' AND x_race_d.race_no = '@raceno')
		ORDER BY t_index.player_no ASC,t_index.yyyymmdd DESC, t_index.race_no DESC
    ) GROUP BY 登番
),QUERY_C AS (
	SELECT * FROM (
		SELECT
			t_index.motor_no as Ｍ番号,
			ROUND(t_index.rate_win_motor, 1) as Ｍ能力,
			ROUND(t_index.rate_win_motor_course1, 1) as Ｍ能力１,
			ROUND(t_index.rate_win_motor_course2, 1) as Ｍ能力２,
			ROUND(t_index.rate_win_motor_course3, 1) as Ｍ能力３,
			ROUND(t_index.rate_win_motor_course4, 1) as Ｍ能力４,
			ROUND(t_index.rate_win_motor_course5, 1) as Ｍ能力５,
			ROUND(t_index.rate_win_motor_course6, 1) as Ｍ能力６
		FROM
			t_index
		WHERE t_index.motor_no in  (SELECT  x_race_d.motor_no FROM x_race_d WHERE x_race_d.yyyymmdd =  '@yyyymmdd' AND x_race_d.pool_code = '@poolcode' AND x_race_d.race_no = '@raceno')
		ORDER BY t_index.motor_no  ASC,t_index.yyyymmdd DESC, t_index.race_no DESC
    ) GROUP BY Ｍ番号
)
SELECT
    (A.艇番 || "号艇[" || A.級別 || "][" || A.登番 || "]" || A.選手名) as 選手,
	B.能力,
    B.直近能力,
	B.直近ST,
	C.Ｍ能力,
    B.能力１,
    B.能力２,
    B.能力３,
    B.能力４,
    B.能力５,
    B.能力６,
    B.逃げ率１,
    B.まくられ率１,
    B.差され率１,
    B.逃し率２,
	B.まくり率２,
	B.差し率２,
    B.まくり率３,
    B.差し率３,
    B.まくり率４,
    B.差し率４,
    B.まくり率５,
    B.差し率５,
    B.まくり率６,
    B.差し率６,
    C.Ｍ能力１,
    C.Ｍ能力２,
    C.Ｍ能力３,
    C.Ｍ能力４,
    C.Ｍ能力５,
    C.Ｍ能力６
FROM
QUERY_A A
	INNER JOIN QUERY_B B ON A.登番 = B.登番
	INNER JOIN QUERY_C C ON A.Ｍ番号 = C.Ｍ番号
'''


