import pandas as pd
import sqlite3

# 1行目が「pokepoke_battle_data」という不要行なのでスキップする
df = pd.read_csv("pokepoke_battle_data.csv", skiprows=1)

print(df.head())  # 読み込み確認

# SQLiteデータベースに接続
conn = sqlite3.connect("battles.db")

# テーブル名は "battles" にする（好きな名前でOK）
df.to_sql("battles", conn, if_exists="replace", index=False)

# カーソル取得
cur = conn.cursor()

# SQLクエリを文字列で定義
query = """
SELECT
    使用デッキ,
    COUNT(*) AS 対戦数,
    SUM(CASE WHEN 勝敗 = '勝ち' THEN 1 ELSE 0 END) AS 勝ち数,
    ROUND(CAST(SUM(CASE WHEN 勝敗 = '勝ち' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*), 2) AS 勝率
FROM
    battles
GROUP BY
    使用デッキ
ORDER BY
    勝率 DESC;
"""

print("【デッキ別 勝率一覧】")
for row in cur.execute(query):
    print(f"デッキ: {row[0]}｜対戦数: {row[1]}｜勝ち数: {row[2]}｜勝率: {row[3]*100:.2f}%")

conn.close()
