''' Here, the objective is to build the dataframe
that will be used for the data analysis. To do that,
we are going to lead a csv and complete the datafrane
with data from web scraping. '''

import pandas as pd
import numpy as np

# Uploading the CSV

df = pd.read_csv("world_cups/WorldCupMatches.csv")
df_util = df[["Year", "Home Team Name", "Home Team Goals", "Away Team Goals", "Away Team Name"]]
df_util = df_util.dropna()

# Web Scraping 

import requests
page = requests.get("https://terrikon.com/en/worldcup-2018")

# Create the Year Series

def df_year_series(df_util):
    array_1 = df_util["Year"].values
    array_int = array_1.astype("i")

    list_aux = list(array_int)
    for i in range(0,80):
        list_aux.append(2018)
        
    array_2 = np.array(list_aux)
    return pd.Series(array_2, index = range(0, len(list_aux)))

# Create the Home Team Names Series

def df_htn_series(df_util, list_1):
    list_home = []
    for i in range(0, 128, 2):
        list_home.append(list_1[i].get_text())

    array_htn = df_util["Home Team Name"].values   
    list_aux = list(array_htn)
    for i in (list_home[::-1]):
        list_aux.append(i)

    array_3 = np.array(list_aux)
    return pd.Series(array_3, index = range(0, len(list_aux)))

# Create the Home Team Goals Series

def df_htg_series(df_util, list_2):
    Home_Goals = []
    for i in range(len(list_2)):
        Home_Goals.append(list_2[i][0])

    array_htg = df_util["Home Team Goals"].values
    array_htg = array_htg.astype("i")   

    list_aux = list(array_htg)
    for i in (Home_Goals[::-1]):
        list_aux.append(i)

    array_4 = np.array(list_aux)
    array_4 = array_4.astype("i")
    return pd.Series(array_4, index = range(0, len(list_aux)))

# Create the Away Team Goals Series

def df_atg_series(df_util, list_2):
    Away_Goals = []
    for i in range(len(list_2)):
        Away_Goals.append(list_2[i][2])

    array_atg = df_util["Away Team Goals"].values
    array_atg = array_atg.astype("i")

    list_aux = list(array_atg)
    for i in (Away_Goals[::-1]):
        list_aux.append(i)

    array_5 = np.array(list_aux)
    array_5 = array_5.astype("i")
    return pd.Series(array_5, index = range(0, len(list_aux)))

# Create the Away Team Names Series

def df_atn_series(df_util, list_1):
    list_away = []
    for i in range(1, 128, 2):
        list_away.append(list_1[i].get_text())

    array_atn = df_util["Away Team Name"].values
    list_aux = list(array_atn)
    for i in (list_away[::-1]):
        list_aux.append(i)

    array_6 = np.array(list_aux)
    return pd.Series(array_6, index = range(0, len(list_aux)))

# Correcting the names of the teams:

def correcting_names(df_original):
    df_original["home_team_names"].values[df_original["home_team_names"].values == 'rn">Bosnia and Herzegovina'] = "Bosnia and Herzegovina"
    df_original["home_team_names"].values[df_original["home_team_names"].values == 'rn">Republic of Ireland'] = 'Republic of Ireland'
    df_original["home_team_names"].values[df_original["home_team_names"].values == 'rn">Serbia and Montenegro'] = 'Serbia and Montenegro'
    df_original["home_team_names"].values[df_original["home_team_names"].values == 'rn">Trinidad and Tobago'] = 'Trinidad and Tobago'
    df_original["home_team_names"].values[df_original["home_team_names"].values == 'rn">United Arab Emirates'] = 'United Arab Emirates'

    df_original["away_team_names"].values[df_original["away_team_names"].values == 'rn">Bosnia and Herzegovina'] = "Bosnia and Herzegovina"
    df_original["away_team_names"].values[df_original["away_team_names"].values == 'rn">Republic of Ireland'] = 'Republic of Ireland'
    df_original["away_team_names"].values[df_original["away_team_names"].values == 'rn">Serbia and Montenegro'] = 'Serbia and Montenegro'
    df_original["away_team_names"].values[df_original["away_team_names"].values == 'rn">Trinidad and Tobago'] = 'Trinidad and Tobago'
    df_original["away_team_names"].values[df_original["away_team_names"].values == 'rn">United Arab Emirates'] = 'United Arab Emirates'

    return df_original

def appending_victory_column(df):
    list_hg = list(df["home_team_goals"].values)
    list_ag = list(df["away_team_goals"].values)
    comparison_list = list(zip(list_hg, list_ag))

    list_victory = []

    for (i,j) in comparison_list:
        if (i > j):
            list_victory.append("home")
        elif (j > i):
            list_victory.append("away")
        else:
            list_victory.append("tie")

    df["victory"] = list_victory
    return df

def appending_loss_column(df):
    list_aux_loss = []

    for i in df["victory"].values:
        if (i == "home"):
            list_aux_loss.append("away")
        elif (i == "away"):
            list_aux_loss.append("home")
        else:
            list_aux_loss.append("tie")
        
    df["loss"] = list_aux_loss
    return df

# Create the integrated Dataframe

def create_df_new():
    df = pd.DataFrame()
    
    year = df_year_series(df_util)

    df["year"] = year
    
    htn = df_htn_series(df_util, list_1)

    df["home_team_names"] = htn

    htg = df_htg_series(df_util, list_2)

    df["home_team_goals"] = htg

    atg = df_atg_series(df_util, list_2)

    df["away_team_goals"] = atg

    atn = df_atn_series(df_util, list_1)

    df["away_team_names"] = atn

    df.dropna(inplace = True)

    df = correcting_names(df)
    df = appending_victory_column(df)
    df = appending_loss_column(df)

    return df 

if page.status_code == 200:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")   

    # Aux lists

    list_1 = soup.find_all("td", class_ = "team")

    # Removing flags from list_1:

    k = 0
    for j in range(8):
        for i in range(4):
            del list_1[32 + k]
        k += 12

    list_2 = []
    for i in soup.find_all("td", class_ = "score"):
        list_2.append(i.get_text())

    df_original = create_df_new()

    df_original = correcting_names(df_original)

else:
    print("Error in the HTTPS requisition")

if __name__ == "__main__":
    print("A library to integrate data and make a dataframe for WC matches data analysis.\n")
