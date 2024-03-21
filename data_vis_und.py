from data_loading import create_df_new
import numpy as np
import pandas as pd

df = create_df_new()

# Function to see the which was the game with most goals in WC history:

def game_with_most_goals(df):
    for i, info in df.iterrows():
        if (info[2] + info[3] == 12):
            break
        
    print(f"{df.iloc[i].values[1]} x {df.iloc[i].values[4]}")

# Functions that will be used on the implementation of the class methods:

def central_tedency(col):
    minimum = df[col].min()
    maximum = df[col].max()
    midpoint = (maximum - minimum)/2
    median = df[col].median()
    mode = df[col].mode()[0]
    
    print(f"For column {col}, we have:")
    print(f"Min = {minimum}, Max = {maximum}, Midpoint = {midpoint}, Median = {median}, Mode = {mode}")

def dispersion(col):
    variance = df[col].var()
    std = df[col].std()
    quantiles = df[col].quantile([0.25, 0.5, 0.75])
    range = df[col].max() - df[col].min()
    
    print(f"For column {col}, we have:")
    print(f"Variance = {variance}, Std = {std}, First Quartile = {quantiles[0.25]}, Second Quartile = {quantiles[0.5]}, Third Quartile = {quantiles[0.75]}, Range = {range}")

# Definition of the numerical columns:
#    
# numerical = ["home_team_goals", "away_team_goals"]
#

# Classes about data understanding:    

class NonNumerical_based:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def all_teams(self):
        teams_wc_h = df["home_team_names"].unique()
        teams_wc_h = set(teams_wc_h)

        teams_wc_a = df["away_team_names"].unique()
        teams_wc_a = set(teams_wc_a)

        teams_wc = teams_wc_a | teams_wc_h
        return teams_wc
    
    def games_played(self):
        games_played = df["home_team_names"].value_counts() + df["away_team_names"].value_counts()
        return games_played
    
    def victories_per_team(self):
        victory_per_team = df["home_team_names"][df["victory"] == "home"].value_counts() + df["away_team_names"][df["victory"] == "away"].value_counts()
        return victory_per_team
    
    def losses_per_team(self):
        loss_per_team = df["home_team_names"][df["loss"] == "home"].value_counts() + df["away_team_names"][df["loss"] == "away"].value_counts()
        return loss_per_team
    
    def goals_per_team(self):
        list_goals = []

        for i in self.all_teams():
            list_goals.append(df["home_team_goals"][df["home_team_names"] == i].values.sum())

        goal_per_team = list(zip(list(self.all_teams()), list_goals))
        return goal_per_team
    
class Numerical_based:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def central_tedency_all(self, numerical):
        for i in numerical:
            central_tedency(i)
    
    def dispersion_all(self, numerical):
        for i in numerical:
            dispersion(i)

    def goals_per_game_stat(self):
        goals_per_game = list(df[["home_team_goals", "away_team_goals"]].sum(axis = 1))
        goals_per_game = np.array(goals_per_game)

        print(f"Total number of goals in all matches at WC history: {goals_per_game.sum()}\nMean of goals per game: {goals_per_game.mean()}\nStandard Deviation of goals per game: {goals_per_game.std()}\nVariance of goals per game: {goals_per_game.var()}\nMaximum number of goals per game: {goals_per_game.max()}")

if __name__ == "__main__":
    print("A library to realize data understanding about WC matches.\n")



