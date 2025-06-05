import pandas as pd
from pokepoke_functions import calculate_overall_winrate, calculate_deck_winrate, get_best_deck

def test_calculate_overall_winrate():
    df = pd.DataFrame({'win': [1, 0, 1, 1]})
    assert calculate_overall_winrate(df) == 75.0

def test_calculate_deck_winrate():
    df = pd.DataFrame({
        'my_deck': ['A', 'A', 'B', 'B'],
        'win': [1, 0, 1, 1]
    })
    result = calculate_deck_winrate(df)
    assert result['A'] == 50.0
    assert result['B'] == 100.0

def test_get_best_deck():
    df = pd.DataFrame({
        'my_deck': ['A', 'A', 'B', 'B', 'C'],
        'win': [1, 0, 1, 1, 1]
    })
    best_deck, winrate = get_best_deck(df)
    assert best_deck == 'B'
    assert winrate == 1.0
