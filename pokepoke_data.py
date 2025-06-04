import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

# --- 日本語フォント設定（macOS向け） ---
plt.rcParams['font.family'] = 'Hiragino Sans'
plt.rcParams['axes.unicode_minus'] = False  # マイナス符号の文字化け対策

# --- CSV読み込み（1行目をスキップ） ---
df = pd.read_csv('pokepoke_battle_data.csv', encoding='utf-8-sig', skiprows=1)

# --- カラム名の確認と変換 ---
df.rename(columns={
    '使用デッキ': 'my_deck',
    '相手デッキ': 'opponent_deck',
    '勝敗': 'result',
    '日付': 'date',
    'ランク': 'rank',
    '自分の先攻/後攻': 'turn_order'
}, inplace=True)

# --- 勝敗を数値化（勝ち=1, 負け=0） ---
df['win'] = df['result'].apply(lambda x: 1 if x == '勝ち' else 0)

# --- 全体勝率 ---
overall_winrate = df['win'].mean() * 100
print(f"\n全体勝率：{overall_winrate:.1f}%")

# --- デッキ別勝率 ---
deck_winrate = df.groupby('my_deck')['win'].mean().round(1) * 100
sorted_winrate = deck_winrate.sort_values(ascending=False)

print("\nデッキ別勝率：")
print(deck_winrate.astype(str) + "%")

# --- 勝率グラフ（オシャレver） ---
fig, ax = plt.subplots(figsize=(10, 6))
colors = plt.cm.viridis(sorted_winrate.values / 100)
bars = ax.bar(sorted_winrate.index, sorted_winrate.values, color=colors)

ax.set_title('デッキ別勝率', fontsize=16, fontweight='bold')
ax.set_ylabel('勝率（%）', fontsize=12)
ax.set_xlabel('デッキ名', fontsize=12)
ax.set_ylim(0, max(sorted_winrate.values) + 10)
plt.xticks(rotation=45, ha='right')

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 1, f'{height:.1f}%', 
            ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()

# --- デッキごとの相性ヒートマップ（勝率%） ---
matchup = df.groupby(['my_deck', 'opponent_deck'])['win'].mean().unstack() * 100

fig, ax = plt.subplots(figsize=(16, 10))

sns.heatmap(matchup, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.5, 
            linecolor='gray', cbar_kws={'label': '勝率％'},
            mask=matchup.isnull(), square=True, ax=ax)

ax.set_title("デッキごとの相性（勝率％）", fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel("相手デッキ", fontsize=12)
ax.set_ylabel("自分のデッキ", fontsize=12)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

# 余白をバランスよく調整
fig.subplots_adjust(top=0.90, bottom=0.30, left=0.20, right=0.90)

plt.show()

# --- 最も勝率が高いデッキ（試合数2試合以上） ---
deck_stats = df.groupby('my_deck').agg({'win': ['mean', 'count']})
deck_stats.columns = ['win_rate', 'count']
filtered_stats = deck_stats[deck_stats['count'] >= 2]

if not filtered_stats.empty:
    most_winning_deck = filtered_stats['win_rate'].idxmax()
    highest_win_rate = filtered_stats['win_rate'].max()
    print(f"\n最も勝率が高いデッキ：{most_winning_deck}（勝率：{highest_win_rate:.1%}）")
else:
    print("\nデータ不足のため、最も勝率が高いデッキを特定できませんでした。")
