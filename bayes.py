# This script scrapes the partial URL of every box
# score in the team schedule and then reconstructs
# the full URL. The idea is that you could then go
# to each of these box score URLs and scrape further
# data.

import requests, re, math
from bs4 import BeautifulSoup
from datetime import datetime


# Site to begin scraping
url = "https://www.pro-football-reference.com/teams/nwe/2023.htm"

# Scrape start page into tree
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

# Isolate the schedule table by id, and grab every row
schedule_table = soup.find(id="games")
# schedule_table = soup.find('tbody', { 'id' : "games" })
rows = schedule_table.findChildren('tr')

Wins = 0; 
nightGame = 0;
totalGames = 0; 



# Loop through every row
for row in rows:
    # Isolate the box score cell using the data-stat attribute
    outcome = row.find('td', {"data-stat": "game_outcome"})
    game_times = row.find('td', {"data-stat": "game_time"})

    totalGames += 1 



    if outcome and outcome.text.strip() == 'W':
        Wins += 1 

    elif game_times:
        try:
            # Remove the timezone from the time string for parsing
            game_time_str = game_times.text.strip().rsplit(' ', 1)[0]
            if len(game_time_str) == 0:
                continue
            game_time_obj = datetime.strptime(game_time_str, '%I:%M%p').time()

            # Convert the comparison time to a datetime.time object
            comparison_time_obj = datetime.strptime("4:00PM", '%I:%M%p').time()

            if game_time_obj > comparison_time_obj:
                nightGame += 1

        except ValueError as e:
            print(f"Error parsing time: {e}")

    else:
        continue

# P(A) = chance of nightgame 
probA = nightGame/totalGames; 


# P(B) = chance of win
probB = Wins/totalGames; 


# P(B|A) = prob of win given its a night game 
probBgivenA = Wins/nightGame;

#BAYES 
if probB > 0: 
    probAgivenB = (probBgivenA * probA) # / probB
    print(probAgivenB)




   





    


    
    
    