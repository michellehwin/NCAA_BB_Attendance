import requests as rq
from bs4 import BeautifulSoup as bs
import pandas as pd
import json


url = "https://www.espn.com/womens-college-basketball/teams"
page = rq.get(url)
soup = bs(page.content, features="lxml")
team_sections = soup.find_all('section', {"class": "TeamLinks"})
team_dict = {}
for section in team_sections:
    team_info_div = section.find('div')
    id_start_index = team_info_div.a['href'].find('id') + 3
    id_end_index = team_info_div.a['href'].find('/', id_start_index)
    team_id = team_info_div.a['href'][id_start_index:id_end_index]
    team_name = team_info_div.h2.contents[0]
    team_dict[team_name] = team_id

with open('espn_team_ids.json', 'w') as fp:
    json.dump(team_dict, fp)