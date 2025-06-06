import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_overall_winrate(df):
    """
    全体の勝率を計算する関数。

    Parameters:
        df (pandas.DataFrame): 'win'列を含むデータフレーム。'win'は1（勝ち）または0（負け）を想定。

    Returns:
        float: 全体の勝率（%表示）
    """
    return df['win'].mean() * 100

def calculate_deck_winrate(df):
    """
    デッキごとの勝率を計算する。

    Parameters:
        df (pandas.DataFrame): 'my_deck'（自分のデッキ）と 'win'（勝敗: 1 or 0）を含むデータフレーム。

    Returns:
        pandas.Series: 各デッキごとの勝率（％）を格納したSeries。デッキ名がインデックス。
    """
    return df.groupby('my_deck')['win'].mean().round(3) * 100


def draw_deck_winrate_bar_chart(sorted_winrate):
    """
    デッキごとの勝率を棒グラフで可視化する。

    Parameters:
        sorted_winrate (pandas.Series): デッキ名をインデックス、勝率（％）を値とするSeries。昇順・降順は問わない。

    Returns:
        None: グラフを表示するだけで、戻り値はなし。
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(x=sorted_winrate.values, y=sorted_winrate.index, palette="Blues_d")
    plt.xlabel("Win Rate (%)")
    plt.ylabel("My Deck")
    plt.title("Win Rate by My Deck")
    plt.tight_layout()
    plt.show()

def draw_matchup_heatmap(df):
    """
    自分のデッキと相手のデッキの勝率をヒートマップで可視化する。

    Parameters:
        df (pandas.DataFrame): 対戦データ（列に 'my_deck', 'opponent_deck', 'win' を含む）

    Returns:
        None: グラフを表示するだけで、戻り値はなし。
    """
    pivot_table = df.pivot_table(index="my_deck", columns="opponent_deck", values="win", aggfunc="mean")
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="coolwarm", cbar=True)
    plt.title("Win Rate Heatmap (My Deck vs Opponent Deck)")
    plt.xlabel("Opponent Deck")
    plt.ylabel("My Deck")
    plt.tight_layout()
    plt.show()

def get_best_deck(df):
    """
    指定されたデータフレームから、対戦回数が2回以上あるデッキの中で
    最も勝率の高いデッキ名とその勝率を返します。

    Parameters
    ----------
    df : pandas.DataFrame
        'my_deck'列にデッキ名、'win'列に勝敗(1=勝ち, 0=負け)が格納されたデータフレーム

    Returns
    -------
    tuple (str or None, float or None)
        最も勝率の高いデッキ名（str）と勝率（float）を返します。
        該当デッキがない場合は (None, None) を返します。
    """
    deck_stats = df.groupby('my_deck').agg({'win': ['mean', 'count']})
    deck_stats.columns = ['win_rate', 'count']
    filtered_stats = deck_stats[deck_stats['count'] >= 2]
    if not filtered_stats.empty:
        most_winning_deck = filtered_stats['win_rate'].idxmax()
        highest_win_rate = filtered_stats['win_rate'].max()
        return most_winning_deck, highest_win_rate
    else:
        return None, None
