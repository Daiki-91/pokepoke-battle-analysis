import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_overall_winrate(df):
    return df['win'].mean() * 100

def calculate_deck_winrate(df):
    return df.groupby('my_deck')['win'].mean().round(1) * 100

def draw_deck_winrate_bar_chart(sorted_winrate):
    # グラフ描画
    pass

def draw_matchup_heatmap(df):
    # グラフ描画
    pass

def get_best_deck(df):
    deck_stats = df.groupby('my_deck').agg({'win': ['mean', 'count']})
    deck_stats.columns = ['win_rate', 'count']
    filtered_stats = deck_stats[deck_stats['count'] >= 2]
    if not filtered_stats.empty:
        most_winning_deck = filtered_stats['win_rate'].idxmax()
        highest_win_rate = filtered_stats['win_rate'].max()
        return most_winning_deck, highest_win_rate
    else:
        return None, None
