# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 13:21:25 2018
@author: Ken

@Modified by: Chigozie Muonagolu 
          on: March 2023     

Purpose:    Using Ken's python NBAGameSimulator to create a simulatuation of
            the 2017-2018 NBA finals to determine the expected win probability of each team.
"""

from NBAGameSimulator import *
from ExternalClasses import Team
import matplotlib.pyplot as plt
import numpy as np
import random as random


# Western Conference team names
west_team_names = ['GSW', 'HOU', 'POR', 'OKC', 'UTA', 'NOP', 'SAS', 'MIN']

# Eastern Conference team names
east_team_names = ['TOR', 'BOS', 'PHI', 'CLE', 'IND', 'MIA', 'MIL', 'WAS']

# Western Conference team 
west_teams = []
# Eastern Conference team 
east_teams = []

# Arrays represeting the game rounds

# first round
west_first_round = [('GSW', 'SAS'), ('HOU', 'MIN'), ('POR', 'NOP'), ('OKC', 'UTA')]
east_first_round =  [('TOR', 'WAS'), ('BOS', 'MIL'), ('PHI', 'MIA'), ('CLE', 'IND')]

# semifinal round
west_semifinals = []
east_semifinals = []

# confrence finals round
west_finals = []
east_finals = []

# nba finals round
nba_finals =[]


# Function to initialize a team
def create_team(team):
    # Loading the data
    gdf = pd.read_csv('nba_games_stats.csv')
    team_df = gdf[gdf.Team == team]

    # Convert date column to datetime format and filter by date range
    team_df['Date'] = pd.to_datetime(team_df['Date'], format='%Y-%m-%d', errors='ignore')
    team_df = team_df.loc[(team_df['Date'] > pd.to_datetime('2017-10-01', format='%Y-%m-%d')) & 
                          (team_df['Date'] <= pd.to_datetime('2018-05-31', format='%Y-%m-%d'))]

    # calculate the means and standard deviations of the points scored and points scored against
    mean_pts = team_df.TeamPoints.mean()
    sd_pts = team_df.TeamPoints.std()
    mean_opp = team_df.OpponentPoints.mean()
    sd_opp = team_df.OpponentPoints.std()

    # create and return a Team object with the relevant attributes
    team_obj = Team()
    team_obj.name = team
    team_obj.mean_pts = mean_pts
    team_obj.sd_pts = sd_pts
    team_obj.mean_opp = mean_opp
    team_obj.sd_opp = sd_opp

    return team_obj

# Function to simulate a game 
def gameSim(team1, team2):
    #randomly samples from a distribution with a mean=100 and a SD=15
    random.gauss(100, 15)

    GSWScore = (rnd.gauss(team1.mean_pts,team1.sd_pts)+rnd.gauss(team2.mean_opp,team2.sd_opp))/2
    CLScore = (rnd.gauss(team2.mean_pts,team2.sd_pts)+rnd.gauss(team1.mean_opp,team1.sd_opp))/2
    if int(round(GSWScore)) > int(round(CLScore)):
        return 1
    elif int(round(GSWScore)) < int(round(CLScore)):
        return -1
    else: return 0

# wrapper function for gameSim, to run multiple simulations for 1 game
def gamesSim(ns, team1, team2):
    gamesout = []
    team1win = 0
    team2win = 0
    tie = 0
    for i in range(ns):
        gm = gameSim(team1, team2)
        gamesout.append(gm)
        if gm == 1:
            team1win +=1 
        elif gm == -1:
            team2win +=1
        else: tie +=1 

    team1WinRate = team1win/(team1win+team2win+tie)
    team2WinRate = team2win/(team1win+team2win+tie)
    
    team1.winRate.append(team1WinRate)
    team2.winRate.append(team2WinRate)

    if(team1WinRate > team2WinRate):
        team1.playoffsWins+=1
        team2.playoffsLosses+=1
    elif(team1WinRate < team2WinRate):
        team2.playoffsWins+=1
        team1.playoffsLosses+=1
    
    print((team1.name),'Win ', team1WinRate,'%')
    print((team2.name),' Win ', team2WinRate,'%')
    print('Tie ', tie/(team1win+team2win+tie), '%')
    return gamesout

# function to load teams on start
def loadTeams():
    # Initialize Western Conference teams
    for team_abbr in west_team_names:
        west_teams.append(create_team(team_abbr))

    # Initialize Eastern Conference teams
    for team_abbr in east_team_names:
        east_teams.append(create_team(team_abbr)) 

# function to Simulates a playoff series
def simulate_series(team1, team2):

    # Run until one team wins the series
    x = 1
    while True:
        print(f"Game: {x}")
        gamesSim(1000, team1, team2)
        print(f"\n") 
        
        # If one team wins 4 games, end the loop and declare the winner
        if team1.playoffsWins >= 4:
            print(f"\n{team1.name} wins the series!")
            break
        elif team2.playoffsWins >= 4:
            print(f"\n{team2.name} wins the series!")
            break
        
        # If 7 games have been played and the series is tied, flip a coin to determine the winner
        if x == 7 and team1.playoffsWins == team2.playoffsWins:
            coin = random.randint(0, 1)
            if coin == 0:
                team1.playoffsWins += 1
                team2.playoffsLosses += 1
                print(f"\n{team1.name} wins Game 7!")
            else:
                team2.playoffsWins += 1
                team1.playoffsLosses += 1
                print(f"\n{team2.name} wins Game 7!")
        
        x += 1

# function to simulate first round
def first_round_simulation():
    # Western confrence
    for matchup in west_first_round:
        # Get the team names from the tuple
        team1_name = matchup[0] 
        team2_name = matchup[1]  

        # Search for the first team in the west_teams array
        for team in west_teams:
            if team.name == team1_name:
                team1 = team
                break

        # Search for the second team in the west_teams array
        for team in west_teams:
            if team.name == team2_name:
                team2 = team
                break
        #run simulation for that round 
        print(f"\n{team1.name} vs {team2.name}")
        simulate_series(team1, team2)

        #Determine the winner
        if team1.playoffsWins > team2.playoffsWins:
            west_semifinals.append(team1)
        else:
            west_semifinals.append(team2)

    # Eastern Confrence 
    for matchup in east_first_round:
        # Get the team names from the tuple
        team1_name = matchup[0] 
        team2_name = matchup[1]  

        # Search for the first team in the west_teams array
        for team in east_teams:
            if team.name == team1_name:
                team1 = team
                break

        # Search for the second team in the west_teams array
        for team in east_teams:
            if team.name == team2_name:
                team2 = team
                break
        
        #run simulation for that round 
        print(f"\n{team1.name} vs {team2.name}")
        simulate_series(team1, team2)

        #Determine the winner
        if team1.playoffsWins > team2.playoffsWins:
            print(f"Winner: {team1.name}")
            east_semifinals.append(team1)
        else:
            print(f"Winner: {team2.name}")
            east_semifinals.append(team2)

# function to simulate semi finals
def semi_finals_simulation():
    # Westeren confrence
    x = 0
    for i in range(2):
        # Create bracket
        team1 = west_semifinals[x]
        x+=1
        team2 = west_semifinals[x]

        team1.Reset()
        team2.Reset()
        #run simulation for that bracket 
        print(f"\n{team1.name} vs {team2.name}")
        simulate_series(team1, team2)

        #Determine the winner
        if team1.playoffsWins > team2.playoffsWins:
            print(f"Winner: {team1.name}")
            west_finals.append(team1)
        else:
            print(f"Winner: {team2.name}")
            west_finals.append(team2)

        x+=1
    # Eastern confrence
    x = 0
    for i in range(2):
        # Create bracket
        team1 = east_semifinals[x]
        x+=1
        team2 = east_semifinals[x]

        team1.Reset()
        team2.Reset()

        #run simulation for that bracket 
        print(f"\n{team1.name} vs {team2.name}")
        simulate_series(team1, team2)
        
        #Determine the winner
        if team1.playoffsWins > team2.playoffsWins:
            print(f"Winner: {team1.name}")
            east_finals.append(team1)
        else:
            print(f"Winner: {team2.name}")
            east_finals.append(team2)

        x+=1

# Function to simulate conference finals
def conference_finals_simulation():
    
    # Western conference finals
    team1 = west_finals[0]
    team2 = west_finals[1]
    team1.Reset()
    team2.Reset()
    print(f"\nWestern Conference Finals: {team1.name} vs {team2.name}")
    simulate_series(team1, team2)

    # Determine the winner
    if team1.playoffsWins > team2.playoffsWins:
        print(f"\n{team1.name} wins the Western Conference Finals!")
        nba_finals.append(team1)
    else:
        print(f"\n{team2.name} wins the Western Conference Finals!")
        nba_finals.append(team2)

    # Eastern conference finals
    team1 = east_finals[0]
    team2 = east_finals[1]
    team1.Reset()
    team2.Reset()
    print(f"\nEastern Conference Finals: {team1.name} vs {team2.name}")
    simulate_series(team1, team2)

    # Determine the winner
    if team1.playoffsWins > team2.playoffsWins:
        print(f"\n{team1.name} wins the Eastern Conference Finals!")
        nba_finals.append(team1)
    else:
        print(f"\n{team2.name} wins the Eastern Conference Finals!")
        nba_finals.append(team2)


# Function to simulate NBA finals
def nba_finals_simulation():
    
    # NBA finals
    team1 = nba_finals[0]
    team2 = nba_finals[0]
    team1.Reset()
    team2.Reset()
    print(f"\nNBA Finals: {team1.name} vs {team2.name}")
    simulate_series(team1, team2)

    # Determine the winner
    if team1.playoffsWins > team2.playoffsWins:
        print(f"\n{team1.name} wins the NBA Finals!")
    else:
        print(f"\n{team2.name} wins the NBA Finals!")

# plot top 2 teams win percentage
def plot_graph():
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'yellow', 'black', 'teal', 'olive']

    # First team plot
    plt.figure(figsize=(10, 6))
    for i in range(len(nba_finals[0].winRate)):
        x = (i)%len(colors)
        plt.bar(i, nba_finals[0].winRate[i], color=colors[x])

    plt.xticks(range(len(nba_finals[0].winRate)), [str(i+1) for i in range(len(nba_finals[0].winRate))])
    plt.xlabel('Games')
    plt.ylabel('Win Percentage')
    plt.title(f'Histogram of Win Percentage of {nba_finals[0].name}')
    plt.show()

    # Second team plot
    plt.figure(figsize=(10, 6))
    for i in range(len(nba_finals[1].winRate)-1):
        x = (i)%len(colors)
        plt.bar(i, nba_finals[1].winRate[i], color=colors[x])

    plt.xticks(range(len(nba_finals[1].winRate)), [str(i+1) for i in range(len(nba_finals[1].winRate))])
    plt.xlabel('Games')
    plt.ylabel('Win Percentage')
    plt.title(f'Histogram of Win Percentage of {nba_finals[1].name}')
    plt.show()

# Simulation 
loadTeams()
first_round_simulation()
semi_finals_simulation()
conference_finals_simulation()
nba_finals_simulation()
plot_graph()
