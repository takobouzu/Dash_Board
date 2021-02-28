/*
【ファイル】 本日の逃げ予想.sql
【機能仕様】 各レースの１号艇の能力値が１位で逃げ勝率が57.0を上回る選手を抽出
【パラメタ】 @yyyymmdd 出走表で選択した日付
*/

/* 検索SQL */
WITH QUERY_A AS (
    SELECT
        x_race_t.yyyymmdd as 年月日,
        x_race_t.pool_code as 場コード,
        x_race_t.pool_name as 場名,
        x_race_t.grade as グレード,
        x_race_t.holding as 開催区分,
        x_race_t.title as タイトル,
        x_race_t.event_date as 開催日,
        x_race_h.race_no as レース番号,
        x_race_h.scheduled_deadline as 投票締切時刻,
        x_race_h.race_name as レース名,
        x_race_d.entry_no as 艇番,
        x_race_d.player_no as 選手登録番号,
        x_race_d.player_name as 選手名,
        x_race_d.class as 級別,
        x_race_d.area as 支部,
        x_race_d.player_native_place	as 出身地,
        x_race_d.age as 年齢,
        x_race_d.body_weight as 体重,
        x_race_d.flying_count as フライング回数,
        x_race_d.lost_count as 出遅れ回数,
        x_race_d.st as 平均スタートタイミング,
        x_race_d.nationwide_win_rate as 全国勝率,
        x_race_d.nationwide_double_rate as 全国二連率,
        x_race_d.nationwide_triple_rate as 全国三連率,
        x_race_d.local_win_rate as 当地勝率,
        x_race_d.local_double_rate as 当地二連率,
        x_race_d.local_triple_rate as 当地三連率,
        x_race_d.motor_no as モーター番号,
        x_race_d.motor_double_rate as モーター二連率,
        x_race_d.motor_triple_rate as モーター三連率,
        x_race_d.boat_no as ボート番号,
        x_race_d.boat_double_rate as ボート二連率,
        x_race_d.boat_triple_rate as ボート三連率	
    FROM x_race_t, x_race_h,x_race_d
    WHERE x_race_t.yyyymmdd =  '@yyyymmdd'
    AND (x_race_t.yyyymmdd = x_race_h.yyyymmdd AND x_race_t.pool_code = x_race_h.pool_code)
    AND (x_race_h.yyyymmdd = x_race_d.yyyymmdd AND x_race_h.pool_code = x_race_d.pool_code AND x_race_h.race_no = x_race_d.race_no)
    ORDER by x_race_t.yyyymmdd ASC, x_race_t.pool_code ASC, x_race_h.race_no ASC,x_race_d.entry_no ASC
),QUERY_B AS (
	SELECT * FROM (
		SELECT
			t_index.player_no as 選手登録番号,
			t_index.ability as 能力指数,
			t_index.st as 平均ST,
			t_index.ability_count as 出走数,
			t_index.ability2 as 直近・能力指数,
			t_index.st2 as 直近・平均ST,
			t_index.ability2_count as 直近・出走数,
			t_index.rate_win_motor as 直近・モーター勝率,
			t_index.rate_win_count as 直近・勝率,
			t_index.motor_count1 as モーター・出走数・１コース,
			t_index.motor_count2 as モーター・出走数・２コース,
			t_index.motor_count3 as モーター・出走数・３コース,
			t_index.motor_count4 as モーター・出走数・４コース,
			t_index.motor_count5 as モーター・出走数・５コース,
			t_index.motor_count6 as モーター・出走数・６コース,
			t_index.rate_win_motor_course1 as モーター・勝率・１コース,
			t_index.rate_win_motor_course2 as モーター・勝率・２コース,
			t_index.rate_win_motor_course3 as モーター・勝率・３コース,
			t_index.rate_win_motor_course4 as モーター・勝率・４コース,
            t_index.rate_win_motor_course5 as モーター・勝率・５コース,
			t_index.rate_win_motor_course6 as モーター・勝率・６コース,
			t_index.course_count_1 as 出走数・１コース,
			t_index.ability_course_1 as 能力指数・１コース,
			t_index.sinnyu_course_1 as 進入偏差・１コース,
			t_index.nige_win_count_course_1 as 逃げ勝数・１コース,
			t_index.nige_win_rate_course_1 as 逃げ勝率・１コース,
			t_index.makuri_lost_count_course_1 as まくられ数・１コース,
			t_index.makuri_lost_rate_course_1 as まくられ率・１コース,
			t_index.sashi_lost_count_course_1 as 差され数・１コース,
			t_index.sashi_lost_rate_course_1 as 差され率・１コース,
			t_index.course_count_2 as 出走数・２コース,
			t_index.ability_course_2 as 能力指数・２コース,
			t_index.sinnyu_course_2 as 進入偏差・２コース,
			t_index.nige_lost_count_course_2 as 逃し数・２コース,
			t_index.nige_lost_rate_course_2 as 逃し率・２コース,
			t_index.makuri_win_count_course_2 as まくり勝数・２コース,
			t_index.makuri_win_rate_course_2 as まくり率・２コース,
			t_index.sashi_win_count_course_2 as 差し勝数・２コース,
			t_index.sashi_win_rate_course_2 as 差し率・２コース,
			t_index.course_count_3 as 出走数・３コース,
			t_index.ability_course_3 as 能力指数・３コース,
			t_index.sinnyu_course_3 as 進入偏差・３コース,
			t_index.makuri_win_count_course_3 as まくり勝数・３コース,
			t_index.makuri_win_rate_course_3 as まくり率・３コース,
			t_index.sashi_win_count_course_3 as 差し勝数・３コース,
			t_index.sashi_win_rate_course_3 as 差し率・３コース,
			t_index.course_count_4 as 出走数・４コース,
			t_index.ability_course_4 as 能力指数・４コース,
			t_index.sinnyu_course_4 as 進入偏差・４コース,
			t_index.makuri_win_count_course_4 as まくり勝数・４コース,
			t_index.makuri_win_rate_course_4 as まくり率・４コース,
			t_index.sashi_win_count_course_4 as 差し勝数・４コース,
			t_index.sashi_win_rate_course_4 as 差し率・４コース,
			t_index.course_count_5 as 出走数・５コース,
			t_index.ability_course_5 as 能力指数・５コース,
			t_index.sinnyu_course_5 as 進入偏差・５コース,
			t_index.makuri_win_count_course_5 as まくり勝数・５コース,
			t_index.makuri_win_rate_course_5 as まくり率・５コース,
			t_index.sashi_win_count_course_5 as 差し勝数・５コース,
			t_index.sashi_win_rate_course_5 as 差し率・５コース,
			t_index.course_count_6 as 出走数・６コース,
			t_index.ability_course_6 as 能力指数・６コース,
			t_index.sinnyu_course_6 as 進入偏差・６コース,
			t_index.makuri_win_count_course_6 as まくり勝数・６コース,
			t_index.makuri_win_rate_course_6 as まくり率・６コース,
			t_index.sashi_win_count_course_6 as 差し勝数・６コース,
			t_index.sashi_win_rate_course_6 as 差し率・６コース
		FROM
			t_index
		ORDER BY t_index.player_no ASC,t_index.yyyymmdd DESC, t_index.race_no DESC
    ) GROUP BY 選手登録番号
)

SELECT * FROM
 (
    SELECT
	    ("[" || 場名 || "] "|| レース番号 || "R " || 艇番 || "号艇[" || 選手登録番号 || "][" || 級別 || "] " || 選手名) as レース情報,投票締切時刻,場名,グレード,タイトル,開催日,レース番号,レース名,艇番,選手登録番号,選手名,級別, 直近・能力指数,逃げ勝率・１コース,
		ROW_NUMBER() OVER (
            PARTITION BY
                年月日,場コード,レース番号
            ORDER BY
                直近・能力指数 DESC
         ) AS 能力順位
    FROM
		(SELECT * FROM (QUERY_A A INNER JOIN QUERY_B B ON A.選手登録番号 = B.選手登録番号))
    
) AS  出走表
WHERE
    出走表.能力順位 = 1 AND 出走表.艇番 = 1 AND 出走表.逃げ勝率・１コース > 57.0
ORDER BY
    投票締切時刻