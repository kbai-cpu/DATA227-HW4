import streamlit as st
import pandas as pd
import numpy as np
from vega_datasets import data

@st.cache_data
def load_pl_data() -> tuple:
    season_2324 = pd.read_csv('data/PL-season-2324.csv')
    season_2425 = pd.read_csv('data/PL-season-2425.csv')
    season_2324['Season'] = '2023-24'
    season_2425['Season'] = '2024-25'

    # ── Q1: team_summary_long ────────────────────────────────────────────────
    def _split_home_away(season_df):
        home = season_df.assign(
            Team=season_df['HomeTeam'],
            GoalsScored=season_df['FTHG'],
            GoalsConceded=season_df['FTAG'],
            Win=(season_df['FTR'] == 'H').astype(int),
            Draw=(season_df['FTR'] == 'D').astype(int),
            Loss=(season_df['FTR'] == 'A').astype(int),
            Points=((season_df['FTR'] == 'H') * 3 + (season_df['FTR'] == 'D') * 1),
        )[['Team', 'Season', 'GoalsScored', 'GoalsConceded', 'Win', 'Draw', 'Loss', 'Points']]

        away = season_df.assign(
            Team=season_df['AwayTeam'],
            GoalsScored=season_df['FTAG'],
            GoalsConceded=season_df['FTHG'],
            Win=(season_df['FTR'] == 'A').astype(int),
            Draw=(season_df['FTR'] == 'D').astype(int),
            Loss=(season_df['FTR'] == 'H').astype(int),
            Points=((season_df['FTR'] == 'A') * 3 + (season_df['FTR'] == 'D') * 1),
        )[['Team', 'Season', 'GoalsScored', 'GoalsConceded', 'Win', 'Draw', 'Loss', 'Points']]

        return pd.concat([home, away], ignore_index=True)

    team_matches = pd.concat(
        [_split_home_away(season_2324), _split_home_away(season_2425)],
        ignore_index=True,
    )
    team_summary = (
        team_matches
        .groupby(['Team', 'Season'], as_index=False)
        .agg({'Points': 'sum', 'Win': 'sum', 'GoalsScored': 'sum', 'GoalsConceded': 'sum'})
    )
    team_summary['GoalDiff'] = team_summary['GoalsScored'] - team_summary['GoalsConceded']
    team_summary_long = team_summary.melt(
        id_vars=['Team', 'Season'],
        value_vars=['Points', 'Win', 'GoalDiff'],
        var_name='Metric',
        value_name='Value',
    )

    # ── Q2: team_attack_long ─────────────────────────────────────────────────
    matches = pd.concat([season_2324, season_2425], ignore_index=True)
    home_attack = matches.assign(
        Team=matches['HomeTeam'], Goals=matches['FTHG'],
        Shots=matches['HS'], ShotsOnTarget=matches['HST'], Corners=matches['HC'],
    )[['Team', 'Season', 'Date', 'Goals', 'Shots', 'ShotsOnTarget', 'Corners']]
    away_attack = matches.assign(
        Team=matches['AwayTeam'], Goals=matches['FTAG'],
        Shots=matches['AS'], ShotsOnTarget=matches['AST'], Corners=matches['AC'],
    )[['Team', 'Season', 'Date', 'Goals', 'Shots', 'ShotsOnTarget', 'Corners']]

    team_match_attack = pd.concat([home_attack, away_attack], ignore_index=True)
    team_match_attack['Date'] = pd.to_datetime(team_match_attack['Date'], format='%d/%m/%y')
    team_match_attack = team_match_attack.sort_values(['Team', 'Season', 'Date'])
    team_match_attack['Matchweek'] = (
        team_match_attack.groupby(['Team', 'Season']).cumcount() + 1
    )
    for col in ['Goals', 'Shots', 'ShotsOnTarget']:
        team_match_attack[f'{col}_roll3'] = (
            team_match_attack.groupby(['Team', 'Season'])[col]
            .transform(lambda x: x.rolling(window=3, min_periods=1).mean())
        )
    team_attack_long = team_match_attack.melt(
        id_vars=['Team', 'Season', 'Matchweek'],
        value_vars=['Goals_roll3', 'Shots_roll3', 'ShotsOnTarget_roll3'],
        var_name='Metric',
        value_name='RollingValue',
    )
    team_attack_long['Metric'] = team_attack_long['Metric'].str.replace('_roll3', '', regex=False)

    # ── Q3: q3_pivot ─────────────────────────────────────────────────────────
    venue_rows = pd.concat([
        pd.DataFrame({
            'Team': season_2324['HomeTeam'], 'Season': '2023-24', 'Venue': 'Home',
            'GoalsScored': season_2324['FTHG'], 'GoalsConceded': season_2324['FTAG'],
            'Points': np.where(season_2324['FTR'] == 'H', 3, np.where(season_2324['FTR'] == 'D', 1, 0)),
        }),
        pd.DataFrame({
            'Team': season_2324['AwayTeam'], 'Season': '2023-24', 'Venue': 'Away',
            'GoalsScored': season_2324['FTAG'], 'GoalsConceded': season_2324['FTHG'],
            'Points': np.where(season_2324['FTR'] == 'A', 3, np.where(season_2324['FTR'] == 'D', 1, 0)),
        }),
        pd.DataFrame({
            'Team': season_2425['HomeTeam'], 'Season': '2024-25', 'Venue': 'Home',
            'GoalsScored': season_2425['FTHG'], 'GoalsConceded': season_2425['FTAG'],
            'Points': np.where(season_2425['FTR'] == 'H', 3, np.where(season_2425['FTR'] == 'D', 1, 0)),
        }),
        pd.DataFrame({
            'Team': season_2425['AwayTeam'], 'Season': '2024-25', 'Venue': 'Away',
            'GoalsScored': season_2425['FTAG'], 'GoalsConceded': season_2425['FTHG'],
            'Points': np.where(season_2425['FTR'] == 'A', 3, np.where(season_2425['FTR'] == 'D', 1, 0)),
        }),
    ], ignore_index=True)

    q3_summary = (
        venue_rows
        .groupby(['Team', 'Season', 'Venue'], as_index=False)
        .agg({'Points': 'sum', 'GoalsScored': 'sum', 'GoalsConceded': 'sum'})
    )
    q3_summary['GoalDiff'] = q3_summary['GoalsScored'] - q3_summary['GoalsConceded']
    q3_pivot = q3_summary.pivot(
        index=['Team', 'Season'], columns='Venue', values=['Points', 'GoalDiff'],
    ).reset_index()
    q3_pivot.columns = [
        '_'.join(col).strip('_') if isinstance(col, tuple) else col
        for col in q3_pivot.columns
    ]
    q3_pivot['HomeAdvantage'] = q3_pivot['Points_Home'] - q3_pivot['Points_Away']

    return team_summary_long, team_attack_long, q3_pivot


@st.cache_data
def load_weather() -> pd.DataFrame:
    df = data.seattle_weather()
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%b")
    return df
