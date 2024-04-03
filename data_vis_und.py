''' Here, the objective is to build a pipeline to deal with the
data visualization and understanding. This pipeline will be applied
to the problem in focus, that is, the analysis of the WC matches
history. '''

from data_loading import create_df_new
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Auxiliary definitions for the plots class:

list_years = df["year"].unique()
list_goals = []

for i in list_years:
    list_goals.append(df[df["year"] == i][["home_team_goals", "away_team_goals"]].values.sum())

# Definition of the numerical columns:
#    
# numerical = ["home_team_goals", "away_team_goals"]
#

# Classes about data understanding:    

class NonNumerical_based:
    def __init__(self):
        pass

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
    def __init__(self, numerical):
        self.dataframe_numerical = numerical

    def central_tedency_all(self):
        for i in self.dataframe_numerical :
            central_tedency(i)
    
    def dispersion_all(self):
        for i in self.dataframe_numerical :
            dispersion(i)

    def pivot_table(self):
        df_pivot = df.pivot_table(values = ["home_team_goals", "away_team_goals"], index = ["year", "home_team_names", "away_team_names"])
        print("Using the home teams as metric:\n")
        display(df_pivot.sort_values(by = "home_team_goals", ascending = False))

        print("Using the away teams as metric:\n")
        display(df_pivot.sort_values(by = "away_team_goals", ascending = False))

    def goals_per_game_stat(self):
        goals_per_game = list(df[self.dataframe_numerical].sum(axis = 1))
        goals_per_game = np.array(goals_per_game)

        print(f"Total number of goals in all matches at WC history: {goals_per_game.sum()}\nMean of goals per game: {goals_per_game.mean()}\nStandard Deviation of goals per game: {goals_per_game.std()}\nVariance of goals per game: {goals_per_game.var()}\nMaximum number of goals per game: {goals_per_game.max()}")

# Class about data vis

class Plots(NonNumerical_based):
    def __init__(self):
        pass

    def plot_victories(self):
        vic_team = self.victories_per_team()
        series_aux_vic = pd.Series(range(1, 66), list(vic_team.index))

        list_aux_vic = list(zip(range(1, 66), list(vic_team.index)))

        print("According to the following relationship between the number and the teams, we have:")
        print(list_aux_vic)
        plt.figure(figsize = (20,20))
        plt.plot(series_aux_vic.values, vic_team.fillna(0).values, "*--b",  ms = 8)
        plt.xticks(np.arange(1, 66, 1))
        plt.xlabel("Indexes of the teams")
        plt.ylabel("Number of victories")
        plt.title("Victories")
        plt.plot()

    def plot_loss(self):
        loss_team = self.losses_per_team()
        series_aux_loss = pd.Series(range(1, 87), list(loss_team.index))

        list_aux_loss = list(zip(range(1, 87), list(loss_team.index)))

        print("According to the following relationship between the number and the teams, we have:")
        print(list_aux_loss)
        plt.figure(figsize = (25,25))
        plt.plot(series_aux_loss.values, loss_team.fillna(0).values, "*--r",  ms = 8)
        plt.xticks(np.arange(1, 87, 1))
        plt.xlabel("Indexes of the teams")
        plt.ylabel("Number of losses")
        plt.title("Losses")
        plt.plot()

    def games_plot(self):
        teams = self.games_played()
        series_aux_teams = pd.Series(range(1, 87), teams.index)

        list_aux_teams = list(zip(range(1, 87), teams.index))

        print("According to the following relationship between the number and the teams, we have:")
        print(list_aux_teams)
        plt.figure(figsize = (25,25))
        plt.plot(series_aux_teams.values, teams.fillna(0).values, "*--g",  ms = 8)
        plt.xticks(np.arange(1, 87, 1))
        plt.xlabel("Indexes of the teams")
        plt.ylabel("Number of games")
        plt.title("Games played by each team")        
        plt.plot()

    def goals_plot(self):
        plt.figure(figsize = (20,20))
        plt.plot(list_years, list_goals, "^",  ms = 12)
        plt.xticks(list_years)
        plt.xlabel("Editions of WC")
        plt.ylabel("Goals")
        plt.title("Number of goals in each edition")
        plt.plot()

    def goals_reg_plot(self):
        sns.jointplot(x = list_years, y = list_goals, kind = "reg")
    
    def number_of_trophies_plot(self):
        winners = ["Spain", "England", "Uruguay", "France", "Argentina", "Italy", "Germany", "Brazil"]
        titles = [1, 1, 2, 2, 2, 4, 4, 5]

        plt.plot(winners, titles, "*", ms = 10)
        plt.title("Winners of WC")
        plt.xlabel("Winners")
        plt.ylabel("Titles")
        plt.plot()

if __name__ == "__main__":
    print("A library to realize data understanding and visualization about WC matches.\n")

 

