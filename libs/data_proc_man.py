''' Here, the objective is to build a framework
to deal with the data processing and manipulation
applied to our problem: the data related to the
WC matches history '''

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from libs.data_loading import create_df_new
from libs.data_vis_und import NonNumerical_based, Numerical_based

df = create_df_new()

# Definition of the different types of ndarray that will be used in the processing and manipulation section.

# Instantiating the classes:

numerical_object = Numerical_based(["home_team_goals", "away_team_goals"])
non_numerical_object = NonNumerical_based()

def goals_per_game_ndarray():
    goals_per_game = list(df[numerical_object.dataframe_numerical].sum(axis = 1))
    goals_per_game = np.array(goals_per_game)
    return goals_per_game

def games_played_per_team_ndarray():
    games_played_per_team = non_numerical_object.games_played().fillna(0).values
    return games_played_per_team

def victories_per_team_ndarray():
    victories_per_team_aux = non_numerical_object.victories_per_team().fillna(0).values
    return victories_per_team_aux

def losses_per_team_ndarray():
    losses_per_team_aux = non_numerical_object.losses_per_team().fillna(0).values
    return losses_per_team_aux

def goals_per_team_ndarray():
    goals_per_team_aux = []

    for i in range(86):
        goals_per_team_aux.append(non_numerical_object.goals_per_team()[i][1])
        
    goals_per_team_aux = np.array(goals_per_team_aux)
    return goals_per_team_aux

# Definition of the discretization function:

def discretization(x):
    if x < 0.33:
        return "low"
    elif 0.33 <= x < 0.67:
        return "medium"
    else:
        return "high"
    
# Class that will treat about the Outlier detection and removal, as well as scaling the data:

class Outlier_Scaling:
    def __init__(self, ndarray, ndarray_normal = 0):
        self.ndarray = ndarray
        self.ndarray_normal = ndarray_normal 

    def outlier_detection_removal(self):
        condition = (self.ndarray < self.ndarray.mean() - 3*self.ndarray.std()) | (self.ndarray > self.ndarray.mean() + 3*self.ndarray.std()) 

        ndarray_set = set(self.ndarray[condition])

        list_indexes = []

        for i in ndarray_set:
            list_indexes.append(np.where(self.ndarray == i))

        cont_index = []

        for i in list_indexes:
            for j in i:
                for k in j:
                    cont_index.append(k)
        
        self.ndarray = np.delete(self.ndarray, cont_index)

    def box_plots(self):
        plt.boxplot(self.ndarray)
        plt.ylabel("Goals per game")
        plt.title("World Cup History")

    def kde_plots(self):
        sns.displot(self.ndarray, kind = "kde")

    def hist_plots(self):
        sns.displot(self.ndarray, kind = "hist")

    def kde_plots_scaled(self):
        sns.displot(self.ndarray_normal, kind = "kde")

    def hist_plots_scaled(self):
        sns.displot(self.ndarray_normal, kind = "hist")
    
    def box_plots_scaled(self):
        plt.boxplot(self.ndarray_normal)
        plt.ylabel("Goals per game")
        plt.title("World Cup History")

    def scaling(self):
        self.ndarray_normal = (self.ndarray - self.ndarray.min())/(self.ndarray.max() - self.ndarray.min())

    def series_discretization(self):
        self.scaling()
        list_values_disc = []

        for i in self.ndarray_normal:
            list_values_disc.append(discretization(i))

        series = pd.Series(list_values_disc, index = self.ndarray)
        return series

if __name__ == "__main__":
    print("A library to process and manipulate data from the WC matches history.\n")
