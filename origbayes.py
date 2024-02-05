# This script scrapes the partial URL of every box
# score in the team schedule and then reconstructs
# the full URL. The idea is that you could then go
# to each of these box score URLs and scrape further
# data.

import requests, re, math
from bs4 import BeautifulSoup

# Site to begin scraping
url = "https://www.baseball-reference.com/teams/PIT/2020-schedule-scores.shtml"

# Scrape start page into tree
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

# Isolate the schedule table by id, and grab every row
schedule_table = soup.find(id="team_schedule")
rows = schedule_table.findChildren('tr')

# Loop through every row
for row in rows:
    # Isolate the box score cell using the data-stat attribute
    boxscore_td = row.findChildren('td', {"data-stat" : "boxscore"})
    if len(boxscore_td) == 0:
        continue

    # Isolate the link and grab it's href field
    game_href = boxscore_td[0].find('a', href=True)['href']
    
    #Get the root url of the page variable
    regex = r'.*\.com'
    url_root = re.findall(regex, url)[0]
    
    # Formulate the final game base_url
    game_url = '{}{}'.format(url_root, game_href)
    
    print(game_url)
    